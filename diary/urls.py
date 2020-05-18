from django.views import generic
from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('user/', views.DiaryList.as_view(), name='diary'),
    path('user/detail/<int:pk>/', views.DiaryDetail.as_view(), name='detail'),
    path('user/category/<int:pk>/', views.DiaryCategoryList.as_view(), name='category'),
    path('user/search/', views.DiarySearchList.as_view(), name='search'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('user/update/', views.UserUpdate.as_view(), name='user_update'),
    #path('user/<int:pk>/update/', views.UserUpdate.as_view(), name='user_update'),
    #path('user/<int:pk>/profile/', views.UserDetail.as_view(), name='user_detail'),
    path('user/profile/', views.UserDetail.as_view(), name='user_detail'),
    path('user/<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete'),
    path('user/post/', views.PostCreate.as_view(), name='post'),
    path('user/recommend/', views.RecommendList.as_view(), name='recommend'),
    path('user/recommend/detail/<int:pk>/', views.DiaryDetail.as_view(), name='recommend_detail'),
    #path('user/recommend/category/<int:pk>/', views.RecommendCategoryList.as_view(), name='recommend_category'),
    #path('user/recommend/search/', views.RecommendSearchList.as_view(), name='recommend_search'),
]
