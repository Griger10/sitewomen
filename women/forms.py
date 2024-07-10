from captcha.fields import CaptchaField
from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать русские символы, дефис и пробел'

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise forms.ValidationError(self.message, self.code)


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label='Категория не выбрана', label='Категории')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label='Не замужем',
                                     required=False, label='Муж')

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
        widgets = {'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
                   'title': forms.TextInput(attrs={'class': 'form-input'})}
        labels = {'slug': 'URL'}

    def clean_title(self):
        allowed_chars = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
        title = self.cleaned_data['title']
        if not (set(title) <= set(allowed_chars)):
            raise forms.ValidationError('Должны присутствовать русские символы, дефис и пробел')
        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя отправителя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()


