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
from django.urls import reverse_lazy

from .models import Module, Topic, Resource
from .mixins import InstructorEditMixin

from students.forms import ModuleEnrollForm


# A Django view is just a Python function that
# receives a web request and returns a web response.
# We'll be using Mixins for our Class Based Views

########################
###      MODULE       ##
########################


class ManageModuleListView(InstructorEditMixin, ListView):
    """
    A view for Instructors to manage Modules created by them
    """
    template_name = 'manage/module/list.html'


manage_module_list_view = ManageModuleListView.as_view()


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

    def get_queryset(self):
        """Search functionality."""
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            return qs.filter(title__icontains=q)
        return qs


module_list_view = ModuleListView.as_view()


module_list_view = ModuleListView.as_view()


class ModuleDetailView(DetailView):
    """
    Renders the view for Module information.
    get_context_data - includes enrollment form in the context for template rendering.
    """
    model = Module
    template_name = 'module/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = ModuleEnrollForm(
            # Set Module in the Enrollment Form
            # (this field is set automatically and hidden from the user)
            initial={'module': self.object}
        )
        return context


module_detail_view = ModuleDetailView.as_view()


<<<<<<< HEAD
class ModuleCreateView(SuccessMessageMixin, InstructorEditMixin, CreateView):
=======
class ModuleCreateView(SuccessMessageMixin, InstructorModuleEditMixin, CreateView):
>>>>>>> 7305a80f7f143fcaaa6765bd1292ddb068bcd3aa
    # template_name = 'manage/module/form.html'
    fields = ['code', 'title', 'level', 'overview']
    success_msg = "Module was created successully."


module_create_view = ModuleCreateView.as_view()


<<<<<<< HEAD
class ModuleUpdateView(InstructorEditMixin, UpdateView):
    success_msg = "Module was updated successully."
=======
module_create_view = ModuleCreateView.as_view()


class ModuleUpdateView(InstructorModuleEditMixin, UpdateView):
    pass
>>>>>>> 7305a80f7f143fcaaa6765bd1292ddb068bcd3aa


module_update_view = ModuleUpdateView.as_view()


<<<<<<< HEAD
class ModuleDeleteView(InstructorEditMixin, DeleteView):
    template_name = 'manage/module/delete.html'
    context_object_name = 'module'
    success_msg = "Module was deleted successully."
=======
class ModuleDeleteView(InstructorModuleMixin, DeleteView):
    template_name = 'manage/module/delete.html'
    context_object_name = 'module'
    success_message = "%(title)s was deleted successully."
>>>>>>> 7305a80f7f143fcaaa6765bd1292ddb068bcd3aa
    success_url = reverse_lazy("modules:manage_list")


module_delete_view = ModuleDeleteView.as_view()


########################
###      TOPIC        ##
########################


class TopicUpdateView(TemplateResponseMixin, View):
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
            return redirect('modules:list')
        context = {'module': self.module, 'formset': formset}
        # <render_to_response> is provided by TemplateResponseMixin
        return self.render_to_response(context)


topic_update_view = TopicUpdateView.as_view()

########################
###     RESOURCE      ##
########################


class ResourceListView(TemplateResponseMixin, View):
    template_name = 'manage/topic/resource_list.html'

    def get(self, request, topic_id):
        topic = get_object_or_404(
            Topic, id=topic_id, module__instructor=request.user)
        return self.render_to_response({'topic': topic})


resource_list_view = ResourceListView.as_view()


class ResourceCreateUpdateView(TemplateResponseMixin, View):
    topic = None
    model = None
    obj = None
    template_name = 'manage/resource/form.html'

    def get_model(self, model_name):
        """Checks whether the model is valid file type and obtain the class for given model. """
        if model_name in ['video', 'image', 'file']:
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
<<<<<<< HEAD
            return redirect('modules:resource_list', self.topic.id)
=======
            return redirect('modules:resource_list_view', self.topic.id)
>>>>>>> 7305a80f7f143fcaaa6765bd1292ddb068bcd3aa

        return self.render_to_response(context)


resource_create_view = ResourceCreateUpdateView.as_view()


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
<<<<<<< HEAD
        return redirect('modules:resource_list', topic.id)
=======
        return redirect('modules:resource_list_view', topic.id)
>>>>>>> 7305a80f7f143fcaaa6765bd1292ddb068bcd3aa


resource_delete_view = ResourceDeleteView.as_view()
