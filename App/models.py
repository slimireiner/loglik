from django.contrib.auth.models import AbstractUser
from django.db import models


# This is an abstract User model
class User(AbstractUser):
    class Meta:
        db_table = 'accounts_users'


# This is a model of the children's profile
class ChildProfile(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child')
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def add_score(self, score: int) -> None:
        self.total_score += score
        self.save(update_fields=['total_score'])


# This is the Tasks model
class Task(models.Model):
    name = models.CharField(max_length=50)
    score = models.IntegerField(default=5)

    def __str__(self):
        return self.name


# This is a model for performing Tasks
class TaskProgress(models.Model):
    statuses = (
        ('in_progress', 'In progress'),
        ('done', 'Done')

    )
    user = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=statuses, default=statuses[0][0])

    def __str__(self):
        return self.status

    def change_status(self, status: str = statuses[0][0]) -> None:
        self.status = status
        if status == self.statuses[1][0]:
            self.user.add_score(self.task.score)
        self.save(update_fields=['status'])
