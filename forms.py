# forms.py
from django import forms
from .models import NewsletterSubscriber
from django import forms
from .models import Contact
from .models import BlogPost

from ckeditor_uploader.widgets import CKEditorUploadingWidget  # CKEditorUploadingWidget kullanılacak

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = BlogPost
        fields = '__all__'


class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']





class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'İsim'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyisim'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Mail'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Konu'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mesaj', 'rows': 3}),
        }
