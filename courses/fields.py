from typing import List, Union
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    """
    Custom field to specify the order of objects within a queryset based on the value of this field.

    Parameters:
        for_fields (list): A list of field names for which to apply the ordering.
    """

    def __init__(self, for_fields: Union[List[str], None] = None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        # before saving the field to the database
        # check whether a value exists for this field in model instance
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                # retrieve all objects for field's model
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    qs = qs.filter(**query)
                # get the order of the last item and increment order
                last_item = qs.latest(self.attname)
                value = last_item.order + 1  # type: ignore
            except ObjectDoesNotExist:
                # assume it's the first object
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            # value exists, use it for the current field
            return super().pre_save(model_instance, add)
