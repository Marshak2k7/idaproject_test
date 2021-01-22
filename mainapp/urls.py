from django.urls import path
from . import views

urlpatterns = [
    path('', views.ImagesListView.as_view(), name='list'),
    path('create/', views.ImageCreateView.as_view(), name='create_image'),
    path('<int:pk>/', views.ImageUpdateView.as_view(), name='image_update'),
]
