from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user).order_by('-created_at')

        status_param = self.request.query_params.get('status')
        search = self.request.query_params.get('search')

        if status_param:
            if status_param.upper() == 'COMPLETED':
                queryset = queryset.filter(is_completed=True)
            elif status_param.upper() == 'PENDING':
                queryset = queryset.filter(is_completed=False)

        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(user=request.user)

        response_serializer = TaskSerializer(task)
        return Response(
            {
                "message": "Task created successfully.",
                "data": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class TaskDetailView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class MarkTaskCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if task.is_completed:
            return Response(
                {"message": "Task is already completed."},
                status=status.HTTP_200_OK
            )

        task.is_completed = True
        task.status = 'COMPLETED'
        task.completed_at = timezone.now()
        task.save()

        return Response(
            {
                "message": "Task marked as completed successfully.",
                "data": TaskSerializer(task).data
            },
            status=status.HTTP_200_OK
        )


class TaskDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        self.perform_destroy(task)
        return Response(
            {"message": "Task deleted successfully."},
            status=status.HTTP_200_OK
        )