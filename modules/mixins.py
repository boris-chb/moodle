from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from modules.models import Module


class InstructorMixin:
    """
    Returns a Queryset with Modules that belong to current user by overwriting <get_queryset()>.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(instructor=self.request.user)


class InstructorEditMixin:
    """
    Sets the current user as creator of the Module after submitting the module creation form.
    """

    def form_valid(self, form):
        # Sets the user as instructor during Module creation
        form.instance.instructor = self.request.user
        return super().form_valid(form)


class InstructorModuleMixin(InstructorMixin, LoginRequiredMixin, UserPassesTestMixin):
    model = Module
    fields = ['title', 'code', 'level', 'overview']
    # Redirect URL:
    success_url = reverse_lazy('modules:list')

    # Checks whether user is staff (Instructor)
    # Students will get 403 Access Denied
    def test_func(self):
        return self.request.user.is_staff


class InstructorModuleEditMixin(InstructorModuleMixin, InstructorEditMixin):
    """
    Combines InstructorModuleMixin and InstructorEditMixin mixins.
    InstructorModuleMixin - checks for staff permission.
    InstructorEditMixin - sets the user as module creator after submitting form.
    """
    template_name = 'manage/module/form.html'
    context_object_name = 'module'
