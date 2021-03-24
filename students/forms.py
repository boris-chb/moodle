from django import forms
from modules.models import Module


class ModuleEnrollForm(forms.Form):
    """
    Form to enroll Students to Modules.
    Contains <module> field to choose from all Modules to enroll.
    This field is hidden from the student, as it will be set automatically.
    """
    module = forms.ModelChoiceField(queryset=Module.objects.all(),
                                    widget=forms.HiddenInput)
