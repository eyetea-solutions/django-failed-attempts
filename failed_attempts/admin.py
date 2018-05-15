from django.contrib import admin
from failed_attempts.models import FailedAttempt


class AdminFailedAttempt (admin.ModelAdmin):
    list_display = ('username', 'IP', 'failures', 'timestamp', 'blocked')
    search_fields = ('username', 'IP', )


admin.site.register(FailedAttempt, AdminFailedAttempt)
