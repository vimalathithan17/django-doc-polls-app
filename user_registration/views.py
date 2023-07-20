from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import PresonalDetailsForm,UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PersonalDetails
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
# Create your views here.
from .decorators import user_not_authenticated
from django.contrib.auth.forms import AuthenticationForm

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('polls:index')

def activate_email(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("user_registration/template_activate_account.html", 
        {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
@user_not_authenticated
def register(request):# have to add try block if user alredy exists!!!!!
    #user_form=UserCreationForm()
    #detail_form=PresonalDetailsForm()
    #content={'user_form':user_form,'details':detail_form}
    #user_form=UserCreationForm()
    #content={'user_form':user_form}
    """if request.method=='POST':
        user_form=UserRegistrationForm(request.POST)
        d=dict(request.POST)
        print(d,type(d))
        k=list(request.POST.keys())
        v=list(request.POST.values())
        di=dict(zip(k[1:7],v[1:7]))
        print("di",di,type(di))
        new=UserRegistrationForm(di)
        print("new",new.is_valid())
        print(request.POST)
        #print(user_form)
        #print(user_form.is_valid())
        #
        '''d2=dict(zip(k[4:],v[4:]))
        print("d2",d2)
        
        print("d2frm",detail_form.is_valid())'''
        #print("new",new,"\nusr",user_form,"\nd2",d2)
        if new.is_valid():
            new.save()
            d2=dict()
            usn=new.cleaned_data.get('username')
            id=User.objects.get(username=usn).id
            print('id',type(id),id)
            d2['user']=str(id)
            d2.update(zip(k[7:],v[7:]))
            '''d2=dict(zip(k[4:],v[4:]))'''
            print(d2)
            detail_form=PresonalDetailsForm(d2)
            print("d2frm",detail_form.is_valid())
            if detail_form.is_valid():
            #new.save()
                try:
                    detail_form.save()
                except Exception as err:
                    print(err)
                    for error in list(detail_form.errors.values()):
                        messages.error(request, error)
                else:
                    messages.success(request,'user acc created for {}'.format(usn))
                    new_user=User.objects.get(username=usn)
                    login(request,new_user)
                    return redirect('polls:index')
        else:
            for error in list(new.errors.values()):
                messages.error(request, error)
            detail_form=PresonalDetailsForm()"""
    if request.method=='POST':
        k=list(request.POST.keys())
        v=list(request.POST.values())
        di=dict(zip(k[1:7],v[1:7]))
        user_form=UserRegistrationForm(di)
        print("new",user_form.is_valid())
        print(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.is_active=False
            new_user.save()
            activate_email(request,new_user,user_form.cleaned_data.get('email'))
            d2=dict()
            usn=user_form.cleaned_data.get('username')
            id=User.objects.get(username=usn).id
            print('id',type(id),id)
            d2['user']=str(id)
            d2.update(zip(k[7:],v[7:]))
            print(d2)
            detail_form=PresonalDetailsForm(d2)
            print("d2frm",detail_form.is_valid())
            if detail_form.is_valid():
                try:
                    detail_form.save()
                except Exception as err:
                    print(err)
                    for error in list(detail_form.errors.values()):
                        messages.error(request, error)
                else:
                    messages.success(request,'user acc created for {}'.format(usn))
                    new_user=User.objects.get(username=usn)
                    login(request,new_user)
                    return redirect('polls:index')
        else:
            for error in list(user_form.errors.values()):
                messages.error(request, error)
            detail_form=PresonalDetailsForm()
            

    else:
        user_form=UserRegistrationForm()
        detail_form=PresonalDetailsForm()
    #content={'user_form':user_form}
    content={'user_form':user_form,'details':detail_form}
    return render(request,'user_registration/register.html',content)
@login_required
def profile_pg(request):
    return render(request,'user_registration/profile.html')
@user_not_authenticated
def custom_login(request):
    if request.method == 'POST':
        form=AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data['username'],
                          password=form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                messages.success(request,f"hello{user.username}")
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('polls:index')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    form=AuthenticationForm()
    return render(request,'user_registration/login.html',{'form':form})
@login_required
def custom_logout(request):
    logout(request)
    #messages.info(request,'logged out sucessfully')
    return render(request,'user_registration/logout.html')
@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form=UserUpdateForm(request.POST,
                              instance=request.user)
        p_form=ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.personaldetails)
        print(request.POST,u_form.is_valid(), p_form.is_valid())
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'sucessesfully updated your profile')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.personaldetails)
    return render(request,'user_registration/edit_profile.html',{'u_form':u_form,'p_form':p_form})