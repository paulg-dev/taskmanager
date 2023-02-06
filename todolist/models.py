from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.

def return_date_time():
    now = timezone.now()
    return now + timedelta(days=1)

class ToDoItem(models.Model):
	# CharField = String value
	# DateTimeField = Datetime datatype
	task_name = models.CharField(max_length = 50)
	description = models.CharField(max_length = 200)
	status = models.CharField(max_length = 50, default = "Pending")
	date_created = models.DateTimeField("Date Created")
	# Adding a user_id to the ToDoItem table, which is a foreign key connected to the Users table.
	user = models.ForeignKey(User, on_delete=models.CASCADE, default="")


class EventItem(models.Model):
	event_name = models.CharField(max_length = 50)
	description = models.CharField(max_length = 200)
	status = models.CharField(max_length = 50, default = "Pending")
	event_date = models.DateField(default=return_date_time)
	user = models.ForeignKey(User, on_delete=models.CASCADE, default="")