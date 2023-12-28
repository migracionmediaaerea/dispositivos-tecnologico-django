from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'dispositivos'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('lotes/', views.IndexLoteTagView.as_view(), name='lotes'),
    path('tags/', views.IndexTagView.as_view(), name='tags'),
    path('tags/<int:pk>/delete', views.TagDeleteView.as_view(), name='tags_delete'),
    path('tags/deleted', views.IndexTagDeletedView.as_view(), name='tags_index_deleted'),
    path('candados/', views.IndexCandadoView.as_view(), name='candados'),
    path('gafetes/', views.IndexGafeteView.as_view(), name='gafetes'),
    path('gafetes/deleted', views.IndexGafeteDeletedView.as_view(), name='gafetes-deleted'),

    
    #path('lotes/<int:pk>', views.ShowLoteView.as_view(), name='show-lote'),
]