from rest_framework import generics
from rest_framework.response import Response

from warehouse.models import Manufacture
from warehouse.serializer import ManufactureSerializer


# Create your views here.
class ManufactureListAPIView(generics.ListAPIView):
    queryset = Manufacture.objects.all()
    serializer_class = ManufactureSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'result': serializer.data})
