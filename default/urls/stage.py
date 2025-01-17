from django.urls import path
from default.views.stage import StageListView, StageView

urlpatterns = [
    path('view', StageListView.as_view(), name='stage-list-view'),
    path('view/<int:id>', StageView.as_view(), name='stage-view'),
]


