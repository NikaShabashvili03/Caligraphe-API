from django.urls import path
from authentication.views.supervisor import SupervisorLoginView, SupervisorProfileView, SupervisorLogoutView

urlpatterns = [
    path('login', SupervisorLoginView.as_view(), name='supervisor-login'),
    path('profile', SupervisorProfileView.as_view(), name='supervisor-profile'),
    path('logout', SupervisorLogoutView.as_view(), name="supervisor-logout"),
]