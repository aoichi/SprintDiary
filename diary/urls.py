from django.views import generic
from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.DiaryList.as_view(), name='list'),
    path('detail/<int:pk>/', views.DiaryDetail.as_view(), name='detail'),
    path('category/<int:pk>/', views.DiaryCategoryList.as_view(), name='category'),
    path('search/', views.DiarySearchList.as_view(), name='search'),
]
