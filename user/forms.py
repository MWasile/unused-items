from django import forms
from django.contrib.auth import get_user_model


class ReigsterUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'last_name']

    def clean_email(self):
        email = self.cleaned_data['email']

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')

        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        re_password = self.data['re_password']

        if password != re_password:
            raise forms.ValidationError('Passwords do not match')

        if len(password) < 6:
            raise forms.ValidationError('Password must be at least 6 characters')

        return password

    def clean_username(self):
        username = self.cleaned_data['username']

        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')

        return username

    def create_new_user(self):
        return get_user_model().objects.create_user(
            username=self.cleaned_data['username'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )


class LoginUserForm(forms.Form):
    user_email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=200)

    def clean_user_email(self):
        user_email = self.cleaned_data['user_email']

        if not get_user_model().objects.filter(email=user_email).exists():
            raise forms.ValidationError('Email doesnt exist')

        return user_email

    def clean_password(self):
        password = self.cleaned_data['password']
        user_email = self.data.get('user_email')

        user = get_user_model().objects.filter(email=user_email).first()

        if not user:
            raise forms.ValidationError('User doesnt exist')

        if not user.check_password(password):
            raise forms.ValidationError('Incorrect password.')


        return password