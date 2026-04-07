from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True, help_text="Ej: Masculino, Femenino, Unisex")

    def __str__(self):
        return self.nombre

class ConfiguracionTienda(models.Model):
    nombre_tienda = models.CharField(max_length=150, default="Noir Elixir")
    telefono_whatsapp = models.CharField(max_length=20, default="573000000000", help_text="Formato numérico sin símbolos. Ej: 573024445555")

    def __str__(self):
        return self.nombre_tienda

    class Meta:
        verbose_name = "Configuración Global"
        verbose_name_plural = "Configuraciones Globales"

class Perfume(models.Model):
    CALIDAD_CHOICES = [
        ('Original', 'Original'),
        ('1.1', '1.1'),
        ('En Aceite', 'En Aceite'),
    ]

    nombre = models.CharField(max_length=150)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="perfumes")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="perfumes")
    calidad = models.CharField(max_length=20, choices=CALIDAD_CHOICES, default='Original')
    
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    volumen_ml = models.IntegerField(help_text="Volumen en mililitros")
    
    imagen = models.ImageField(upload_to='perfumes/')
    
    en_promocion = models.BooleanField(default=False)
    precio_anterior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.marca.nombre} ({self.calidad})"

class PerfumeImagen(models.Model):
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name='imagenes_extra')
    imagen = models.ImageField(upload_to='perfumes/extras/')

    def __str__(self):
        return f"Imagen extra para {self.perfume.nombre}"
