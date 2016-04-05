from django.conf.urls import url
from .views import AccountCreationAPIHandler, CohortListCreateAPIHandler

# API endpoints
urlpatterns = [
    url(r'^cohorts$',
        CohortListCreateAPIHandler.as_view(),
        name='cohorts-list'),
    
    url(r'^accounts$',
        AccountCreationAPIHandler.as_view(),
        name='accounts-create'),

    # url(r'^clipboards/(?P<pk>[0-9]+)$',
    #     views.ClipboardDetail.as_view(),
    #     name='clipboard-detail'),

    # url(r'^clipboards/(?P<pk>[0-9]+)/snippets$',
    #     views.ClipboardSnippetList.as_view(),
    #     name='clipboard-snippets-list'),
]
