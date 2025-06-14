# Paquetería del Bienestar

Este proyecto es una simulación de un sistema de rastreo de paquetes desarrollado como parte de un proyecto universitario. La aplicación utiliza Django como framework principal, MongoDB como base de datos y está diseñada para simular el movimiento dinámico de paquetes a través de rutas entre estados de México.

---

## Requisitos previos

1. **Python**: Versión 3.10.10.
2. **MongoDB**: Instalado y ejecutándose como base de datos principal.
3. **Virtualenv**: Para crear entornos virtuales de Python.

---

## Instalación

### Paso 1: Configurar MongoDB

1. Instala MongoDB siguiendo la guía oficial: [Documentación de instalación](https://www.mongodb.com/docs/manual/installation/).
2. Una vez instalado, asegúrate de que MongoDB esté ejecutándose:
   ```bash
   mongod
mongosh
   ```
3. Crea una base de datos para el proyecto (opcional):
   ```bash
   mongo
   use paqueteria_del_bienestar
   ```

### Paso 2: Clonar el repositorio

Clona este repositorio a tu máquina local:
```bash
git@github.com:rayo-alcantar/Paqueteria_del_bienestar.git
cd paqueteria_del_bienestar
```

### Paso 3: Configurar el entorno virtual

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

### Paso 4: Instalar dependencias

Instala las dependencias del proyecto desde el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Paso 5: Configurar Django

1. Crea un archivo `.env` en la raíz del proyecto y añade la siguiente configuración (personalízala según sea necesario):
   ```
   DEBUG=True
   SECRET_KEY=tu_llave_secreta
   DATABASE_NAME=paqueteria_del_bienestar
   DATABASE_HOST=127.0.0.1
   DATABASE_PORT=27017
   ```

2. Realiza las migraciones de la base de datos:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## Uso

### Cargar datos iniciales (Estados y Frases)

Para cargar los datos iniciales, utiliza los siguientes scripts:

1. **Cargar estados**:
   ```bash
   python manage.py shell < cargar_estados.py
   ```

   Este script elimina todos los estados existentes y crea los nuevos basados en los datos de regiones y coordenadas ficticias.

2. **Cargar frases**:
   ```bash
   python manage.py shell < cargar_frases.py
   ```

   Este script elimina todas las frases existentes y registra nuevas frases necesarias para las rutas de los paquetes.

### Iniciar el servidor

Para ejecutar la aplicación en un entorno de desarrollo:
```bash
python manage.py runserver
```

Accede a la aplicación en: [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Estructura del Proyecto

- **`paquetes`**: Aplicación principal que contiene los modelos, vistas y plantillas para gestionar los paquetes, estados y rutas.
- **`cargar_estados.py`**: Script para cargar estados de México organizados por región.
- **`cargar_frases.py`**: Script para cargar frases descriptivas para las rutas.

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

---

## Librerías utilizadas

- **Django**: Framework principal para el desarrollo.
- **Djongo**: Conector de MongoDB para Django.
- **Python-dotenv**: Para manejar configuraciones sensibles en un archivo `.env`.

---

## Contribución

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama nueva para tus cambios:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza tus cambios y haz commit:
   ```bash
   git commit -m "Añade nueva funcionalidad"
   ```
4. Haz push a tu rama y abre un pull request:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```

---

---

© 2024 Paquetería del Bienestar - Todos los derechos reservados.
```# PaqueteriaBienestar
# PaqueteriaBienestar
