from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.

class TravelDetail(models.Model):
	id = models.IntegerField(primary_key=True)
	user = models.ForeignKey(User, related_name="TravelDetails", on_delete=models.CASCADE)
	subject = models.CharField(max_length=256)
	message = models.TextField()
	date = models.DateTimeField("Date(dd/mm/yyyy) Time(hh:mm)", default = timezone.now())
	created_at = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.subject

	class Meta:
		ordering = ["-created_at"]
