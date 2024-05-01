from django.urls import path
from .views import home, register, update_profile
from quizzes.forms import CustomAuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm
        , next_page=update_profile
    ), name='login'),
    path('profile/', update_profile, name='update_profile'),
    path('logout/', LogoutView.as_view(next_page=home), name='logout'),
]
