from django.urls import path
from .views import my_submissions, submit_record, delete_my_record

urlpatterns = [
    path("my/submissions", my_submissions),
    path("my/submissions/<int:record_id>", delete_my_record),
    path("my/submissions/submit", submit_record),
]
