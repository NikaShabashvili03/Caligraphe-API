from django.urls import path, include

urlpatterns = [
    path('work/', include('default.urls.work')),
    path('stage/', include('default.urls.stage')),
]
