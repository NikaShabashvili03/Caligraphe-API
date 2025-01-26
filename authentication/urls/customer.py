from django.urls import path
from authentication.views.customer import CustomerResetPassword, CustomerLoginView, CustomerProfileView, CustomerLogoutView, CustomerRegisterView, GoogleLogin, CustomerVerificationEmail, CustomerSendVerificationEmail, CustomerSendResetPassword

urlpatterns = [
    path('login', CustomerLoginView.as_view(), name='customer-login'),
    path('register', CustomerRegisterView.as_view(), name="customer-register"),
    path('profile', CustomerProfileView.as_view(), name='customer-profile'),
    path('logout', CustomerLogoutView.as_view(), name="customer-logout"),
    path('verify-email/<str:token>', CustomerVerificationEmail.as_view(), name='verify-email'),
    path('reset-password/<str:token>', CustomerResetPassword.as_view(), name='reset-password'),
    path('send-email-verify', CustomerSendVerificationEmail.as_view(), name='send-email-verify'),
    path('send-password-reset', CustomerSendResetPassword.as_view(), name='send-password-reset'),
    path('auth/google', GoogleLogin.as_view(), name='google-login'),
]