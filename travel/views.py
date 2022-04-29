from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TravelForm
from .models import TravelDetail
from accounts.models import User

from django_celery_beat.models import CrontabSchedule,PeriodicTask, PeriodicTasks, IntervalSchedule
import json

from django.contrib.auth import get_user_model
User = get_user_model()

from datetime import datetime
from django.utils import timezone
from django.contrib import messages


def generate_schedule(id, interval):
	print("\n\n reached here \n Lets schedule you travel \n")
	print(id)
	print("\n")
	print(interval)
	print("\n")
	schedule, created = IntervalSchedule.objects.get_or_create(
		every=interval,
		period=IntervalSchedule.MINUTES)

	name = str(id)
	task = PeriodicTask.objects.create(
		interval=schedule,
		name="Travel"+name,
		task='travel.tasks.TravelNow',
		args=json.dumps([id])
		)

	print("\n Task generated \n")
	return


def get_time_diff(interval):
	print("\n interval " + str(interval) + "\n time now: ")
	time_now = timezone.now()
	print(time_now)
	duration = interval-time_now
	print("\n Duration: " + str(duration)+"\n")
	duration_in_minutes = duration.total_seconds()
	return int(duration_in_minutes/60)


def ReadyToTravel(request, id):
	obj = get_object_or_404(TravelDetail, id = id)
	form = TravelForm(request.POST or None, instance = obj)

	if form.is_valid():
		form.save()
		interval = get_time_diff(obj.date)
		print("\n\n final interval")
		print(interval)
		print("\nCurrent Id : ")
		print(obj.id)
		# print()
		# generate_schedule(obj.id, interval)

		return redirect('/')

	return render(request, 'travel/NewTravel.html', {'form':form})


# Create your views here.
@login_required
def Travelling(request):
	if request.method == 'POST':
		form = TravelForm(request.POST)

		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()

			interval = get_time_diff(obj.date)
			print("\n\n")
			print(interval)
			print("\nCurrent Id : ")
			obj2 = TravelDetail.objects.get(subject = form.cleaned_data['subject'])
			print(obj2.id)
			# print()
			generate_schedule(obj2.id, interval)

			messages.success(request, "You are about to Travel in the future ahead in time!")
			# form.save()

			return redirect('/')

	else:
		form = TravelForm()

	return render(request, 'travel/NewTravel.html', {'form':form})


@login_required
def TravelPlans(request):
	plans = TravelDetail.objects.filter(user=request.user)
	return render(request, "travel/ListTravelPlans.html", {'plans':plans})

def delete_periodic_task(id):
    name = str(id)
    name="Travel"+name
    obj1 = PeriodicTask.objects.filter(name = name).exists()
    if obj1:
        obj = PeriodicTask.objects.get(name = name)
        print("\n periodic task exists and deleted \n")
        obj.delete()
    else:
        print("\n Periodic doesn't exists \n")
    return 


@login_required
def RemoveTravelPlan(request, id):
	obj = get_object_or_404(TravelDetail, id=id)
	obj.delete()
	delete_periodic_task(id)
	return redirect('travel:travel-plan-list')

def RemoveTravelPlanWithoutRequest(id):
	obj = get_object_or_404(TravelDetail, id=id)
	obj.delete()
	delete_periodic_task(id)
	return

@login_required
def PlanUpdate(request, id):
	obj = get_object_or_404(TravelDetail, id = id)
	form = TravelForm(request.POST or None, instance = obj)

	if form.is_valid():
		form.save()
		return redirect('travel:travel-plan-list')

	return render(request, 'travel/PlanUpdate.html', {'form':form})






# --------------------------------------------
# For Help
# --------------------------------------------

# One approach is to filter the ToDo items by the currently logged in user:

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render

# from your_app.models import ToDo

# @login_required
# def todos_for_user(request):
#     todos = ToDo.objects.filter(user=request.user)
#     return render(request, 'todos/index.html', {'todos' : todos})

# This locks down the view for authenticated users only, and filtering by the logged in user 
# from the request, another user, even if logged in, can't access another user's ToDo records. 
