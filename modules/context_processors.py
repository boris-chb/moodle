from .models import Module

def nav_list(request):
    modules = Module.objects.all()
    return dict(modules=modules)