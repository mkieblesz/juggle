from datetime import date

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from juggle.constants import MAX_NUMBER_OF_APPLICATIONS_PER_JOB_PER_DAY
from juggle.models import Business, Job, JobApplication, Professional
from juggle.serializers import JobApplicationCreateSerializer, JobApplicationSerializer


class EntitySearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get("query", None)

        # FIRST VERSION
        entities = (
            [
                {"type": "professional", "full_name": p.full_name}
                for p in Professional.objects.all()
                if query is None or query in p.full_name
            ]
            + [
                {"type": "business", "company_name": b.company_name}
                for b in Business.objects.all()
                if query is None or query in b.company_name
            ]
            + [
                {"type": "job", "title": j.title}
                for j in Job.objects.all()
                if query is None or query in j.title
            ]
        )

        # # SECOND VERSION - union requres same amount of columns
        # professional_qs = (
        #     Professional.objects.annotate(type=Value("professional"))
        #     .annotate(full_name=Concat("user__first_name", Value(" "), "user__last_name"))
        #     .filter(user__last_name__icontains=query)
        #     .values("type", "full_name")
        # )

        # business_qs = (
        #     Business.objects.annotate(type=Value("business"))
        #     .filter(company_name__icontains=query)
        #     .values("type", "company_name")
        # )

        # job_qs = (
        #     Job.objects.annotate(type=Value("job"))
        #     .filter(title__icontains=query)
        #     .values("type", "title")
        # )

        # entities = professional_qs.union(business_qs, job_qs)
        # print(list(entities))

        return Response(entities, status=status.HTTP_200_OK)


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    filterset_fields = ('job',)

    def get_serializer_class(self):
        if self.action == "create":
            return JobApplicationCreateSerializer

        return JobApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        job = serializer.validated_data["job"]

        if (
            JobApplication.objects.filter(job=job, date=date.today()).count()
            >= MAX_NUMBER_OF_APPLICATIONS_PER_JOB_PER_DAY
        ):
            return Response(
                {"message": "You can't apply for this job today. Try tomorrow"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
