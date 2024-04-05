from django.urls import path

from courses import views


urlpatterns = [
    path("mine/", views.ManageCourseListView.as_view(), name="manage_course_list"),
    path("create/", views.CreateCourseView.as_view(), name="create_course"),
    path("<pk>/edit/", views.UpdateCourseView.as_view(), name="edit_course"),
    path("<pk>/delete/", views.DeleteCourseView.as_view(), name="delete_course"),
]
