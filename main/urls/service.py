# urls.py
from django.urls import path
from main.views.service import ServiceView

urlpatterns = [
    path('view/<int:id>', ServiceView.as_view(), name='service-view'),
]


