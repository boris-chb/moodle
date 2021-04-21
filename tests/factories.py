from django.template.defaultfilters import slugify

import factory
import factory.fuzzy

from modules.models import Module


class ModuleFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText()
    code = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    overview = factory.Faker(
        'paragraph', nb_sentences=4, variable_nb_sentences=True)
    level = factory.fuzzy.FuzzyChoice(
        x[0] for x in Module.LEVEL_CHOICES
    )

    class Meta:
        model = Module
