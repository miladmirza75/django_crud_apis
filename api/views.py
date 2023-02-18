# api/views.py

from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    ListAPIView,
    DestroyAPIView,
)
from django.shortcuts import get_object_or_404
from .serializers import get_serializer_for_model
from .filters import get_filter_class_for_model

class CRUDAPIViewMixin:
    model = None

    def get_serializer_class(self):
        return get_serializer_for_model(self.model)

    def get_queryset(self):
        return self.model.objects.all()

class CreateModelMixin(CRUDAPIViewMixin):
    def perform_create(self, serializer):
        serializer.save()

class RetrieveModelMixin(CRUDAPIViewMixin):
    def get_object(self):
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        return get_object_or_404(queryset, **{self.lookup_field: lookup_value})

class UpdateModelMixin(CRUDAPIViewMixin):
    def perform_update(self, serializer):
        serializer.save()

class DestroyModelMixin(CRUDAPIViewMixin):
    def perform_destroy(self, instance):
        instance.delete()

class ListModelMixin(CRUDAPIViewMixin):
    filter_class = None

    def get_filter_class(self):
        return get_filter_class_for_model(self.model)

    def filter_queryset(self, queryset):
        filter_class = self.get_filter_class()
        if filter_class:
            filter_instance = filter_class(
                self.request.GET,
                queryset=queryset,
                request=self.request,
            )
            return filter_instance.qs
        return queryset

class CreateModelAPIView(CreateModelMixin, CreateAPIView):
    pass

class RetrieveModelAPIView(RetrieveModelMixin, RetrieveAPIView):
    pass

class UpdateModelAPIView(UpdateModelMixin, RetrieveModelMixin, UpdateAPIView):
    pass

class ListModelAPIView(ListModelMixin, ListAPIView):
    pass

class DestroyModelAPIView(DestroyModelMixin, RetrieveModelMixin, DestroyAPIView):
    pass

def addurls(model):
    views = {
        'list': ListModelAPIView,
        'create': CreateModelAPIView,
        'retrieve': RetrieveModelAPIView,
        'update': UpdateModelAPIView,
        'destroy': DestroyModelAPIView,
    }

    urlpatterns = []

    for key, view_class in views.items():
        view_func = view_class.as_view(model=model)
        pattern = r'^{}/{}$'.format(model, key)
        urlpatterns.append(url(pattern, view_func, name='{}_{}'.format(model, key)))

    return urlpatterns
