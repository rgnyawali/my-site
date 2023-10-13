from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterForm(UserCreationForm):
	email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	
class PasswordReset(forms.Form):
	email = forms.EmailField(label="Email")

class SetPassword(forms.Form):
 password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
		)
 password2 = forms.CharField(
        label=("Password Confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,   
    )
 
 def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            validate_password(password1)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1
 
 def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
