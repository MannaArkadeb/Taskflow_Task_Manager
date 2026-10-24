from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Task, User
from .serializers import ProjectSerializer, TaskSerializer, UserSerializer, ChangePasswordSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny] # Anyone can register

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'id': request.user.id, 'role': request.user.role})

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Project.objects.all()

    def destroy(self, request, *args, **kwargs):
        # Prevent Team Members from deleting projects
        if request.user.role != 'Manager':
            return Response(
                {"error": "Only Managers can delete projects."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'deadline', 'assigned_to']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Manager':
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)

    def create(self, request, *args, **kwargs):
        if request.user.role != 'Manager':
            return Response(
                {"error": "Only Managers can create and assign tasks."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    # NEW: Automatically set assigned_by to the Manager making the request
    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    # NEW: Block members from updating assignments
    def update(self, request, *args, **kwargs):
        if request.user.role != 'Manager':
            if 'assigned_to' in request.data or 'assigned_by' in request.data:
                return Response({"error": "Members cannot change assignments."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Prevent Team Members from deleting tasks
        if request.user.role != 'Manager':
            return Response(
                {"error": "Only Managers can delete tasks."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            # Verify the old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"error": "Wrong old password."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Hash and save the new password
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)