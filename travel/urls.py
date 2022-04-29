from django.urls import path
from . import views

app_name = "travel"

urlpatterns = [
		path("NewTravel/", views.Travelling, name="new-travel"),
		path("TravelPlans/", views.TravelPlans, name="travel-plan-list"),
		path("DeleteTravelPlan/<id>/", views.RemoveTravelPlan, name="remove-travel-plan"),
		path("UpdatePlan/<id>/", views.PlanUpdate, name="plan-update"),
]