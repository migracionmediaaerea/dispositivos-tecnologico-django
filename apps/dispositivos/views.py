import os
from datetime import datetime

from catalogos_modular.models import CatalogoCandado, Gafete, Group, Lote, Tag
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django_filters.views import FilterView
from gafetes_modular.models import GafeteOficial

from .filters import CandadoFilter, GafeteFilter, LoteFilter, TagFilter


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dispositivos/index.html"



class IndexLoteTagView(PermissionRequiredMixin, FilterView):
	permission_required = 'catalogos_modular.view_tags_index'
	model = Lote
	template_name = "dispositivos/lotes/index.html"
	context_object_name = 'lotes'
	paginate_by = 20
	filterset_class = LoteFilter

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['ACCESO_URL'] =  os.getenv('ACCESO_URL')
		return context

	def get_queryset(self):
		if self.request.user.has_group('Tramitador de tags'):
			return Lote.objects.filter(created_by=self.request.user, deleted__isnull=True)
		else:
			return Lote.objects.filter(deleted__isnull=True)

class IndexTagView(PermissionRequiredMixin, FilterView):
	permission_required = 'catalogos_modular.view_tags_index'
	model = Tag
	template_name = "dispositivos/tags/index.html"
	context_object_name = 'tags'
	paginate_by = 20
	filterset_class = TagFilter

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['ACCESO_URL'] =  os.getenv('ACCESO_URL')
		return context

	def get_queryset(self):
		if self.request.user.has_group('Tramitador de tags'):
			return Tag.objects.filter(created_by=self.request.user, deleted__isnull=True).exclude(estado=Tag.Status.DESACTIVADO)
		else:
			return Tag.objects.filter(deleted__isnull=True).exclude(estado=Tag.Status.DESACTIVADO)

class IndexTagDeletedView(IndexTagView):
	
	def get_queryset(self):
		print(Tag.objects.filter(deleted__isnull=True, estado=Tag.Status.DESACTIVADO))
		if self.request.user.has_group('Tramitador de tags'):
			return Tag.objects.filter(created_by=self.request.user, deleted__isnull=True, estado=Tag.Status.DESACTIVADO)
		else:
			return Tag.objects.filter(deleted__isnull=True, estado=Tag.Status.DESACTIVADO)

class TagDeleteView(PermissionRequiredMixin, generic.View):
	permission_required = 'catalogos_modular.view_tags_index'
	model = Tag

	# será una desactivación en vez de un borrado
	def post(self, request, *args, **kwargs):
		tag = Tag.objects.filter(pk=kwargs['pk']).first()
		if not tag:
			messages.error(request, 'No se encontró el tag')
			return HttpResponseRedirect(reverse('dispositivos:tags'))
		
		if tag.estado == Tag.Status.DESACTIVADO:
			messages.error(request, 'El tag ya se encuentra desactivado')
			return HttpResponseRedirect(reverse('dispositivos:tags'))
		
		if self.request.user.has_group('Tramitador de tags'):
			if tag.created_by != self.request.user:
				messages.error(request, 'No tiene permisos para desactivar este tag')
				return HttpResponseRedirect(reverse('dispositivos:tags'))
		
		tag.estado = Tag.Status.DESACTIVADO
		tag.updated_by = request.user
		tag.updated_at = datetime.utcnow()
		tag.save()
		messages.success(request, 'Tag desactivado correctamente')
		return HttpResponseRedirect(reverse('dispositivos:tags'))

class ShowLoteView(PermissionRequiredMixin, generic.DetailView):
	permission_required = 'catalogos_modular.view_tags_index'
	model = Lote
	template_name = "dispositivos/tags/show.html"
	context_object_name = 'lote'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		lote = self.get_object()
		tags = Tag.objects.filter(lote=lote).order_by('tag')
		
		tag_anterior = None
		tag_inicial = None
		tag_final = None
		rango = {
			'numero_inicial': [],
			'numero_final': [],
		}
		for tag in tags:
			if tag_anterior is None:
				tag_anterior = tag.tag
				tag_inicial = tag.tag
				continue

			if tag_inicial is None:
				tag_inicial = tag_anterior
				tag_anterior = tag.tag
				continue
			
			if int(tag.tag[-10:]) != int(tag_anterior[-10:]) + 1:
				rango['numero_inicial'].append(tag_inicial)
				rango['numero_final'].append(tag_anterior)
				tag_inicial = None
			
			tag_anterior = tag.tag

		rango['numero_inicial'].append(tag_inicial)
		rango['numero_final'].append(tag_anterior)

		# sort rango['numero_inicial'] and rango['numero_final']
		rango['numero_inicial'].sort()
		rango['numero_final'].sort()
			
		context['rango'] = rango
		return context

class IndexCandadoView(PermissionRequiredMixin, FilterView):
	permission_required = 'catalogos_modular.view_candados_index'
	template_name = "dispositivos/candados/index.html"
	context_object_name = 'candados'
	paginate_by = 20
	filterset_class = CandadoFilter
	
	def get_queryset(self):
		values = ['created_by__first_name', 'created_by__last_name', 'created_by__second_last_name', 'created_by__rfc', 'created_by__curp', 'candado', 'roto']
		if self.request.user.has_group('Tramitador de candados'):
			return CatalogoCandado.objects.filter(created_by=self.request.user).only(*values).order_by('candado')
		
		return CatalogoCandado.objects.all().only(*values).order_by('candado')

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['ACCESO_URL'] = settings.ACCESO_URL
		return context

class IndexGafeteView(PermissionRequiredMixin, FilterView):
	permission_required = 'gafetes_modular.view_gafetes_index'
	template_name = "dispositivos/gafetes/index.html"
	context_object_name = 'gafetes'
	paginate_by = 20
	filterset_class = GafeteFilter
	model = GafeteOficial

	def get_queryset(self):
		return GafeteOficial.objects.filter(deleted__isnull=True).order_by('numero_gafete')

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['ACCESO_URL'] = settings.ACCESO_URL
		return context

class IndexGafeteDeletedView(PermissionRequiredMixin, FilterView):
	permission_required = 'gafetes_modular.view_gafetes_index'
	template_name = "dispositivos/gafetes/index.html"
	context_object_name = 'gafetes'
	paginate_by = 20
	filterset_class = GafeteFilter
	model = GafeteOficial

	def get_queryset(self):
		return GafeteOficial.all_objects.filter(deleted__isnull=False).order_by('numero_gafete')


	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['ACCESO_URL'] = settings.ACCESO_URL
		return context
