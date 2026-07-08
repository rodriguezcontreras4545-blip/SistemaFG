# Sistema de Control de Inventario - FICA Reacondicionados 💻📦

Este es un sistema web robusto diseñado para automatizar el control de existencias, flujos de ingresos por lotes y despachos de equipos informáticos reacondicionados. Reemplaza las hojas de cálculo tradicionales por una base de datos relacional optimizada en **Tercera Forma Normal (3NF)**, garantizando la integridad de los números de serie únicos y el historial de transacciones.

## 🚀 Características Principales

* **Ingreso Masivo por Lotes (Formulario Dinámico):** Permite registrar múltiples equipos del mismo modelo escaneando o digitando sus números de serie de manera simultánea en una interfaz reactiva controlada por JavaScript.
* **Despacho y Salidas en Bloque:** Validación en tiempo real del stock (`en_stock = True`). Si una serie no existe o ya fue vendida, el sistema frena la transacción de forma atómica para evitar inconsistencias.
* **Upgrades en Caliente:** Capacidad de registrar modificaciones de hardware (Aumentos de memoria RAM o cambios de Disco) directamente en el momento del despacho, actualizando la ficha técnica del equipo automáticamente.
* **Interfaz Profesional Adaptativa:** Panel de administración completamente personalizado mediante el framework **Jazzmin**, con soporte nativo para temas oscuros, filtros avanzados y barras de búsqueda cruzada.
* **Arquitectura Distribuida:** Backend desarrollado en Django conectándose a través de la red local (TCP/IP) a un servidor de base de datos dedicado corriendo sobre **Debian Linux**.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.14+ & Django 6.0.6
* **Base de Datos:** MariaDB / MySQL (Desplegado en servidor dedicado Debian)
* **Frontend:** Bootstrap 4, FontAwesome 5 & JavaScript (Vanilla)
* **Entorno Visual:** Django Jazzmin Admin
* **Control de Versiones:** Git & GitHub

---

## 🔧 Instalación y Configuración Local

Si deseas replicar este entorno de desarrollo en otra computadora, sigue estos pasos:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/rodriguezcontreras4545-blip/SistemaFG.git](https://github.com/rodriguezcontreras4545-blip/SistemaFG.git)
cd SistemaFG

# En Linux/macOS
python -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate

Instalar las dependencias del proyecto
pip install -r requirements.txt



Configurar las variables de conexión
Abre el archivo core/settings.py y asegúrate de apuntar los parámetros de la base de datos hacia tu servidor MariaDB (Local o remoto en Debian):
Python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bd_inventario_reacondicionados',
        'USER': 'tu_usuario_db',
        'PASSWORD': 'tu_contraseña_db',
        'HOST': 'IP_DE_TU_SERVIDOR',
        'PORT': '3306',
    }
}


Aplicar migraciones y crear el superusuario
Bash

python manage.py migrate
python manage.py createsuperuser


Iniciar el servidor de desarrollo
Bash

python manage.py runserver 0.0.0.0:8000

Accede desde tu navegador a http://localhost:8000/admin/




© 2026 FICA S.A.C. -Rodriguez C. Jose A. - Todos los derechos reservados. Desarrollado como parte del proyecto de Ingeniería de TI.
