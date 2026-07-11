from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, IntegrityError
from .models import ModeloEquipo, Equipo, Salida

def ingreso_inventario(request):
    # Obtener todos los modelos del catálogo para llenar la lista desplegable en el formulario
    modelos = ModeloEquipo.objects.all().order_by('marca', 'modelo')

    if request.method == 'POST':
        # 1. Capturar los datos generales compartidos por el lote
        modelo_id = request.POST.get('modelo')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        n_guia_ingreso = request.POST.get('n_guia_ingreso')
        historial = request.POST.get('historial', 'NORMAL')
        estado_grado = request.POST.get('estado_grado')
        lote = request.POST.get('lote')
        observacion = request.POST.get('observacion')

        # 👇 CAMBIO 1: Captura limpia y segura de RAM y Disco (Soporte para Monitores/CPUs)
        memoria_ram = request.POST.get('memoria_ram')
        disco = request.POST.get('disco', '').strip() or None

        # Convertir RAM a entero solo si el operador escribió un número (si viene vacío, guarda None)
        memoria_ram = int(memoria_ram) if memoria_ram and memoria_ram.isdigit() else None

        # Detectar si el checkbox de ingreso masivo fue seleccionado
        es_masivo = request.POST.get('es_masivo') == 'on'

        # 2. Recolectar las series según el tipo de ingreso
        series_a_procesar = []
        if es_masivo:
            # Captura la lista completa de series generadas dinámicamente por la tabla
            series_a_procesar = request.POST.getlist('series_masivas[]')
        else:
            # Captura la serie única del cuadro de texto individual
            serie_unica = request.POST.get('numero_serie')
            if serie_unica:
                series_a_procesar.append(serie_unica.strip())

        # Validar que al menos haya una serie para registrar
        if not series_a_procesar or all(s == '' for s in series_a_procesar):
            messages.error(request, "Debe ingresar al menos un número de serie válido.")
            return render(request, 'inventario/ingreso_form.html', {'modelos': modelos})

        # 3. Guardar en la Base de Datos usando una Transacción Atómica
        try:
            with transaction.atomic():
                # Buscamos el objeto del catálogo correspondiente
                modelo_obj = ModeloEquipo.objects.get(id=modelo_id)
                
                for serie in series_a_procesar:
                    if not serie.strip():
                        continue  # Ignorar casillas vacías si las hubiera
                        
                    # Crear el registro físico del equipo
                    Equipo.objects.create(
                        modelo=modelo_obj,
                        numero_serie=serie.strip().upper(), # Guardamos en mayúsculas para estandarizar
                        fecha_ingreso=fecha_ingreso,
                        n_guia_ingreso=n_guia_ingreso,
                        historial=historial,
                        estado_grado=estado_grado,
                        lote=lote,
                        memoria_ram=memoria_ram,  # 👇 CAMBIO 2: Pasamos la variable ya procesada (puede ser número o None)
                        disco=disco,              # 👇 Guarda texto o None si es un Monitor
                        observacion=observacion,
                        en_stock=True
                    )
            
            # 👇 CAMBIO 3: Mensaje popup personalizado de éxito para el lote
            cantidad_registrada = len([s for s in series_a_procesar if s.strip()])
            messages.success(request, f"¡Lote de Importación Procesado! Se cargaron con éxito {cantidad_registrada} unidades bajo la Guía N° {n_guia_ingreso or 'S/N'}.")
            return redirect('ingreso_inventario')

        except IntegrityError:
            # Este error salta automáticamente si MySQL/MariaDB detecta una serie duplicada (UNIQUE constraint)
            messages.error(request, "Error de integridad: Uno o más números de serie ya existen en la base de datos. No se guardó ningún registro.")
        except Exception as e:
            # Cualquier otro error inesperado (ej. problemas de conversión de datos)
            messages.error(request, f"Hubo un error inesperado al procesar el inventario: {str(e)}")

    # Si entra por GET, simplemente renderiza el formulario vacío con los modelos disponibles
    return render(request, 'inventario/ingreso_form.html', {'modelos': modelos})

def salida_inventario(request):
    if request.method == 'POST':
        # 1. Capturar los datos del despacho
        fecha_salida = request.POST.get('fecha_salida')
        cliente = request.POST.get('cliente')
        n_guia_salida = request.POST.get('n_guia_salida')
        ram_salida = request.POST.get('ram_salida')
        disco_salida = request.POST.get('disco_salida')
        observacion = request.POST.get('observacion')
        es_masivo = request.POST.get('es_masivo') == 'on'

        # Limpieza de datos para los componentes opcionales de upgrade
        ram_salida = int(ram_salida) if ram_salida else None
        disco_salida = disco_salida.strip() if disco_salida else None

        # 2. Recolectar las series que van a salir
        series_a_procesar = []
        if es_masivo:
            series_a_procesar = request.POST.getlist('series_masivas[]')
        else:
            serie_unica = request.POST.get('numero_serie')
            if serie_unica:
                series_a_procesar.append(serie_unica.strip())

        if not series_a_procesar or all(s == '' for s in series_a_procesar):
            messages.error(request, "Debe ingresar al menos un número de serie para despachar.")
            return render(request, 'inventario/salida_form.html')

        # 3. Procesar el despacho seguro en bloque
        try:
            with transaction.atomic():
                for serie in series_a_procesar:
                    if not serie.strip():
                        continue
                    
                    # VALIDACIÓN CLAVE: El equipo debe existir y estar disponible (en stock)
                    try:
                        equipo_obj = Equipo.objects.get(numero_serie=serie.strip().upper(), en_stock=True)
                    except Equipo.DoesNotExist:
                        # Si una sola serie está mal digitada o ya se vendió, frena todo el lote por seguridad
                        raise Exception(f"La serie '{serie.strip().upper()}' no está disponible en stock o no existe.")

                    # Crear el registro de salida corporativo
                    Salida.objects.create(
                        equipo=equipo_obj,
                        fecha_salida=fecha_salida,
                        cliente=cliente,
                        n_guia_salida=n_guia_salida,
                        ram_salida=ram_salida,
                        disco_salida=disco_salida,
                        observacion=observacion
                    )

            cantidad_despachada = len([s for s in series_a_procesar if s.strip()])
            messages.success(request, f"¡Despacho procesado! Se retiraron {cantidad_despachada} unidades del stock correctamente.")
            return redirect('salida_inventario')

        except Exception as e:
            # Captura nuestro mensaje de error personalizado y hace Rollback automático
            messages.error(request, f"Despacho cancelado: {str(e)}")

    return render(request, 'inventario/salida_form.html')