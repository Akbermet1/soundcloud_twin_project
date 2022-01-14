from django.urls import path, include
from .views import RegisterView, LoginView, ActivateView, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:activation_code>/', ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]