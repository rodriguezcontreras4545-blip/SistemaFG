from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError

class ModeloEquipo(models.Model):
    # 1. Definimos los nuevos tipos de producto requeridos
    PRODUCTO_CHOICES = [
        ('LAPTOP', 'Laptop'),
        ('CPU', 'CPU / Computadora'),
        ('AIO', 'All-in-One'),
        ('MONITOR', 'Monitor'),
    ]
    producto = models.CharField(max_length=50, choices=PRODUCTO_CHOICES, default='LAPTOP')
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=150)
    tamano = models.CharField(max_length=20, verbose_name="Tamaño", blank=True, null=True)
    generacion = models.CharField(max_length=50, blank=True, null=True)
    procesador = models.CharField(max_length=50, blank=True, null=True)
    velocidad = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'modelos_equipos'
        verbose_name = "Modelo de Equipo"
        verbose_name_plural = "Catálogo de Modelos"
        unique_together = ('marca', 'modelo', 'procesador', 'velocidad')

    def __str__(self):
        return f"[{self.get_producto_display()}] {self.marca} {self.modelo} {self.procesador or ''}"


class Equipo(models.Model):
    modelo = models.ForeignKey(ModeloEquipo, on_delete=models.CASCADE)
    numero_serie = models.CharField(max_length=100, unique=True)
    fecha_ingreso = models.DateField()
    n_guia_ingreso = models.CharField(max_length=100, blank=True, null=True)
    historial = models.CharField(max_length=100, default='NOMINAL')
    estado_grado = models.CharField(max_length=50)
    lote = models.CharField(max_length=100, blank=True, null=True)
    
    # 2. Hacemos estos campos opcionales para dar soporte a Monitores
    memoria_ram = models.IntegerField(blank=True, null=True)
    disco = models.CharField(max_length=100, blank=True, null=True)
    
    observacion = models.TextField(blank=True, null=True)
    en_stock = models.BooleanField(default=True)

    class Meta:
        db_table = 'equipos' # Se conecta exacto a tu tabla de MySQL
        verbose_name = "Equipo Físico"
        verbose_name_plural = "Equipos en Stock"

    def __str__(self):
        return f"S/N: {self.numero_serie} - {self.modelo.modelo}"


class Salida(models.Model):
    equipo = models.OneToOneField(Equipo, on_delete=models.RESTRICT, db_column='equipo_id')
    fecha_salida = models.DateField()
    cliente = models.CharField(max_length=200)
    n_guia_salida = models.CharField(max_length=50)
    
    # Campos opcionales para upgrades en caliente
    ram_salida = models.IntegerField(blank=True, null=True)
    disco_salida = models.CharField(max_length=100, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'salidas' # Se conecta exacto a tu tabla de MySQL
        verbose_name = "Registro de Salida"
        verbose_name_plural = "Salidas / Despachos"

    def save(self, *args, **kwargs):
        # Lógica automática: Al guardar la salida, modifica el equipo físico relacionado
        # Si hubo upgrade, actualiza los componentes en la tabla del equipo físico
        if self.ram_salida:
            self.equipo.memoria_ram = self.ram_salida
        if self.disco_salida:
            self.equipo.disco = self.disco_salida
            
        # Cambia el stock a falso (0) automáticamente
        self.equipo.en_stock = False
        self.equipo.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Salida {self.n_guia_salida} - Cliente: {self.cliente}"