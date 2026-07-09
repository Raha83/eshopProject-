from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from account_module.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "avatar", "about_user", "address"]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }
        labels = {
            'fisrt_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'تصویر پروفایل',
            'about_user': 'درباره کاربر',
            'address': 'آدرس'
        }


class ChangePassForm(forms.Form):
    current_password = forms.CharField(
        label='رمز عبور فعلی',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    new_password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if new_password == confirm_password:
            return confirm_password

        raise ValidationError('رمز عبور با تکرار آن تطابق ندارد')
