from django.urls import path
from .views import *
from django.contrib.auth import views as authViews


app_name="users"
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('password-change/',authViews.PasswordChangeView.as_view(),name='password_change'),
    path('password-change-done/',authViews.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('update-profile/<slug:slug>/',UserProfileUpdateView.as_view(),name='update_profile'),
    path('create_code2/',create_code2,name='create_code2'),
    path('create_now/',create_now,name='create_now'),
    path('delete_now/',delete_now,name='delete_now'),
]