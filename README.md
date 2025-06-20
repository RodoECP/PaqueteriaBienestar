# Paquetería del Bienestar

Este proyecto es una simulación de un sistema de rastreo de paquetes desarrollado como parte de un proyecto universitario. La aplicación utiliza Django como framework principal, MongoDB como base de datos y está diseñada para simular el movimiento dinámico de paquetes a través de rutas entre estados de México.

---

## Requisitos previos

1. **Python**: Versión 3.10.10.
3. **Virtualenv**: Para crear entornos virtuales de Python.

---

## Instalación

### Paso 1: Configurar el entorno virtual

1. Crea un entorno virtual:
   ```bash
   python -m venv .venv
   ```
2. Activa el entorno virtual:
   - En Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

### Paso 2: Instalar dependencias

Instala las dependencias del proyecto desde el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Paso 3: Iniciar el servidor

Para ejecutar la aplicación en un entorno de desarrollo:
```bash
python manage.py runserver
```

Accede a la aplicación en: [http://127.0.0.1:8000].

---

## Estructura del Proyecto

- **`paquetes`**: Aplicación principal que contiene los modelos, vistas y plantillas para gestionar los paquetes, estados y rutas.

---

## Funcionalidades principales

1. **Solicitar envío**:
   - Permite registrar un nuevo paquete con detalles del remitente, receptor, estado de origen y destino.
   - Genera rutas dinámicas entre los estados seleccionados.

2. **Rastrear paquete**:
   - Proporciona un sistema de rastreo en tiempo real simulado.
   - Muestra el progreso del paquete a medida que avanza por las rutas configuradas.

3. **Dinámica de rutas**:
   - Las rutas son activadas dinámicamente según el tiempo ficticio de transición basado en las distancias entre estados.

4. **Manejo de Usuarios**:
   - Los usuarios se pueden registrar para realizar un pedido, modificar sus datos y borrar su cuenta si desean.
   - Borrar una cuenta no elimina los pedidos que se hayan realizado con ella, solo los desvincula.

---

## Librerías utilizadas

- **Django**: Framework principal para el desarrollo.
- **Djongo**: Conector de MongoDB para Django.
- **DNSPython**: Conector de Python a MongoDB Atlas
- **Python-dotenv**: Para manejar configuraciones sensibles en un archivo `.env`.


---

© 2024 Paquetería del Bienestar - Todos los derechos reservados.
```