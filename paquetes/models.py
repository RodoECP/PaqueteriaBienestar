import uuid
from djongo import models
from bson import ObjectId


class Usuario(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_usuario



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
    uusuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100, unique=True, blank=True)
    remitente = models.CharField(max_length=255)
    direccion_recoleccion = models.TextField()
    receptor = models.CharField(max_length=255)
    direccion_entrega = models.TextField()
    descripcion = models.TextField()
    peso = models.FloatField()
    estado_actual = models.ForeignKey(
        Estado, on_delete=models.SET_NULL, null=True, related_name="paquetes"
    )
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    estado_paquete = models.CharField(
        max_length=50,
        choices=[
            ("En tránsito", "En tránsito"),
            ("Recolección", "Recolección"),
            ("Entregado", "Entregado"),
            ("Retrasado", "Retrasado"),
            ("Cancelado", "Cancelado"),
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
      



class SolicitudEnvio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    remitente_nombre = models.CharField(max_length=100)
    remitente_colonia = models.CharField(max_length=100)
    remitente_calle = models.CharField(max_length=100)
    remitente_numero = models.CharField(max_length=20)
    remitente_cp = models.CharField(max_length=5)
    remitente_estado = models.CharField(max_length=100)

    destinatario_nombre = models.CharField(max_length=100)
    destinatario_colonia = models.CharField(max_length=100)
    destinatario_calle = models.CharField(max_length=100)
    destinatario_numero = models.CharField(max_length=20)
    destinatario_cp = models.CharField(max_length=5)
    destinatario_estado = models.CharField(max_length=100)

    peso = models.FloatField()
    dimensiones = models.CharField(max_length=50)
    descripcion = models.TextField()
    cotizacion = models.FloatField()
    numero_seguimiento = models.CharField(max_length=20, unique=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud de {self.remitente_nombre} - {self.destinatario_nombre}"
