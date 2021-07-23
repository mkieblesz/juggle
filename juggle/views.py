from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from juggle.models import Job, JobApplication
from juggle.serializers import JobSerializer, JobApplicationSerializer


class EntitySearch(APIView):
    def get(self, request, format=None):
        return Response([])


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
