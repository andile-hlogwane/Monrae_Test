from django.urls import path
from . import views

urlpatterns = [
    path("sentiment-analysis/", views.AsyncNLPView.as_view()),
]
