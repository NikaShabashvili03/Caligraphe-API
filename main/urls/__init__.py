from django.urls import path, include

urlpatterns = [
    path('supervisor/', include('main.urls.supervisor')),
    path('renovation/', include('main.urls.renovation')),
    path('work/', include('main.urls.work')),
    path('stage/', include('main.urls.stage'))
]
