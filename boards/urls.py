from django.urls import path
from .views import CreateView, GetView, UpdateView, DeleteView, GetSortView, GetGroupByView

urlpatterns = [
    path('add', CreateView.as_view()),
    path('', GetView.as_view()),
    path('sort', GetSortView.as_view()),
    path('groupby', GetGroupByView.as_view()),
    path('update', UpdateView.as_view()),
    path('delete', DeleteView.as_view()),
]
