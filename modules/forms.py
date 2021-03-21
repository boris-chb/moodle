from django import forms
from django.forms.models import inlineformset_factory
from .models import Module, Topic

# Build a model formset dynamically for Topics related to certain Module
TopicFormSet = inlineformset_factory(Module, Topic, 
                                     fields=['title', 'description'],
                                     extra=1, can_delete=True)
