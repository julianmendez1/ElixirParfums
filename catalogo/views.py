from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Perfume, Marca, Categoria, ConfiguracionTienda

def get_navbar_context():
    """Retorna las listas necesarias para poblar los menús desplegables del Navbar y ajustes globales."""
    return {
        'categorias_disponibles': Categoria.objects.all(),
        'marcas_disponibles': Marca.objects.all(),
        'configuracion': ConfiguracionTienda.objects.first(), # Inyecta el Settings Global
    }

def catalogo_list(request):
    query = request.GET.get('q', '')
    categoria_nombre = request.GET.get('categoria', '')
    marca_nombre = request.GET.get('marca', '')
    
    perfumes_base = Perfume.objects.filter(disponible=True)
    perfumes = perfumes_base
    
    filtro_activo = False

    # Buscador Global Minimalista (busca en nombre y foreignkey marca__nombre)
    if query:
        perfumes = perfumes.filter(Q(nombre__icontains=query) | Q(marca__nombre__icontains=query))
        filtro_activo = True
    
    # Filtros por dropdown de Navbar interactuando con ForeingKey fields
    if categoria_nombre:
        perfumes = perfumes.filter(categoria__nombre=categoria_nombre)
        filtro_activo = True
        
    if marca_nombre:
        perfumes = perfumes.filter(marca__nombre=marca_nombre)
        filtro_activo = True

    # Secciones especiales si no hay búsqueda
    nuevos = []
    promociones = []
    if not filtro_activo:
        nuevos = perfumes_base.order_by('-fecha_creacion')[:8]
        promociones = perfumes_base.filter(en_promocion=True).order_by('-fecha_creacion')[:8]

    context = {
        'perfumes': perfumes,
        'query': query,
        'categoria_seleccionada': categoria_nombre,
        'marca_seleccionada': marca_nombre,
        'filtro_activo': filtro_activo,
        'nuevos': nuevos,
        'promociones': promociones,
    }
    context.update(get_navbar_context())
    
    return render(request, 'catalogo/index.html', context)

def perfume_detalle(request, pk):
    perfume = get_object_or_404(Perfume, pk=pk, disponible=True)
    
    # Obtener sugerencias: excluimos el perfume actual y usamos ordenamiento aleatorio (?) limitando a 10.
    perfumes_sugeridos = Perfume.objects.filter(disponible=True).exclude(pk=perfume.pk).order_by('?')[:10]
    
    context = {
        'perfume': perfume,
        'perfumes_sugeridos': perfumes_sugeridos,
    }
    context.update(get_navbar_context()) # Para NavBar y Whatsapp Dinámico
    
    return render(request, 'catalogo/detalle.html', context)
