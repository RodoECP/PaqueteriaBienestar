import traceback
import random
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.db.models import Q
from .models import Paquete, Estado, Ruta, Frase, Usuario
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from bson import ObjectId
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# Mapeo de tiempo de transición por tipo de ruta (1 minuto para cada transición)
TIEMPO_TRANSICION_MAP = {
	"Recolección": timedelta(minutes=1),
	"En Tránsito": timedelta(minutes=1),
	"En Centro de Distribución": timedelta(minutes=1),
	"En Entrega": timedelta(minutes=1),
}

def index(request):
    usuario_id = request.session.get('usuario_id')
    paquetes = None
    usuario_nombre = None

    if usuario_id:
        try:
            obj_id = ObjectId(usuario_id)
            usuario = Usuario.objects.get(_id=obj_id)
            paquetes = Paquete.objects.filter(uusuario=usuario).order_by('-fecha_envio')
            usuario_nombre = usuario.nombre_usuario
        except (Exception, Usuario.DoesNotExist):
            # Si hay algún error con la sesión, la limpiamos
            del request.session['usuario_id']
            request.session.modified = True

    return render(request, 'index.html', {
        'paquetes': paquetes,
        'usuario_nombre': usuario_nombre,
        'autenticado': bool(usuario_id)
    })

def rastrear_paquete(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        try:
            paquete = Paquete.objects.get(codigo=codigo)
        except Paquete.DoesNotExist:
            error = "El número de rastreo ingresado no existe."
            return render(request, "rastreo_paquete.html", {"error": error})
        rutas = list(Ruta.objects.filter(paquete=paquete).order_by("orden"))
        fecha_inicio = rutas[0].fecha_actualizacion if rutas else None
        if not fecha_inicio:
            error = "No se pudo determinar la fecha de inicio del paquete."
            return render(request, "rastreo_paquete.html", {"error": error})
        elapsed_time = now() - fecha_inicio
        tiempo_acumulado = timedelta(0)
        current_route = None
        rutas_relevantes = []
        for ruta in rutas:
            tipo_ruta = "Recolección" if ruta.orden == 1 else "En Tránsito"
            tiempo_transicion = TIEMPO_TRANSICION_MAP.get(tipo_ruta, timedelta(minutes=1))
            tiempo_acumulado += tiempo_transicion
            if elapsed_time >= tiempo_acumulado:
                ruta.activo = False
                ruta.fecha_actualizacion = fecha_inicio + (tiempo_acumulado - tiempo_transicion)
                ruta.save()
                rutas_relevantes.append(ruta)
            else:
                if current_route is None:
                    current_route = ruta
                    ruta.activo = True
                    ruta.fecha_actualizacion = fecha_inicio + (tiempo_acumulado - tiempo_transicion)
                    ruta.save()
                    rutas_relevantes.append(ruta)
                break
        if hasattr(paquete.peso, 'to_decimal'):
            paquete.peso = Decimal(paquete.peso.to_decimal())
        if current_route is None:
            paquete.estado_paquete = "Entregado"
            paquete.fecha_entrega = fecha_inicio + tiempo_acumulado
            paquete.save()
            Ruta.objects.filter(paquete=paquete).update(activo=False)
            rutas_relevantes = rutas
        else:
            paquete.estado_actual = current_route.estado_destino
            paquete.estado_paquete = tipo_ruta
            paquete.save()

        estado_origen = rutas[0].estado_origen if rutas else None
        estado_destino = rutas[-1].estado_destino if rutas else None

        context = {
            "paquete": paquete,
            "rutas": rutas_relevantes,
            "estado_origen": estado_origen,
            "estado_destino": estado_destino,
        }
        return render(request, "rastreo_paquete.html", context)
    return render(request, "rastreo_paquete.html")


def descargar_pdf(request, codigo):
    try:
        paquete = get_object_or_404(Paquete, codigo=codigo)
        rutas = list(Ruta.objects.filter(paquete=paquete).order_by("orden"))
        estado_origen = rutas[0].estado_origen if rutas else None
        estado_destino = rutas[-1].estado_destino if rutas else None

        # Calcular el costo estimado dinámicamente
        peso = float(paquete.peso or 0)
        costo_envio = 50 + (10 * peso)

        context = {
            "paquete": paquete,
            "rutas": rutas,
            "estado_origen": estado_origen,
            "estado_destino": estado_destino,
            "costo_envio": costo_envio,
        }

        # Renderizar el template para el PDF
        pdf_content = render_to_string('paquete_entregado_pdf.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="comprobante_entrega_{paquete.codigo}.pdf"'

        # Crear el PDF
        pisa_status = pisa.CreatePDF(pdf_content, dest=response)

        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        return response

    except Exception as e:
        error = f"Hubo un error al generar el PDF: {e}"
        traceback_str = traceback.format_exc()
        print(traceback_str)
        rutas = list(Ruta.objects.filter(paquete=paquete).order_by("orden")) if 'paquete' in locals() else []
        estado_origen = rutas[0].estado_origen if rutas else None
        estado_destino = rutas[-1].estado_destino if rutas else None

        context = {
            "error": error,
            "paquete": paquete if 'paquete' in locals() else None,
            "rutas": rutas,
            "estado_origen": estado_origen,
            "estado_destino": estado_destino,
        }
        return render(request, "rastreo_paquete.html", context)


@transaction.atomic
def solicitar_envio(request):
    estados = Estado.objects.all()
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    try:
        obj_id = ObjectId(usuario_id)
        usuario = Usuario.objects.get(_id=obj_id)
    except (Usuario.DoesNotExist, Exception):
        return redirect('login')

    if request.method == "POST":
        errors = {}
        form_data = request.POST.copy()
        try:
            descripcion = request.POST.get("descripcion")
            peso = request.POST.get("peso")
            remitente = request.POST.get("remitente")

            # Datos de dirección de recolección
            colonia_recoleccion = request.POST.get("colonia_recoleccion")
            calle_recoleccion = request.POST.get("calle_recoleccion")
            numero_recoleccion = request.POST.get("numero_recoleccion")
            codigo_postal_recoleccion = request.POST.get("codigo_postal_recoleccion")

            receptor = request.POST.get("receptor")

            # Datos de dirección de entrega
            colonia_entrega = request.POST.get("colonia_entrega")
            calle_entrega = request.POST.get("calle_entrega")
            numero_entrega = request.POST.get("numero_entrega")
            codigo_postal_entrega = request.POST.get("codigo_postal_entrega")
            
            estado_origen_id = request.POST.get("estado_origen_id")
            estado_destino_id = request.POST.get("estado_destino_id")
            
            # Validaciones
            if not descripcion:
                errors['descripcion'] = "La descripción es obligatoria."
            if not peso:
                errors['peso'] = "El peso es obligatorio."
            else:
                try:
                    peso = float(peso)
                    if peso <= 0:
                        errors['peso'] = "El peso debe ser un número positivo."
                except ValueError:
                    errors['peso'] = "El peso debe ser un número válido."
            if not remitente:
                errors['remitente'] = "El nombre del remitente es obligatorio."

            # Validar dirección de recolección
            if not colonia_recoleccion:
                errors['colonia_recoleccion'] = "La colonia de recolección es obligatoria."
            if not calle_recoleccion:
                errors['calle_recoleccion'] = "La calle de recolección es obligatoria."
            if not numero_recoleccion:
                errors['numero_recoleccion'] = "El número de recolección es obligatorio."
            if not codigo_postal_recoleccion:
                errors['codigo_postal_recoleccion'] = "El código postal de recolección es obligatorio."

            if not receptor:
                errors['receptor'] = "El nombre del receptor es obligatorio."

            # Validar dirección de entrega
            if not colonia_entrega:
                errors['colonia_entrega'] = "La colonia de entrega es obligatoria."
            if not calle_entrega:
                errors['calle_entrega'] = "La calle de entrega es obligatoria."
            if not numero_entrega:
                errors['numero_entrega'] = "El número de entrega es obligatorio."
            if not codigo_postal_entrega:
                errors['codigo_postal_entrega'] = "El código postal de entrega es obligatorio."

            if not estado_origen_id:
                errors['estado_origen_id'] = "Debe seleccionar un estado de origen."
            if not estado_destino_id:
                errors['estado_destino_id'] = "Debe seleccionar un estado de destino."

            if errors:
                raise ValueError("Hay errores en el formulario.")
            
            estado_origen = get_object_or_404(Estado, pk=estado_origen_id)
            estado_destino = get_object_or_404(Estado, pk=estado_destino_id)

            # Concatenar direcciones
            direccion_recoleccion = f"{calle_recoleccion} {numero_recoleccion}, Col. {colonia_recoleccion}, C.P. {codigo_postal_recoleccion}"
            direccion_entrega = f"{calle_entrega} {numero_entrega}, Col. {colonia_entrega}, C.P. {codigo_postal_entrega}"

            # Crear el paquete con estado inicial "Recolección"
            codigo = str(uuid.uuid4()).replace("-", "").upper()[:12]
            paquete = Paquete.objects.create(
                codigo=codigo,
                remitente=remitente,
                direccion_recoleccion=direccion_recoleccion,
                receptor=receptor,
                direccion_entrega=direccion_entrega,
                descripcion=descripcion,
                peso=peso,
                estado_actual=estado_origen,
                estado_paquete="Recolección",
                uusuario=usuario,
            )

            # Crear rutas
            frases = Frase.objects.all()
            if not frases.exists():
                raise Exception("No hay frases disponibles en la base de datos.")

            frases_list = list(frases)
            orden = 1
            rutas = []

            # Ruta 1: Recolección (siempre presente)
            frase_recoleccion, created = Frase.objects.get_or_create(frase="En Recolección")
            ruta_recoleccion = Ruta(
                paquete=paquete,
                frase=frase_recoleccion,
                estado_origen=estado_origen,
                estado_destino=estado_origen,
                orden=orden,
                activo=True,
                fecha_actualizacion=now(),
            )
            rutas.append(ruta_recoleccion)
            orden += 1

            # Si es envío local (mismo estado)
            if estado_origen == estado_destino:
                # Crear ruta de entrega local
                frase_entrega_local, created = Frase.objects.get_or_create(frase="En reparto local")
                ruta_entrega = Ruta(
                    paquete=paquete,
                    frase=frase_entrega_local,
                    estado_origen=estado_origen,
                    estado_destino=estado_destino,
                    orden=orden,
                    activo=False,
                    fecha_actualizacion=None,
                )
                rutas.append(ruta_entrega)
            else:
                # Lógica para envíos entre diferentes estados (tu código original modificado)
                estados_ruta = [estado_origen]
                
                # Obtener regiones de origen y destino
                regiones_origen = [region.strip() for region in estado_origen.region.split(',')]
                regiones_destino = [region.strip() for region in estado_destino.region.split(',')]

                # Obtener estados intermedios que conecten las regiones
                estados_intermedios = Estado.objects.exclude(pk__in=[estado_origen.pk, estado_destino.pk])
                filtros = Q()
                for region in regiones_origen + regiones_destino:
                    filtros |= Q(region__icontains=region)

                estados_intermedios = estados_intermedios.filter(filtros)
                estados_intermedios = list(set(estados_intermedios))

                if not estados_intermedios:
                    estados_intermedios = list(Estado.objects.exclude(pk__in=[estado_origen.pk, estado_destino.pk]))

                num_intermedias = min(2, len(estados_intermedios))
                if num_intermedias > 0:
                    estados_seleccionados = random.sample(estados_intermedios, num_intermedias)
                    estados_ruta.extend(estados_seleccionados)

                estados_ruta.append(estado_destino)

                # Crear rutas basadas en los estados de la ruta
                for i in range(len(estados_ruta) - 1):
                    estado_origen_ruta = estados_ruta[i]
                    estado_destino_ruta = estados_ruta[i + 1]
                    frase = random.choice(frases_list)
                    ruta = Ruta(
                        paquete=paquete,
                        frase=frase,
                        estado_origen=estado_origen_ruta,
                        estado_destino=estado_destino_ruta,
                        orden=orden,
                        activo=False,
                        fecha_actualizacion=None,
                    )
                    rutas.append(ruta)
                    orden += 1

            Ruta.objects.bulk_create(rutas)

            return render(
                request,
                "solicitar_envio.html",
                {
                    "success": True,
                    "codigo": paquete.codigo,
                    "estado_origen": estado_origen.nombre,
                    "estado_destino": estado_destino.nombre,
                    "peso": paquete.peso,
                    "descripcion": paquete.descripcion,
                    "remitente": paquete.remitente,
                    "direccion_recoleccion": direccion_recoleccion,
                    "receptor": paquete.receptor,
                    "direccion_entrega": direccion_entrega,
                    "estados": estados,
                },
            )
        except ValueError:
            return render(
                request,
                "solicitar_envio.html",
                {
                    "errors": errors,
                    "estados": estados,
                    "form_data": form_data,
                },
            )
        except Exception as e:
            error = f"Hubo un error al procesar tu solicitud: {e}"
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return render(
                request,
                "solicitar_envio.html",
                {
                    "error": error,
                    "estados": estados,
                    "form_data": form_data,
                },
            )

    return render(request, "solicitar_envio.html", {"estados": estados})

def acerca_de(request):
	return render(request, "acerca_de.html")

def FAQ(request):
	return render(request, "FAQ.html")

def puntos_atencion(request):
    return render(request, 'envios/puntos_atencion.html')


def login_usuario(request):
    if request.method == 'POST':
        email = request.POST['email']
        contraseña = request.POST['password']
        print(f"Intento login con email={email}")

        try:
            usuario = Usuario.objects.get(correo=email)
            print(f"Usuario encontrado: {usuario.nombre_usuario}")
            if check_password(contraseña, usuario.contraseña):
                print("Contraseña correcta")
                request.session['usuario_id'] = str(usuario._id)
                request.session['usuario_nombre'] = usuario.nombre_usuario
                messages.success(request, "Sesión iniciada.")
                return redirect('index')
            else:
                print("Contraseña incorrecta")
                messages.error(request, "Contraseña incorrecta.")
        except Usuario.DoesNotExist:
            print("Usuario no existe")
            messages.error(request, "El usuario no existe.")

    return render(request, 'login.html')

def registrar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['email']
        contraseña = request.POST['password1']
        confirmar_contraseña = request.POST['password2']

        if contraseña != confirmar_contraseña:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registro')

        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect('registro')

        usuario = Usuario(
            nombre_usuario=nombre,
            correo=correo,
            contraseña=make_password(contraseña)  # ← contraseña segura
        )
        usuario.save()
        messages.success(request, "Usuario registrado. Inicia sesión.")
        return redirect('login')

    return render(request, 'registro.html')

def logout_usuario(request):
    request.session.flush()
    messages.success(request, "Sesión cerrada.")
    return redirect('index')

def perfil_usuario(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    
    try:
        obj_id = ObjectId(request.session['usuario_id'])
        usuario = Usuario.objects.get(_id=obj_id)
    except (Usuario.DoesNotExist, Exception):
        logout_usuario(request)
        return redirect('login')

    if request.method == 'POST':
        # Procesar actualización de perfil
        nombre_usuario = request.POST.get('nombre_usuario')
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        try:
            usuario.nombre_usuario = nombre_usuario
            usuario.correo = correo
            
            if password:
                usuario.contraseña = make_password(password)
            
            usuario.save()
            request.session['usuario_nombre'] = nombre_usuario
            messages.success(request, "Perfil actualizado correctamente")
            return redirect('perfil')
        except Exception as e:
            messages.error(request, f"Error al actualizar perfil: {str(e)}")

    return render(request, 'perfil.html', {'usuario': usuario})

def eliminar_cuenta(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    
    if request.method == 'POST':
        try:
            obj_id = ObjectId(request.session['usuario_id'])
            usuario = Usuario.objects.get(_id=obj_id)
            Paquete.objects.filter(uusuario=usuario).update(uusuario=None)
            usuario.delete()
            logout_usuario(request)
            messages.success(request, "Tu cuenta ha sido eliminada permanentemente")
            return redirect('index')
        except Exception as e:
            messages.error(request, f"Error al eliminar cuenta: {str(e)}")
            return redirect('perfil')
    
    return redirect('perfil')