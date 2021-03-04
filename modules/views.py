from django.urls import reverse_lazy
# from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Module

# A Django view is just a Python function that
# receives a web request and returns a web response. 
# We'll be using Mixins for our Class Based Views

class InstructorMixin:
    """
        Overriding a Manager’s base QuerySet - get_queryset().
        Used to retrieve objects from database.
        We'll filter just the objects that belong to current user.
        ELI5: Does a database query just for objects created by current user.
              Basically show me my modules only
    """
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(instructor=self.request.user)


class InstructorEditMixin:
    """
        Implementing the form_valid() method, which is used by 
        views with forms or model forms such as CreateView and UpdateView (using ModelFormMixin mixin).
        Also form_valid() is executed when the submitted form is valid.
    """
    def form_valid(self, form):
        # Sets the user as instructor during Module creation
        form.instance.instructor = self.request.user
        return super().form_valid(form)

# VIEW MIXIN 
class InstructorModuleMixin(InstructorMixin, LoginRequiredMixin, UserPassesTestMixin):
    model = Module
    fields = ['title', 'code', 'level', 'overview']
    # Redirect URL:
    success_url = reverse_lazy('module_list')

    # Checks whether user is staff (Instructor)
    # Students will get 403 Access Denied
    def test_func(self):
      return self.request.user.is_staff


# EDIT MIXIN
class InstructorModuleEditMixin(InstructorModuleMixin, InstructorEditMixin):
    template_name = 'manage/module/form.html'
    pass

########################
## CLASS BASED VIEWS: ##
########################

# READ                 ↓ VIEW mixin ↓
class ModuleListView(InstructorModuleMixin, ListView):
    template_name = 'manage/module/list.html'
    pass

# CREATE               ↓ EDIT mixin ↓
class ModuleCreateView(InstructorModuleEditMixin, CreateView):
    # template_name = 'manage/module/form.html'
    pass

# UPDATE               ↓ EDIT mixin ↓
class ModuleUpdateView(InstructorModuleEditMixin, UpdateView):
    pass


# DELETE               ↓ VIEW mixin ↓
class ModuleDeleteView(InstructorModuleMixin, DeleteView):
    template_name = 'manage/module/delete.html'


"""
Without Mixins, each (create, update, view, delete) class would look like this:

class ManageModuleListView(ListView):
    model = Module
    # template_name = 'courses/manage/course/list.html'
    
    # Retrieve just the modules created by the current user
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
"""
