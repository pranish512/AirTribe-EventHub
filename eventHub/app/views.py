from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Reservation
from .serializers import EventSerializer, ReservationSerializer


class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        
        status_param = self.request.query_params.get("status")
        venue_param = self.request.query_params.get("venue")

        if status_param:    
            queryset = queryset.filter(status=status_param)

        if venue_param:
            queryset = queryset.filter(
                venue__icontains=venue_param
            )

        return queryset


class ReservationViewSet(viewsets.ModelViewSet):

    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = Reservation.objects.all()

        event_id = self.request.query_params.get("event_id")

        # GET /api/reservations/?event_id=1
        if event_id:
            queryset = queryset.filter(event_id=event_id)

        return queryset

    # POST /api/reservations/{id}/cancel/
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):

        reservation = self.get_object()

        if reservation.status == "cancelled":
            return Response(
                {"error": "Already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Restore seats
        reservation.event.available_seats += reservation.seats_reserved
        reservation.event.save()

        # Update reservation status
        reservation.status = "cancelled"
        reservation.save()

        serializer = self.get_serializer(reservation)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )