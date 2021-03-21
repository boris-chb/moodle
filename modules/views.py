from django.urls import reverse_lazy
from django.forms.models import modelform_factory
from .forms import TopicFormSet
from django.apps import apps
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View # Render templates => HTTP response
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from .models import Module, Topic, Resource

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
    context_object_name = 'module'


                        ########################
                        ###                   ##
                        ### CLASS BASED VIEWS ##
                        ###                   ##
                        ########################


########################
###                   ##
###     MODULES       ##
###                   ##
########################

# READ                 ↓ VIEW mixin ↓
class ModuleListView(InstructorModuleMixin, ListView):
    template_name = 'manage/module/list.html'
    context_object_name = 'modules'

# CREATE               ↓ EDIT mixin ↓
class ModuleCreateView(SuccessMessageMixin, InstructorModuleEditMixin, CreateView):
    # template_name = 'manage/module/form.html'
    fields = '__all__'
    success_message = "%(title)s was created successully."

# UPDATE               ↓ EDIT mixin ↓
class ModuleUpdateView(InstructorModuleEditMixin, UpdateView):
    pass


# DELETE               ↓ VIEW mixin ↓
class ModuleDeleteView(InstructorModuleMixin, DeleteView):
    template_name = 'manage/module/delete.html'
    context_object_name = 'module'

########################
###                   ##
###      TOPIC        ##
###                   ##
########################

class ModuleTopicUpdateView(TemplateResponseMixin, View):
  """
    1. Build a ModuleFormSet instance using POST data.
    2. Validate the forms.
    3. If the formset is valid, <.save()> is being called and changes are submitted to the database. Otherwise, render the template to display errors.
  """
  template_name = 'manage/topic/formset.html'
  module = None

  def get_formset(self, data=None):
    # To avoid repeating formset creation
    return TopicFormSet(instance=self.module, data=data)
  
  def dispatch(self, request, pk):
    """
      Provided by <View> Class.
      Retrieves the Module for given <id> that belongs to current <request.user>.
      Data is saved in <module> attribute of the view.
    """
    self.module = get_object_or_404(Module, id=pk, instructor=request.user)
    return super().dispatch(request, pk)
  
  def get(self, request, *args, **kwargs):
    formset = self.get_formset()
    context = {'module': self.module, 'formset': formset}
    return self.render_to_response(context)
  
  def post(self, request, *args, **kwargs):
    formset = self.get_formset(data=request.POST)
    if formset.is_valid():
      formset.save()
      return redirect('module_list')
    context = {'module': self.module, 'formset': formset}
    # Provided by TemplateResponseMixin ↓
    return self.render_to_response(context)



########################
###                   ##
###     RESOURCE      ##
###                   ##
########################

class TopicResourceListView(TemplateResponseMixin, View):
  template_name = 'manage/topic/resource_list.html'
  context_object_name = 'topics'

  def get(self, request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, module__instructor=request.user)
    return self.render_to_response({'topic': topic})

class ResourceCreateUpdateView(TemplateResponseMixin, View):
  topic = None
  model = None
  obj = None
  template_name = 'manage/resource/form.html'
  context_object_name = 'resource'

  def get_model(self, model_name):
    """ Checks whether the model is Text/Video/Image/File and obtain the class for given model. """
    if model_name in ['text', 'video', 'image', 'file']:
      return apps.get_model(app_label='modules', model_name=model_name)
    return None
  
  def get_form(self, model, *args, **kwargs):
    """
      Creates a dynamic form and excludes certain common fields,
      instead of including fields for each model in particular.
      (What is left will be included automatically)
    """
    Form = modelform_factory(model, exclude=['instructor', 'created', 'updated'])
    return Form(*args, **kwargs)

  def dispatch(self, request, topic_id, model_name, id=None):
    """
      Receives the corresponding URL parrameters.
      Stores the Model (text/file/video/image) + Module + Content as a single Class.
    """
    self.topic = get_object_or_404(Topic, id=topic_id, module__instructor=request.user)
    self.model = self.get_model(model_name) # Model name of content to be created/updated
    if id: # then Update the model:
      self.obj = get_object_or_404(self.model, id=id, creator=request.user)
    # else Create a new one:
    return super().dispatch(request, topic_id, model_name, id)

  def get(self, request, topic_id, model_name, id=None):
    """
      Invoked when a GET request is being passed to build the model form.
      <self.obj> is None if no ID is provided, i.e. no form is created.
    """
    form = self.get_form(self.model, instance=self.obj)
    context = {'form': form, 'object': self.obj}
    return self.render_to_response(context)

  def post(self, request, topic_id, model_name, id=None):
    form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)
    context = {'form': form, 'object': self.obj}

    if form.is_valid():
      obj = form.save(commit=False)
      obj.instructor = request.user
      obj.save()
      if not id:
        # New Resource
        Resource.objects.create(topic=self.topic, item=obj)
      return redirect('module_content_list', self.topic.id)
    
    return self.render_to_response(context)

class ContentDeleteView(View):
  
  def post(self, request, id):
    """
      Retrieves the Resource object with the given ID.

    """
    resource = get_object_or_404(Resource, id=id, topic__module__instructor=request.user)
    topic = resource.topic
    # Deletes the File object
    resource.item.delete()
    # Deletes the Resource object
    resource.delete()
    return redirect('topic_resource_list', topic.id)


############
## TO DO: ##
############



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
