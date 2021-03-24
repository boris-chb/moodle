from django.urls import path
from . import views

urlpatterns = [
    path('register/',
         views.StudentRegistrationView.as_view(), name='student_registration'),

    # Modules
    path('enroll-module/',
         views.StudentEnrollModuleView.as_view(), name='student_enroll_module'),
    path('modules/', views.StudentModuleListView.as_view(),
         name='student_module_list'),
    path('module/<pk>/', views.StudentModuleDetailView.as_view(),
         name='student_module_detail'),
    
    # Topics
    # path('module/<pk>/topic/<topic_id>/', views.StudentTopicDetailView.as_view(),
    #      name='student_topic_detail'),
]
