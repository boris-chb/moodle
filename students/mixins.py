from modules.models import Module, Topic

class StudentModuleMixin:
  model = Module

  def get_queryset(self):
    qs = super().get_queryset()
    return qs.filter(students__in=[self.request.user])

# class StudentTopicMixins:
#   model = Topic

#   def get_queryset(self):
#     qs = super().get_queryset().filter
#     return qs.filter(topics__in=Module.objects.)