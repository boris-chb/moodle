from django.urls import path
from . import views

urlpatterns = [
    path('register/',
         views.StudentRegistrationView.as_view(), name='student_registration'),
    path('enroll-module/',
         views.StudentEnrollModuleView.as_view(), name='student_enroll_module'),
]
