# -*- coding: utf-8 -*-
from rest_framework import generics

from .models import Candidate, Election
from .serializers import CandidatePublicSerializer

class ElectionCandidatesListAPIView(generics.ListAPIView):
	model = Candidate
	serializer_class = CandidatePublicSerializer

	def get_queryset(self):
		view_nominations_key = self.kwargs.pop('key')
		return Election.objects.get(view_nominations_key=view_nominations_key).candidate_set.filter(vetted=True).order_by('candidate_last_name')
