from django.conf.urls import url
from .views import LocationListCreateAPIHandler

# API endpoints
urlpatterns = [
    url(r'^locations$',
        LocationListCreateAPIHandler.as_view(),
        name='locations-list'),

    # url(r'^clipboards/(?P<pk>[0-9]+)$',
    #     views.ClipboardDetail.as_view(),
    #     name='clipboard-detail'),

    # url(r'^clipboards/(?P<pk>[0-9]+)/snippets$',
    #     views.ClipboardSnippetList.as_view(),
    #     name='clipboard-snippets-list'),
]
