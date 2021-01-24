import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models
from django.urls import reverse
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Photo(models.Model):
    image_file = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='Файл')
    image_url = models.URLField(null=True, blank=True, verbose_name='Ссылка')
    width = models.IntegerField(blank=True, default=0, verbose_name='Ширина')
    height = models.IntegerField(blank=True, default=0, verbose_name='Высота')
    changed_image_file = models.ImageField(upload_to='images', blank=True)

    def save(self, *args, **kwargs, ):
        global changed_img
        if self.image_url and not self.image_file:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image_file.save(f"image_{self.pk}.jpeg", File(img_temp))

        img = Image.open(self.image_file)
        if self.changed_image_file:
            changed_img = Image.open(self.changed_image_file)
        if self.width == 0:
            self.width = img.width
        if self.height == 0:
            self.height = img.height
        if self.height == img.height or self.height == changed_img.height:
            basewidth = self.width
            wpercent = (basewidth / float(img.size[0]))
            self.height = int((float(img.size[1]) * float(wpercent)))
        if self.width == img.width or self.width == changed_img.width:
            baseheight = self.height
            hpercent = (baseheight / float(img.size[1]))
            self.width = int((float(img.size[0]) * float(hpercent)))
        new_img = img.convert('RGB')
        resized_new_image = new_img.resize((self.width, self.height), Image.ANTIALIAS)
        filestream = BytesIO()
        resized_new_image.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image_file.name.split('.'))
        self.changed_image_file = InMemoryUploadedFile(
            filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
        )
        super(Photo, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    def clean(self):
        super().clean()
        if not self.image_file and not self.image_url:
            raise ValidationError('Хотя бы одно поле должно быть заполнено', code='invalid')

        IMAGE_URL_ENDSWITH = (
            '.jpg',
            '.jpeg',
            '.png',
            '.gif',
        )
        if not self.image_file and self.image_url:
            if not str(self.image_url).endswith(IMAGE_URL_ENDSWITH):
                raise ValidationError('Неправильный URL. Он должен заканчиваться на {}'.format(IMAGE_URL_ENDSWITH),
                                      code='invalid url')

    def get_absolute_url(self):
        return reverse('image_update', kwargs={'pk': self.id})
