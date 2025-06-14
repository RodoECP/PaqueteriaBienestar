from paquetes.models import Frase

# Frases para registrar en la base de datos
frases_data = [
    {"frase": "en camino a"},
    {"frase": "recolectado en"},
    {"frase": "se dirige a"},
    {"frase": "está en el centro de recolección de"},
    {"frase": "entregado en"}  # Frase adicional
]

# Paso 1: Eliminar todas las frases existentes
print("Eliminando todas las frases existentes...")
Frase.objects.all().delete()

# Paso 2: Insertar nuevas frases
print("Cargando nuevas frases...")
for frase in frases_data:
    Frase.objects.create(**frase)

print("Frases cargadas exitosamente.")
