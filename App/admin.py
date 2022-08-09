from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    pass


class ChildProfileAdmin(admin.ModelAdmin):
    pass


class TaskAdmin(admin.ModelAdmin):
    pass


class TaskProgressAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(ChildProfile, ChildProfileAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskProgress, TaskProgressAdmin)





