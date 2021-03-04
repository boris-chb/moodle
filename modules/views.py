from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Module

# We'll be using Mixins for our Class Based Views


class InstructorMixin:
    """
        Overriding a Manager’s base QuerySet - get_queryset().
        Used to retrieve objects from database.
        We'll filter just the objects that belong to current user.
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


class InstructorModuleMixin(InstructorMixin, LoginRequiredMixin, UserPassesTestMixin):
    model = Module
    fields = ['title', 'slug', 'level', 'overview']
    # Redirect URL:
    success_url = reverse_lazy('module_list')

    def test_func(self):
      return self.request.user.is_staff



class InstructorModuleEditMixin(InstructorModuleMixin, InstructorEditMixin):
    template_name = 'manage/module/form.html'
    pass


# CREATE
class ModuleCreateView(InstructorModuleMixin, CreateView):
    template_name = 'manage/module/form.html'


# READ
class ModuleListView(InstructorModuleMixin, ListView):
    template_name = 'manage/module/list.html'
    pass


# UPDATE
class ModuleUpdateView(InstructorModuleMixin, UpdateView):
    pass


# DELETE
class ModuleDeleteView(InstructorModuleMixin, DeleteView):
    # template_name = 'modules/manage/delete.html'
    pass


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
