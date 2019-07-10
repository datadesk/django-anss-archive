import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from anss.models import Feed, FeedEarthquake
from django.views.generic import TemplateView


class BaseJsonView(TemplateView):

    def to_json(self, content, **response_kwargs):
        return HttpResponse(
            content,
            content_type='application/json',
            **response_kwargs
        )


class LatestFeedView(BaseJsonView):

    def get_context_data(self, **kwargs):
        return Feed.objects.latest()

    def render_to_response(self, context, **response_kwargs):
        f = json.load(context.content)
        d = json.dumps(f, indent=4)
        return self.to_json(d)


class FeedListView(BaseJsonView):

    def get_context_data(self, **kwargs):
        return Feed.objects.all()[:100]

    def render_to_response(self, context, **response_kwargs):
        object_list = serializers.serialize('json', context, indent=4)
        return self.to_json(object_list)
