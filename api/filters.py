# api/filters.py

from django_filters import rest_framework as filters
from django.apps import apps

def get_filter_class_for_model(model):
    model_name = model._meta.model_name
    app_label = model._meta.app_label
    model_class = apps.get_model(app_label, model_name)

    class FilterSet(filters.FilterSet):
        class Meta:
            model = model_class
            fields = '__all__'

    return FilterSet
