from django.http import Http404
from django.shortcuts import render

from .utils import listar_zonas_con_conteo, obtener_detalle_zona, resumen_por_zona


def vista_listado(request):
    """Muestra todas las zonas registradas (CA-01, CA-02)."""
    contexto = {'zonas': listar_zonas_con_conteo()}
    return render(request, 'monitor/listado.html', contexto)


def vista_detalle(request, zona_id):
    """
    Muestra el detalle de una zona: dispositivos, consumo total y estado.
    Si la zona no existe, responde 404 (CA-08).
    """
    detalle = obtener_detalle_zona(zona_id)
    if detalle is None:
        raise Http404(f"No existe una zona con id {zona_id}.")

    return render(request, 'monitor/detalle.html', {'zona': detalle})


def vista_resumen_zonas(request):
    """
    Muestra la vista general "Resumen de consumo por zona" (nuevo
    requerimiento Fase 2): tarjetas con los totales generales y una tabla
    con el resumen de cada zona. Toda la agregacion (conteos, sumas y
    estado) se calcula en utils.resumen_por_zona(); esta vista solo arma
    el contexto y renderiza la plantilla.
    """
    contexto = resumen_por_zona()
    return render(request, 'monitor/resumen_zonas.html', contexto)