from abc import ABC

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, ChildProfile, Task, TaskProgress
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'username']
        extra_kwargs = {
            'username': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CreateTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(CreateTokenSerializer, cls).get_token(user)
        token['username'] = user.username
        return token


class ChildProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    parent = serializers.SlugRelatedField(slug_field='id', queryset=User.objects, required=True)

    class Meta:
        model = ChildProfile
        fields = ['name', 'parent']

    def create(self, validated_data):
        child = ChildProfile.objects.create(
            name=validated_data['name'],
            parent=validated_data['parent']
        )
        child.save()
        return child


class TaskProgressSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='id', queryset=ChildProfile.objects, required=True)
    task = serializers.SlugRelatedField(slug_field='id', queryset=Task.objects, required=True)

    class Meta:
        model = TaskProgress
        fields = ['user', 'task']

    def create(self, validated_data):
        task_progress = TaskProgress.objects.create(
            user=validated_data['user'],
            task=validated_data['task']
        )
        task_progress.save()
        return task_progress


class TaskUpgradeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='id', queryset=ChildProfile.objects, required=True)
    task = serializers.SlugRelatedField(slug_field='id', queryset=Task.objects, required=True)
    status = serializers.CharField(required=True)

    class Meta:
        model = TaskProgress
        fields = ['user', 'task', 'status']


class GetAllScoreSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    total_score = serializers.IntegerField()

    class Meta:
        model = ChildProfile
        fields = ['name', 'total_score']
