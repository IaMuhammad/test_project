from django.urls import path

from warehouse.views import ManufactureListAPIView

urlpatterns = [
    path('get-info', ManufactureListAPIView.as_view()),
]
