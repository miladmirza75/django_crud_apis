# api/serializers.py

from rest_framework import serializers
from django.apps import apps

def get_serializer_for_model(model):
    model_name = model._meta.model_name
    app_label = model._meta.app_label
    model_class = apps.get_model(app_label, model_name)

    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'

    return Serializer
