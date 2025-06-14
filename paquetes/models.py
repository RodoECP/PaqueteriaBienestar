import uuid
from django.db import models

class Estado(models.Model):
	nombre = models.CharField(max_length=100, unique=True)
	latitud = models.FloatField(null=True, blank=True, default=0.0)
	longitud = models.FloatField(null=True, blank=True, default=0.0)
	region = models.CharField(max_length=100, null=True, blank=True)  # Aumentado max_length a 100

	def __str__(self):
		return self.nombre

class Frase(models.Model):
	frase = models.CharField(max_length=255)  # Frase para describir estados de la ruta

	def __str__(self):
		return self.frase

class Paquete(models.Model):
	codigo = models.CharField(max_length=100, unique=True, blank=True)  # Código único del paquete
	remitente = models.CharField(max_length=255)  # Nombre del remitente
	direccion_recoleccion = models.TextField()  # Dirección completa de recolección
	receptor = models.CharField(max_length=255)  # Nombre del receptor
	direccion_entrega = models.TextField()  # Dirección completa de entrega
	descripcion = models.TextField()  # Descripción del paquete
	peso = models.FloatField()  # Peso del paquete en kilogramos
	estado_actual = models.ForeignKey(
		Estado, on_delete=models.SET_NULL, null=True, related_name="paquetes"
	)  # Estado actual donde se encuentra el paquete
	fecha_envio = models.DateTimeField(auto_now_add=True)  # Fecha en la que se envió el paquete
	fecha_entrega = models.DateTimeField(null=True, blank=True)  # Fecha de entrega (si ya fue entregado)
	estado_paquete = models.CharField(
		max_length=50,
		choices=[
			("En tránsito", "En tránsito"),
			("Recolección", "Recolección"),
			("Entregado", "Entregado"),
			("Retrasado", "Retrasado"),  # Estado adicional para flexibilidad
			("Cancelado", "Cancelado"),  # Estado adicional para flexibilidad
		],
		default="En tránsito",
	)

	def save(self, *args, **kwargs):
		if not self.codigo:
			self.codigo = str(uuid.uuid4()).replace("-", "").upper()[:12]
		super().save(*args, **kwargs)

	def __str__(self):
		return f"Paquete {self.codigo} - {self.estado_paquete}"

class Ruta(models.Model):
	paquete = models.ForeignKey(
		Paquete, on_delete=models.CASCADE, related_name="rutas"
	)
	frase = models.ForeignKey(
		Frase, on_delete=models.CASCADE, related_name="rutas"
	)
	estado_origen = models.ForeignKey(
		Estado, on_delete=models.CASCADE, related_name="rutas_origen"
	)
	estado_destino = models.ForeignKey(
		Estado, on_delete=models.CASCADE, related_name="rutas_destino"
	)
	fecha_actualizacion = models.DateTimeField(auto_now_add=True)
	orden = models.PositiveIntegerField(default=0)  # Orden lógico de la ruta
	activo = models.BooleanField(default=False)  # Indica si es el estado actual

	def __str__(self):
		return f"Ruta: {self.estado_origen} -> {self.estado_destino} | Paquete: {self.paquete.codigo}"
