from django.contrib import admin
from django.utils.html import format_html
from .models import Marca, Categoria, ConfiguracionTienda, Perfume, PerfumeImagen

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(ConfiguracionTienda)
class ConfiguracionTiendaAdmin(admin.ModelAdmin):
    list_display = ('nombre_tienda', 'telefono_whatsapp')

class PerfumeImagenInline(admin.TabularInline):
    model = PerfumeImagen
    extra = 1

@admin.action(description="Duplicar perfumes seleccionados")
def duplicar_perfumes(modeladmin, request, queryset):
    for perfume in queryset:
        perfume.pk = None # Al resetear primary key genramos un clon
        perfume.nombre = f"{perfume.nombre} - Copia"
        perfume.save()

@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ('miniatura_imagen', 'nombre', 'marca', 'categoria', 'calidad', 'precio', 'en_promocion', 'disponible')
    list_filter = ('marca', 'categoria', 'calidad', 'en_promocion', 'disponible')
    search_fields = ('nombre', 'marca__nombre', 'descripcion')
    readonly_fields = ('fecha_creacion',)
    inlines = [PerfumeImagenInline]
    actions = [duplicar_perfumes]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'marca', 'descripcion', 'categoria', 'calidad')
        }),
        ('Precios y Volumen', {
            'fields': ('precio', 'volumen_ml', 'en_promocion', 'precio_anterior')
        }),
        ('Media y Estado', {
            'fields': ('imagen', 'disponible', 'fecha_creacion')
        }),
    )

    def miniatura_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 5px; object-fit: cover; display:block;"/>', obj.imagen.url)
        return "Sin imagen"
    miniatura_imagen.short_description = "Thumb"
