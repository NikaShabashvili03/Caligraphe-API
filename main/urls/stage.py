# urls.py
from django.urls import path
from main.views.stage import StageListView, StageCompleteView

urlpatterns = [
    path('view', StageListView.as_view(), name='stage-view'),
    path('complete/<int:id>', StageCompleteView.as_view(), name='stage-complete'),
]


