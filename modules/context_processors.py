from .models import Module

def nav_list(request):
    links = Module.objects.all()
    return dict(links=links)