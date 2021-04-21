
from django.urls import path
from .views import (
    manage_module_list_view,
    module_list_view,
    module_detail_view,
    module_create_view,
    module_update_view,
    module_delete_view,
    topic_update_view,
<<<<<<< HEAD
    resource_list_view,
    resource_create_view,
    resource_delete_view
=======
    resource_list_view
>>>>>>> 7305a80f7f143fcaaa6765bd1292ddb068bcd3aa
)

app_name = 'modules'

urlpatterns = [
    # Order: View > Create > Update > Delete
    # Modules
<<<<<<< HEAD
    path('dashboard/', manage_module_list_view, name='manage_list'),
=======
    # List View For Instructors
    path('dashboard/', manage_module_list_view, name='manage_list'),
    # List View For Students
>>>>>>> 7305a80f7f143fcaaa6765bd1292ddb068bcd3aa
    path('all/', module_list_view, name='list'),
    path('create/', module_create_view, name='create'),
    path('edit/<int:pk>/', module_update_view, name='edit'),
    path('delete/<int:pk>/', module_delete_view, name='delete'),
    path('<slug:slug>/', module_detail_view, name='detail'),

    # Topics
<<<<<<< HEAD
    path('topic/<int:pk>/edit/', topic_update_view, name='topic_update'),

    # Resources
    path('topic/<int:topic_id>/', resource_list_view, name='resource_list'),
    path('topic/<int:topic_id>/resource/<model_name>/create/',
         resource_create_view, name='resource_create'),
    path('topic/<int:topic_id>/resource/<model_name>/<id>/',
         resource_create_view, name='resource_update'),
    path('resource/<int:id>/delete/', resource_delete_view,
         name='resource_delete'),
=======
    path('<pk>/topic/', topic_update_view, name='topic_update'),

    # Resources
    path('topic/<int:topic_id>/', resource_list_view, name='resource_list'),

    #     path('topic/<int:topic_id>/resource/<model_name>/create/', views.ResourceCreateUpdateView.as_view(), name='topic_resource_create'),

    #     path('topic/<int:topic_id>/resource/<model_name>/<id>/', views.ResourceCreateUpdateView.as_view(), name='topic_resource_update'),

    #     path('resource/<int:id>/delete/', views.ResourceDeleteView.as_view(), name='topic_resource_delete'),
>>>>>>> 7305a80f7f143fcaaa6765bd1292ddb068bcd3aa
]
