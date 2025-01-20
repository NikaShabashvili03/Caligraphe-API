from django.urls import path, include

urlpatterns = [
    path('customer/', include('authentication.urls.customer')),
    path('supervisor/', include('authentication.urls.supervisor')),
]
