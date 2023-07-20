from .models import PersonalDetails
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class PresonalDetailsForm(ModelForm):
    class Meta:
        model=PersonalDetails
        fields='__all__'#['age','blood_group']

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
    def save(self,commit=False):
        user = super(UserRegistrationForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user #creates a new instance of the form and saves it to db
class UserUpdateForm(ModelForm):
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'email' ]
class ProfileUpdateForm(ModelForm):
    class Meta:
        model=PersonalDetails
        fields=['age','blood_group','profile_image']