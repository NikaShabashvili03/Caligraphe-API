from django.urls import path, include

urlpatterns = [
    path('service/', include('default.urls.service')),
    path('stage/', include('default.urls.stage')),
]
