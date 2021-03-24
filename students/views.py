from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import CustomUserCreationForm
from .forms import ModuleEnrollForm
from .mixins import StudentModuleMixin
from modules.models import Module, Topic


class StudentRegistrationView(CreateView):
    template_name = 'students/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('student_module_list')

    def form_valid(self, form):
        """
        Authenticates the student after they register.
        """
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


class StudentEnrollModuleView(LoginRequiredMixin, FormView):
    """
    Handles Student enrollment for individual Modules.
    Only logged-in users can access the view due to LoginRequiredMixin.
    Form submission is handled by FormView.
    """
    module = None
    form_class = ModuleEnrollForm

    def form_valid(self, form):
        # Get the Module from the form data
        self.module = form.cleaned_data['module']
        # Add the user to the set of enrolled students
        self.module.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        # URL to redirect student to in case of successfull enrollment
        return reverse_lazy('module_list')

class StudentModuleListView(LoginRequiredMixin, StudentModuleMixin, ListView):
  """
  A list view for Students to see Modules they're enrolled in.
  """
  template_name = 'student/module/list.html'
  context_object_name = 'modules'



class StudentModuleDetailView(StudentModuleMixin, DetailView):
  template_name = 'student/module/detail.html'
  # context_object_name = 'modules'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    module = self.get_object()
    if 'topic_id' in self.kwargs:
      # Get the topic
      context['topic'] = module.topics.get(id=self.kwargs['topic_id'])
    else:
      # Get the first topic
      context['topic'] = module.topics.all()[0]
    return context

# class StudentTopicDetailView(StudentTopicMixins, DetailView):
#   template_name = 'student/topic/detail.html'
#   model = Topic
#   context_object_name = 'topics'
