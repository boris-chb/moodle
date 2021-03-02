from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, CustomEmailDomainUserCreationForm


class SignUpView(CreateView):
    form_class = CustomEmailDomainUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
