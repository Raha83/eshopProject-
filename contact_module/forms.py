from django import forms
from .models import ContactUs

class ContactUsForm(forms.Form):
    full_name=forms.CharField(label="نام و نام خانوادگی",
    max_length=50,
    error_messages={
       'required' : 'لطفا نام و نام خانوادگی خود را وارد کنید',
       'max_length': 'نام و نام خانوادگی نمی تواند بیشتر از 50 کاراکتر باشد'
    },
    widget=forms.TextInput(attrs={
      'class':'form-control',
      'placeholder':'نام و نام خانوادگی'
    }
    ))
    email=forms.EmailField(label="ایمیل",
    widget=forms.EmailInput(attrs={
      'class':'form-control',
      'placeholder':'ایمیل'
    }))
    title=forms.CharField(label="موضوع",
    widget=forms.TextInput(attrs={
      'class':'form-control',
      'placeholder':'عنوان'
    }))
    message=forms.CharField(label="متن",
    widget=forms.Textarea(attrs={
      'class':'form-control',
      'placeholder':'متن پیام',
      'rows':'5',
      'id':'message'
    }))

class ContactUsModelForm(forms.ModelForm):
  class Meta:
    model=ContactUs
    fields=["full_name","email","title","message"]
    widgets={
      'full_name':forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'نام و نام خانوادگی'
      }),
      'email':forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'ایمیل'
      }),
      'title':forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'عنوان'
      }),
      'message':forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'متن پیام',
        'rows':5,
        'id':'message'
      })
    }
    labels={
      'message':'متن پیام'
    }
    error_messages={
      'full_name':{
        'required' : 'لطفا نام و نام خانوادگی خود را وارد کنید',
        'max_length': 'نام و نام خانوادگی نمی تواند بیشتر از 50 کاراکتر باشد'
      }
    }


