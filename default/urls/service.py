# urls.py
from django.urls import path
from default.views.service import ServiceListView, ServiceView

urlpatterns = [
    path('view', ServiceListView.as_view(), name='service-list-view'),
    path('view/<int:id>', ServiceView.as_view(), name='service-view'),
]


