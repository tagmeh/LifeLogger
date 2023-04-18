# from rest_framework import viewsets
# from .models import HealthStats
# from .serializers import HealthStatsSerializer
#
#
# class HealthStatsViewSet(viewsets.ModelViewSet):
#     serializer_class = HealthStatsSerializer
#     queryset = HealthStats.objects.all()
#
#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)
