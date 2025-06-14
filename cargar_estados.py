# -*- coding: utf-8 -*-
from paquetes.models import Estado

# Datos de los estados con sus regiones y latitudes actualizadas
estados_data = [
	{"estado": "Baja California", "latitud": 32.0, "region": "Norte, Noroeste"},
	{"estado": "Baja California Sur", "latitud": 24.0, "region": "Norte, Noroeste"},
	{"estado": "Sonora", "latitud": 29.0, "region": "Norte, Noroeste"},
	{"estado": "Chihuahua", "latitud": 28.0, "region": "Norte"},
	{"estado": "Coahuila", "latitud": 27.0, "region": "Norte, Noreste"},
	{"estado": "Nuevo Leon", "latitud": 25.7, "region": "Norte, Noreste"},
	{"estado": "Tamaulipas", "latitud": 24.2, "region": "Norte, Noreste"},
	{"estado": "Durango", "latitud": 24.0, "region": "Norte"},
	{"estado": "Sinaloa", "latitud": 24.0, "region": "Norte, Noroeste"},
	{"estado": "Zacatecas", "latitud": 22.8, "region": "Norte, Centro-Norte"},
	{"estado": "San Luis Potosi", "latitud": 22.2, "region": "Norte, Centro-Norte"},
	{"estado": "Aguascalientes", "latitud": 21.9, "region": "Centro, Centro-Norte"},
	{"estado": "Guanajuato", "latitud": 21.0, "region": "Centro"},
	{"estado": "Queretaro", "latitud": 20.6, "region": "Centro"},
	{"estado": "Ciudad de Mexico", "latitud": 19.4, "region": "Centro"},
	{"estado": "Estado de Mexico", "latitud": 19.3, "region": "Centro"},
	{"estado": "Hidalgo", "latitud": 20.1, "region": "Centro"},
	{"estado": "Tlaxcala", "latitud": 19.3, "region": "Centro, Centro-Sur"},
	{"estado": "Puebla", "latitud": 19.0, "region": "Centro, Centro-Sur"},
	{"estado": "Morelos", "latitud": 18.9, "region": "Centro, Centro-Sur"},
	{"estado": "Nayarit", "latitud": 21.5, "region": "Centro, Occidente"},
	{"estado": "Jalisco", "latitud": 20.5, "region": "Centro, Occidente"},
	{"estado": "Colima", "latitud": 19.2, "region": "Centro, Occidente"},
	{"estado": "Michoacan", "latitud": 19.7, "region": "Centro, Occidente"},
	{"estado": "Guerrero", "latitud": 17.6, "region": "Sur, Suroeste"},
	{"estado": "Oaxaca", "latitud": 17.1, "region": "Sur, Suroeste"},
	{"estado": "Chiapas", "latitud": 16.5, "region": "Sur, Sureste"},
	{"estado": "Tabasco", "latitud": 18.0, "region": "Sur, Sureste"},
	{"estado": "Veracruz", "latitud": 19.2, "region": "Sur, Sureste, Centro-Sur"},
	{"estado": "Campeche", "latitud": 19.8, "region": "Sur, Sureste"},
	{"estado": "Yucatan", "latitud": 20.4, "region": "Sur, Sureste"},
	{"estado": "Quintana Roo", "latitud": 19.0, "region": "Sur, Sureste"},
]

# Paso 1: Eliminar todos los estados existentes
print("Eliminando todos los estados existentes...")
Estado.objects.all().delete()

# Paso 2: Crear estados en la base de datos con los datos actualizados
print("Cargando nuevos estados...")
for estado in estados_data:
	Estado.objects.update_or_create(
		nombre=estado["estado"],
		defaults={
			"latitud": estado["latitud"],
			"region": estado["region"],
		},
	)

print("Estados cargados exitosamente.")
