from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'country')

    def clean_email(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[1]
        domain_list = ["mytudublin.ie"]
        if domain not in domain_list:
            raise forms.ValidationError("Please use your '@mytudublin.ie' email address provided.")
        return data

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'country')

class ProfileEditForm(forms.ModelForm):
  
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo', 'bio')
