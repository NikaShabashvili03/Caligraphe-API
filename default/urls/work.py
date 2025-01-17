# urls.py
from django.urls import path
from default.views.work import WorkListView, WorkView

urlpatterns = [
    path('view', WorkListView.as_view(), name='work-list-view'),
    path('view/<int:id>', WorkView.as_view(), name='work-view'),
]


