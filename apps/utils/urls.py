
from django.urls import path

from . import views

app_name = 'utils'

urlpatterns = [
    path('csv-custom/<str:model>', views.GenerateCustomCsv.as_view(), name='csv-custom'),
    path('csv/<str:model>', views.GenerateCsv.as_view(), name='csv'),
    #path('csv-historic/<str:model>/', views.GenerateHistoricCsv.as_view(), name='csv-historic'),
]