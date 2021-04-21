from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from modules.models import Module


class InstructorEditMixin(UserPassesTestMixin):
    """
    Reusable logic for Instructor actions over Modules.
    """
    model = Module
    fields = ['title', 'code', 'level', 'overview']
    template_name = 'manage/module/form.html'
    context_object_name = 'module'

    def form_valid(self, form):
        # Sets the user as instructor during Module creation
        form.instance.instructor = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        # Retrieves all Modules created by current User
        qs = super().get_queryset()
        return qs.filter(instructor=self.request.user)

    def test_func(self):
        # Test function for <UserPassesTestMixin>. Checks for Staff permission, otherwise 403
        return self.request.user.is_staff
