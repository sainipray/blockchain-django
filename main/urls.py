from django.urls import path

from main.views import MineView, NewTransationView, TrainView, NodeResolveView, NodeRegisterView

urlpatterns = [
    path('mine/', MineView.as_view()),
    path('transaction/new/', NewTransationView.as_view()),
    path('train/', TrainView.as_view()),
    path('nodes/resolve/', NodeResolveView.as_view()),
    path('nodes/register/', NodeRegisterView.as_view()),
]
