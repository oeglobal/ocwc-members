# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import CandidateAddView, CandidateEditView, CandidateView, ElectionListView, VoteView, VoteAddFormView
from .api import ElectionCandidatesListAPIView

urlpatterns = [
    url(r'^candidate/nominate/$', CandidateAddView.as_view(), name='candidate-add'),

    url(r'^candidate/edit/(?P<key>[\w|\W]+)/$',
        CandidateEditView.as_view(lookup_field='edit_link_key', lookup_url_kwarg='key'), name='candidate-edit'),
    url(r'^candidate/view/(?P<key>[\w|\W]+)/$',
        CandidateView.as_view(lookup_field='view_link_key', lookup_url_kwarg='key'), name='candidate-view'),

    url(r'^candidate/list/(?P<key>[\w|\W]+)/$',
        ElectionListView.as_view(lookup_field='view_nominations_key', lookup_url_kwarg='key'), name='candidate-list'),

    url(r'^api/candidate/list/(?P<key>[\w|\W]+)/$', ElectionCandidatesListAPIView.as_view(), name='api-candidate-list'),

    url(r'^vote/add/(?P<pk>\d+)/$', VoteAddFormView.as_view(), name='vote-add'),
    url(r'^vote/(?P<pk>\d+)/$', VoteView.as_view(), name='vote-view'),
]
