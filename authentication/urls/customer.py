from django.urls import path
from authentication.views.customer import CustomerLoginView, CustomerProfileView, CustomerLogoutView, CustomerRegisterView

urlpatterns = [
    path('login', CustomerLoginView.as_view(), name='customer-login'),
    path('register', CustomerRegisterView.as_view(), name="customer-register"),
    path('profile', CustomerProfileView.as_view(), name='customer-profile'),
    path('logout', CustomerLogoutView.as_view(), name="customer-logout"),
]