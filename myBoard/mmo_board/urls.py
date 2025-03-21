from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('response/accept/<int:pk>/', views.response_accept, name='response_accept'),
    path('response/delete/<int:pk>/', views.response_delete, name='response_delete'),
    path('newsletter/create/', views.create_newsletter, name='create_newsletter'),
]
