from celery import shared_task
from django.shortcuts import get_object_or_404
from .models import TravelDetail
from .views import RemoveTravelPlanWithoutRequest
from django.utils import timezone
from accounts.models import User
from django.core.mail import send_mail
import json

from django.contrib.auth import get_user_model
User = get_user_model()

@shared_task(bind=True)
def sample(self):
	print("Hello")


@shared_task(bind=True)
def TravelNow(self, id):

	time_now = timezone.now()
	obj = get_object_or_404(TravelDetail, id=id)
	sub = obj.subject
	tim = obj.date
	obj2 = get_object_or_404(User, username = obj.user)
	objEmail = obj2.email
	if time_now < tim:
		return
	subject = f'{sub}'
	from_email = 'simulations.ai@gmail.com'
	user_email = [objEmail,]
	try:
		new_msg = f'{obj.message}'
		send_mail(subject, new_msg, from_email, user_email, fail_silently=False)

	except BadHeaderError:
		return HttpResponse('Invalid header found.')

	RemoveTravelPlanWithoutRequest(id)






	# 8109120685