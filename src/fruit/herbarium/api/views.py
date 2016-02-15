from rest_framework import generics

from . import serializers
from ..models import Herbarium


class HerbariumList(generics.ListAPIView):
    queryset = Herbarium.objects.select_related('kind')
    serializer_class = serializers.HerbariumSerializer
