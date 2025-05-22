from .views import EventListCreateView, EventDetailView, PurchaseTicketView, UserTicketsView
from django.urls import path

urlpatterns = [
    path('events', EventListCreateView.as_view()),
    path('events/<uuid:id>', EventDetailView.as_view()),
    path('events/<int:id>/tickets', PurchaseTicketView.as_view()),
    path('users/<int:id>/tickets', UserTicketsView.as_view())

]