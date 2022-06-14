from django.urls import path
from .views import CreateView, GetView, UpdateView, DeleteView

urlpatterns = [
    path('add', CreateView.as_view()),
    path('', GetView.as_view()),
    path('update', UpdateView.as_view()),
    path('delete', DeleteView.as_view()),
]
