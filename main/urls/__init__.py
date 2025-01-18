from django.urls import path, include

urlpatterns = [
    path('supervisor/', include('main.urls.supervisor')),
    path('renovation/', include('main.urls.renovation')),
    path('service/', include('main.urls.service')),
    path('stage/', include('main.urls.stage'))
]
