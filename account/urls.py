from django.urls import path, include
from .views import (RegisterView, LoginView,
                    ActivateView, LogoutView,
                    ChangePasswordView, ForgotPasswordView,
                    ForgotPasswordCompleteView)


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:activation_code>/', ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_complete/', ForgotPasswordCompleteView.as_view()),
]