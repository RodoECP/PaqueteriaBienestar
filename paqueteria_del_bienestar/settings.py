from pathlib import Path

# Construye rutas dentro del proyecto como BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta (mantenla en secreto en producción)
SECRET_KEY = '95gz=npbnhkvqss#bk-db_by#mz+*$xzeai9n$e0ww$i_v2y1%'

# ¡No ejecutes con debug activado en producción!
DEBUG = True # Asegúrate de establecer DEBUG en False en producción

ALLOWED_HOSTS = ['paqueteriabienestar.zapto.org', '127.0.0.1', 'localhost']

# Definición de aplicaciones
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'paquetes',  # Tu app de paquetes
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'paqueteria_del_bienestar.urls'

# Configuración de plantillas
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],  # Ruta global al directorio de plantillas
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',  # Necesario para algunas funciones
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
                'paquetes.context_processors.auth_context',  # Tu contexto personalizado
			],
		},
	},
]

WSGI_APPLICATION = 'paqueteria_del_bienestar.wsgi.application'

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'paqueteria_mexicana',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb+srv://EquipoPaqueteria:EquipoPaqueteria@cluster0.y4bexfw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',
            'tls': True,
        }
    }
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

# Internacionalización
LANGUAGE_CODE = 'es-mx'  # Ajustado para México

TIME_ZONE = 'America/Mexico_City'  # Zona horaria de México

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Archivos estáticos (CSS, JavaScript, Imágenes)
STATIC_URL = '/static/'

# Definir STATIC_ROOT para que collectstatic recopile los archivos estáticos aquí
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración opcional: descomentar si tienes archivos estáticos adicionales fuera de tus apps
STATICFILES_DIRS = [
	BASE_DIR / "static",
]

# Configuración de Django REST Framework (si lo usas)
REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',  # Renderizar siempre en JSON
	),
	'DEFAULT_PARSER_CLASSES': (
		'rest_framework.parsers.JSONParser',
	),
}