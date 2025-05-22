from django.shortcuts import render
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .serializers import EventSerializer, TicketSerializer, UserSerializer


# DB
EVENTS = {}
TICKETS = {}
USERS = {}

#
#helper
def paginate(data, request):
    try:
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        return data[offset:offset+limit]
    except:
        return data


class EventListCreateView(APIView):
    def get(self, request):
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        venue  = request.GET.get('venue')
        filtered_events = list(EVENTS.values())
        if date_from and date_to:
            filtered_events = [
                e for e in filtered_events 
                if date_from <= e['date'] <= date_to
            ]
        if venue:
            filtered_events = [e for e in filtered_events if e['venue'] == venue]

        paginated = paginate(filtered_events, request)
        return Response(paginated)


    def post(self, request):
        id = uuid.uuid4()
        data =  request.data
        data['id'] = id
        data['created_at'] = datetime.now()
        EVENTS[id] = data
        return Response(data, status= status.HTTP_201_CREATED)


class EventDetailView(APIView):
    def get(self, request, id):
        event = EVENTS.get(id)
        if not event:
            return Response({'error': 'Event not found'}, status=400)
        return Response(event)

class PurchaseTicketView(APIView):
    def post(self, request, id):
        ticket_counter = uuid.uuid4()
        user_id = request.data.get('user_id')
        event_id = int(id)
        
        if not user_id or int(user_id) not in USERS:
            return Response({'error': 'Invalid user_id'}, status=400)
        if event_id not in EVENTS:
            return Response({'error': 'Invalid event_id'}, status=400)

        # Check duplicate booking
        for ticket in TICKETS.values():
            if ticket['event_id'] == event_id and ticket['user_id'] == int(user_id):
                return Response({'error': 'User has already booked this event'}, status=400)

        # Check capacity
        event_tickets = [t for t in TICKETS.values() if t['event_id'] == event_id]
        if len(event_tickets) >= EVENTS[event_id]['capacity']:
            return Response({'error': 'Event full'}, status=400)

        ticket = {
            'id': ticket_counter,
            'event_id': event_id,
            'user_id': int(user_id),
            'created_at': datetime.now()
        }
        TICKETS[ticket_counter] = ticket
        return Response(ticket, status=201)

class UserTicketsView(APIView):
    def get(self, request, id):
        user_id = int(id)
        if user_id not in USERS:
            return Response({'error': 'User not found'}, status=404)
        user_tickets = [t for t in TICKETS.values() if t['user_id'] == user_id]
        return Response(user_tickets)
