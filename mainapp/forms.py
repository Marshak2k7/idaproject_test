from django import forms
from django.core.exceptions import ValidationError
from .models import Photo


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image_file', 'image_url', 'width', 'height']

        widgets = {
            'width': forms.HiddenInput(attrs=
                                       {'required': False}
                                       ),
            'height': forms.HiddenInput(attrs=
                                        {'required': False}
                                        )
        }

    def clean(self):
        image_file = self.cleaned_data['image_file']
        image_url = self.cleaned_data['image_url']
        if image_file and image_url:
            raise ValidationError('Только одно поле должно быть заполнено', code='both fields')


class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['width', 'height']

    def clean_width(self):
        width = self.cleaned_data['width']
        if not width:
            raise ValidationError('Поле не должно быть пустым, оставьте значение по умолчанию или введите новое',
                                  code='empty width')
        if width < 0:
            raise ValidationError('Поле не должно быть отрицательным', code='zero or negative width')
        return width

    def clean_height(self):
        height = self.cleaned_data['height']
        if not height:
            raise ValidationError('Поле не должно быть пустым, оставьте значение по умолчанию или введите новое',
                                  code='empty height')
        if height < 0:
            raise ValidationError('Поле не должно быть отрицательным', code='zero or negative height')
        return height
