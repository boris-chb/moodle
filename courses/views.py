from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse_lazy

from courses.models import Course


# # # # # # # # # #
# # M I X I N S # #
# # # # # # # # # #
class AuthorMixin:
    """
    Mixin used to get the base QuerySet and filter the objects by the 'author' attribute (field) to retrieve
    objects that belong to the current user (request.user).
    Can be used for views that interact with any model that contains an 'author' attribute.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class AuthorEditMixin:
    """
    Implements the form_valid method (used by views that use ModelFormMixin).
    Example: Views with forms or Model forms such as CreateView and UpdateView.
    form_valid is executed after submitted form passes validation.
    """

    def form_valid(self, form):
        # set the current user as author of object that is created/modified
        form.instance.author = self.request.user
        return super().form_valid(form)


class AuthorCourseMixin(AuthorMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course  # used by all views for QuerySets
    fields = [
        "subject",
        "title",
        "slug",
        "overview",
    ]  # model fields used to build the form

    # redirect after successful form submission
    success_url = reverse_lazy("manage_course_list")


class AuthorCourseEditMixin(AuthorCourseMixin, AuthorEditMixin):
    template_name = "courses/manage/course/form.html"


# # # # # # # # #
# # V I E W S # #
# # # # # # # # #


# permission_required - used by PermissionRequiredMixin to check if
#       the user accessing the view has necessary permissions
class ManageCourseListView(AuthorCourseMixin, ListView):
    template_name = "courses/manage/course/list.html"
    permission_required = "courses.view_course"


class CreateCourseView(AuthorCourseEditMixin, CreateView):
    permission_required = "courses.add_course"


class UpdateCourseView(AuthorCourseEditMixin, UpdateView):
    permission_required = "courses.change_course"


class DeleteCourseView(AuthorCourseMixin, DeleteView):
    template_name = "courses/manage/course/delete.html"
    permission_required = "courses.delete_course"
