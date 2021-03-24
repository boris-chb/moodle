
from django.urls import path
from . import views

urlpatterns = [
    # Order: View > Create > Update > Delete
    # Modules
    # List View For Instructors
    path('dashboard/',
         views.ManageModuleListView.as_view(), name='manage_module_list'),
    # List View For Students
    path('all/', views.ModuleListView.as_view(), name='module_list'),
    path('create/',
         views.ModuleCreateView.as_view(), name='module_create'),
    path('edit/<int:pk>/',
         views.ModuleUpdateView.as_view(), name='module_edit'),
    path('delete/<int:pk>/',
         views.ModuleDeleteView.as_view(), name='module_delete'),
    path('<slug:slug>/',
         views.ModuleDetailView.as_view(), name='module_detail'),

    # Topics
    path('<pk>/topic/',
         views.ModuleTopicUpdateView.as_view(), name='module_topic_update'),

    # Resources
    path('topic/<int:topic_id>/',
         views.TopicResourceListView.as_view(), name='topic_resource_list'),

    path('topic/<int:topic_id>/resource/<model_name>/create/',
         views.ResourceCreateUpdateView.as_view(), name='topic_resource_create'),

    path('topic/<int:topic_id>/resource/<model_name>/<id>/',
         views.ResourceCreateUpdateView.as_view(), name='topic_resource_update'),

    path('resource/<int:id>/delete/',
         views.ResourceDeleteView.as_view(), name='topic_resource_delete'),
]
