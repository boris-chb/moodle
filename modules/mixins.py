from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from modules.models import Module


class InstructorEditMixin(UserPassesTestMixin):
    """
<<<<<<< HEAD
    Reusable logic for Instructor actions over Modules.
=======
    Returns a Queryset with Modules that belong to current user by overwriting <get_queryset()>.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(instructor=self.request.user)


class InstructorEditMixin:
    """
    Sets the current user as creator of the Module after submitting the module creation form.
>>>>>>> 7305a80f7f143fcaaa6765bd1292ddb068bcd3aa
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

<<<<<<< HEAD
=======
class InstructorModuleMixin(InstructorMixin, LoginRequiredMixin, UserPassesTestMixin):
    model = Module
    fields = ['title', 'code', 'level', 'overview']
    # Redirect URL:
    success_url = reverse_lazy('modules:list')

    # Checks whether user is staff (Instructor)
    # Students will get 403 Access Denied
>>>>>>> 7305a80f7f143fcaaa6765bd1292ddb068bcd3aa
    def test_func(self):
        # Test function for <UserPassesTestMixin>. Checks for Staff permission, otherwise 403
        return self.request.user.is_staff
