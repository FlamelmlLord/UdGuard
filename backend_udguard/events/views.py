from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from events.serializers import EventsSerializer, CreateEventsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from events.models import Events


class EventsListCreateViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Events.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(events, request)
        serializer = EventsSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        tipo = request.user.tipo_user
        if tipo == "admin":
            serializer = CreateEventsSerializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
