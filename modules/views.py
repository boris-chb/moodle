from django.db.models import Count
from django.forms.models import modelform_factory
from .forms import TopicFormSet
from django.apps import apps
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404

from .models import Module, Topic, Resource
from .mixins import InstructorMixin, InstructorEditMixin, InstructorModuleMixin, InstructorModuleEditMixin

from students.forms import ModuleEnrollForm
"""
A Django view is just a Python function that 
breceives a web request and returns a web response. 
We'll be using Mixins for our Class Based Views
"""

########################
###      MODULE       ##
########################


class ManageModuleListView(InstructorModuleMixin, ListView):
    """
    A view for Instructors to manage Modules created by them
    """
    template_name = 'manage/module/list.html'
    context_object_name = 'modules'


class ModuleListView(TemplateResponseMixin, View):
    """
    A view to list all modules.
    Inherits from TemplateResponseMixins to return a HTTP Response via <render_to_response> method.
    """
    model = Module
    template_name = 'module/list.html'

    def get(self, request):
        """
        Retrieve all available Modules along with total number of Topics for each Module.
        Returns an HTTP response.
        """
        modules = Module.objects.annotate(total_topics=Count('topics'))
        return self.render_to_response({'modules': modules})


class ModuleDetailView(DetailView):
    """
    Renders the view for Module information.
    get_context_data - includes enrollment form in the context for template rendering.
    """
    model = Module
    template_name = 'module/detail.html'
    context_object_name = 'module'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = ModuleEnrollForm(
            # Set Module in the Enrollment Form
            # (this field is set automatically and hidden from the user)
            initial={'module': self.object}
        )
        return context


class ModuleCreateView(SuccessMessageMixin, InstructorModuleEditMixin, CreateView):
    # template_name = 'manage/module/form.html'
    fields = ['code', 'title', 'slug', 'level', 'overview']
    success_message = "%(title)s was created successully."


class ModuleUpdateView(InstructorModuleEditMixin, UpdateView):
    pass


class ModuleDeleteView(InstructorModuleMixin, DeleteView):
    template_name = 'manage/module/delete.html'
    context_object_name = 'module'


########################
###      TOPIC        ##
########################


class ModuleTopicUpdateView(TemplateResponseMixin, View):
    """
          1. Build a ModuleFormSet instance using POST data.
          2. Validate the forms.
          3. If the formset is valid, <.save()> is being called and changes are submitted to the database.
            Otherwise, render the template to display errors.
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
        # <render_to_response> is provided by TemplateResponseMixin
        return self.render_to_response(context)


########################
###     RESOURCE      ##
########################

class TopicResourceListView(TemplateResponseMixin, View):
    template_name = 'manage/topic/resource_list.html'
    context_object_name = 'topics'

    def get(self, request, topic_id):
        topic = get_object_or_404(
            Topic, id=topic_id, module__instructor=request.user)
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
        Form = modelform_factory(
            model, exclude=['creator', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, topic_id, model_name, id=None):
        """
          Receives the corresponding URL parrameters.
          Stores the Model (text/file/video/image) + Module + Content as a single Class.
        """
        self.topic = get_object_or_404(
            Topic, id=topic_id, module__instructor=request.user)
        # Model name of content to be created/updated
        self.model = self.get_model(model_name)
        if id:  # then Update the model:
            self.obj = get_object_or_404(
                self.model, id=id, creator=request.user)
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
        form = self.get_form(self.model, instance=self.obj,
                             data=request.POST, files=request.FILES)
        context = {'form': form, 'object': self.obj}

        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            if not id:
                # New Resource
                Resource.objects.create(topic=self.topic, item=obj)
            return redirect('topic_resource_list', self.topic.id)

        return self.render_to_response(context)


class ResourceDeleteView(View):

    def post(self, request, id):
        """
          Retrieves the Resource object with the given ID.

        """
        resource = get_object_or_404(
            Resource, id=id, topic__module__instructor=request.user)
        topic = resource.topic
        # Deletes the File object
        resource.item.delete()
        # Deletes the Resource object
        resource.delete()
        return redirect('topic_resource_list', topic.id)


############
## TO DO: ##
############
