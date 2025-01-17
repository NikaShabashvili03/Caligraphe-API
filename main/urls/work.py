# urls.py
from django.urls import path
from main.views.work import WorkView

urlpatterns = [
    path('view/<int:id>', WorkView.as_view(), name='work-view'),
]


