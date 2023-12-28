from django.urls import path

from . import views

app_name = 'history'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', views.UserLogsView.as_view(), name='users'),
    path('recover-users/<int:pk>/', views.UserRollbackView.as_view(), name='recover-users'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
]