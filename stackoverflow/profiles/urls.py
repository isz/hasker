from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'profile'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='profile/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.profile_view, name='details'),
]
