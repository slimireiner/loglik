import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import User, ChildProfile, TaskProgress, Task
from .serializers import (
    CreateTokenSerializer,
    ChildProfileSerializer,
    TaskProgressSerializer,
    TaskUpgradeSerializer,
    GetAllScoreSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer
from rest_framework import generics


# Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Login
class TokenCreate(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CreateTokenSerializer


# Add Child
class ChildAdd(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ChildProfile.objects.all()
    serializer_class = ChildProfileSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Add progress
class AddTask(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TaskProgress.objects.all()
    serializer_class = TaskProgressSerializer


# Change status task, add score
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_task(request):
    data = request.POST
    serializer = TaskUpgradeSerializer(data=data, many=True)
    if serializer.is_valid():
        task_progress = TaskProgress.objects.filter(user_id=data['user'], task_id=data['task']).first()
        if task_progress.status != 'done':
            task_progress.change_status(status=data['status'])
            return HttpResponse(task_progress)
        else:
            return HttpResponse('Points for the task have already been awarded!')


# Get score
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_scores(request, score_id: int):
    total_score = ChildProfile.objects.filter(id=score_id).first()
    task = TaskProgress.objects.filter(user=total_score.id)
    return HttpResponse(json.dumps({'name': total_score.name, 'total_score': total_score.total_score, }))


# Get all score
class ScoreList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ChildProfile.objects.all()
    serializer_class = GetAllScoreSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GetAllScoreSerializer(queryset, many=True)
        return Response(serializer.data)
