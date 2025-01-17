# urls.py
from django.urls import path
from main.views.renovation import RenovationListView, RenovationView

urlpatterns = [
    path('view', RenovationListView.as_view(), name='renovation-list-view'),
    path('view/<str:track>', RenovationView.as_view(), name='renovation-view'),
]


