from django.contrib import admin

from .models import Department,Assessment,Question,Option,AssessmentAttempt,UserResponse

admin.site.register(Department)
admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(AssessmentAttempt)
admin.site.register(UserResponse)

# Register your models here.
