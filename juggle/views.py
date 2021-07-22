from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from juggle.models import Job, JobApplication
from juggle.serializers import EntitySerializer, JobSerializer, JobApplicationSerializer



# List all entities listed on the website
# Search for jobs, professionals
class EntitySearch(APIView):
    def get(self, request, format=None):
        serializer = EntitySerializer()
        return Response(serializer.data)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# Allow to list all applicants for any job
# Allow professional to apply for any job
# Limit to 5 applications per job per day
class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
