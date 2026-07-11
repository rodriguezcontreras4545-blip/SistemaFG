from django.contrib import admin
from .models import ModeloEquipo, Equipo, Salida

@admin.register(ModeloEquipo)
class ModeloEquipoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'producto', 'procesador', 'generacion', 'tamano', 'velocidad')
    search_fields = ('marca', 'modelo', 'procesador', 'producto')
    list_filter = ('producto', 'marca')


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('numero_serie', 'get_producto', 'get_modelo', 'estado_grado', 'memoria_ram', 'disco', 'lote', 'en_stock', 'fecha_ingreso')
    
    # 🔍 BARRA DE BÚSQUEDA AVANZADA: 
    # Ahora puedes buscar por serie, marca, modelo, procesador exacto, lote o nro de guía de ingreso.
    search_fields = ('numero_serie', 'modelo__modelo', 'modelo__marca', 'modelo__procesador', 'lote', 'n_guia_ingreso')
    
    # 🌪️ PANELES DE FILTRADO (Lado derecho):
    # Agregamos filtros por Lote, Procesador, Tipo de Producto (Laptop/CPU), Estado estético, Stock y rango de fechas.
    list_filter = (
        'en_stock',
        'modelo__producto',      # <-- Filtro para Laptop / CPU / Monitor
        'modelo__marca',
        'modelo__procesador',    # <-- Filtro por Core i5, i7, Ryzen, etc.
        'estado_grado',
        'lote',                  # <-- Filtro por lote específico
        'fecha_ingreso',         # <-- Filtro dinámico por fechas (Hoy, últimos 7 días, este mes)
    )
    
    # Línea de tiempo superior para navegación rápida por fecha de ingreso
    date_hierarchy = 'fecha_ingreso'

    # Métodos para mostrar datos del catálogo en la tabla de equipos
    def get_modelo(self, obj):
        return f"{obj.modelo.marca} {obj.modelo.modelo} ({obj.modelo.procesador})"
    get_modelo.short_description = 'Ficha Técnica'

    def get_producto(self, obj):
        return obj.modelo.producto.upper()
    get_producto.short_description = 'Tipo'


@admin.register(Salida)
class SalidaAdmin(admin.ModelAdmin):
    # Unificamos en 'get_producto_modelo'
    list_display = (
        'n_guia_salida', 'get_serie', 'get_producto_modelo', 
        'get_procesador', 'get_generacion', 'get_ram', 
        'get_disco', 'cliente', 'fecha_salida'
    )
    search_fields = ('n_guia_salida', 'cliente', 'equipo__numero_serie', 'equipo__modelo__marca', 'equipo__modelo__modelo')
    list_filter = ('fecha_salida', 'equipo__modelo__producto', 'equipo__modelo__marca', 'cliente')
    date_hierarchy = 'fecha_salida'

    def get_serie(self, obj):
        return obj.equipo.numero_serie
    get_serie.short_description = 'Número de Serie'

    # 🌟 NUEVA FUNCIÓN COMBINADA PARA AHORRAR ESPACIO 🌟
    def get_producto_modelo(self, obj):
        return f"[{obj.equipo.modelo.get_producto_display()}] {obj.equipo.modelo.marca} {obj.equipo.modelo.modelo}"
    get_producto_modelo.short_description = 'Producto / Modelo'

    def get_procesador(self, obj):
        return obj.equipo.modelo.procesador or '-'
    get_procesador.short_description = 'Procesador'

    def get_generacion(self, obj):
        return obj.equipo.modelo.generacion or '-'
    get_generacion.short_description = 'Generación'

    def get_ram(self, obj):
        if obj.ram_salida:
            return f"{obj.ram_salida} GB"
        return f"{obj.equipo.memoria_ram} GB" if obj.equipo.memoria_ram else '-'
    get_ram.short_description = 'RAM Final'

    def get_disco(self, obj):
        if obj.disco_salida:
            return obj.disco_salida
        return obj.equipo.disco or '-'
    get_disco.short_description = 'Disco Final'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "equipo":
            kwargs["queryset"] = Equipo.objects.filter(en_stock=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)