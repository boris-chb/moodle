
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.ModuleListView.as_view(), name='module_list'),
    path('create/', views.ModuleCreateView.as_view(), name='module_create'),
    path('<pk>/edit/', views.ModuleUpdateView.as_view(), name='module_edit'),
    path('<pk>/delete/', views.ModuleDeleteView.as_view(), name='module_delete'),
    ]
