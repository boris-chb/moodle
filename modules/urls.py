from django.urls import path
from . import views

urlpatterns = [
  path('list/', views.ManagerCourseListView.as_view()),
]