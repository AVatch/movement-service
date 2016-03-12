from django.conf.urls import url
from .views import LocationListCreateAPIHandler, LocationRevealAPIHandler

# API endpoints
urlpatterns = [
    url(r'^locations$',
        LocationListCreateAPIHandler.as_view(),
        name='locations-list'),

    url(r'^locations/(?P<pk>[0-9]+)/reveal',
        LocationRevealAPIHandler.as_view(),
        name='location-reveal'),

    # url(r'^clipboards/(?P<pk>[0-9]+)/snippets$',
    #     views.ClipboardSnippetList.as_view(),
    #     name='clipboard-snippets-list'),
]
