from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import Photo
from .forms import ImageCreateForm
from .forms import ImageChangeForm


class ImageCreateView(CreateView):
    model = Photo
    form_class = ImageCreateForm
    template_name = 'create.html'

    def get_success_url(self):
        return reverse_lazy('image_update', kwargs={'pk': self.object.id})


class ImagesListView(ListView):
    model = Photo
    template_name = 'index.html'


class ImageUpdateView(UpdateView):
    template_name = 'detail.html'
    model = Photo
    form_class = ImageChangeForm
