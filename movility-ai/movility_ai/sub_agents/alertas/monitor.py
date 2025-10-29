# Copyright 2025 MovilityAI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools para Agente Gestor de Contingencias - Web Scraping y Monitoreo"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

# Mock data de incidentes actuales (simula web scraping de redes sociales y APIs)
INCIDENTES_ACTIVOS_MOCK = [
    {
        "id": "INC001",
        "tipo": "accidente",
        "severidad": "grave",
        "ubicacion": "Autopista Sur, altura Est. Ayurá",
        "coordenadas": {"lat": 6.1679, "lon": -75.5863},
        "descripcion": "Colisión múltiple en carril izquierdo",
        "inicio": "2025-10-29T07:45:00",
        "duracion_estimada": 75,  # minutos
        "afectados_estimados": 15000,
        "fuente": "Twitter @sttmed",
        "estado": "activo",
        "vias_afectadas": ["Autopista Sur sentido sur", "Carrera 43A"],
    },
    {
        "id": "INC002",
        "tipo": "manifestacion",
        "severidad": "moderada",
        "ubicacion": "Plaza Botero - Centro",
        "coordenadas": {"lat": 6.2522, "lon": -75.5686},
        "descripcion": "Manifestación pacífica estudiantil",
        "inicio": "2025-10-29T09:00:00",
        "duracion_estimada": 180,  # 3 horas
        "afectados_estimados": 8000,
        "fuente": "El Colombiano",
        "estado": "activo",
        "vias_afectadas": ["Carrera 52 (Carabobo)", "Calle 52"],
    },
    {
        "id": "INC003",
        "tipo": "obra_vial",
        "severidad": "leve",
        "ubicacion": "Av. Las Palmas - Poblado",
        "coordenadas": {"lat": 6.2088, "lon": -75.5664},
        "descripcion": "Mantenimiento programado de vía",
        "inicio": "2025-10-29T06:00:00",
        "duracion_estimada": 480,  # 8 horas
        "afectados_estimados": 3000,
        "fuente": "Secretaría Movilidad",
        "estado": "activo",
        "vias_afectadas": ["Av. Las Palmas carril derecho"],
    },
]

# Mock data de alertas del Metro (simula API del Metro)
ALERTAS_METRO_MOCK = [
    {
        "id": "METRO001",
        "tipo": "contingencia_metro",
        "severidad": "informativa",
        "linea": "Linea A",
        "tramo": "Normal",
        "descripcion": "Servicio operando con normalidad",
        "inicio": "2025-10-29T05:00:00",
        "estado": "normal",
        "fuente": "@metrodemedellin",
    }
]

# Mock data de eventos masivos
EVENTOS_MASIVOS_MOCK = [
    {
        "id": "EVT001",
        "nombre": "Partido Atlético Nacional vs América",
        "lugar": "Estadio Atanasio Girardot",
        "fecha": "2025-10-29T19:30:00",
        "asistentes_esperados": 35000,
        "impacto_movilidad": "alto",
        "zonas_afectadas": ["Estadio", "Av. 70", "Av. 80"],
        "recomendacion": "Usar Metro, llegar 1 hora antes",
    }
]


def monitorear_redes_sociales(
    filtros: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Simula web scraping de redes sociales (@sttmed, @metrodemedellin).
    
    Args:
        filtros: Filtros opcionales (keywords, zonas, timeframe)
    
    Returns:
        Alertas y menciones relevantes de movilidad
    """
    # TODO: Implementar scraping real con APIs de Twitter/X
    # import tweepy
    # api = tweepy.API(auth)
    # tweets = api.user_timeline(screen_name='sttmed', count=50)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "fuentes_monitoreadas": ["@sttmed", "@metrodemedellin", "#MedellinAlerta"],
        "alertas_nuevas": 3,
        "alertas": [
            {
                "fuente": "@sttmed",
                "hora": "08:15 AM",
                "mensaje": "🚨 Accidente Autopista Sur altura Ayurá. Eviten la zona. Autoridades en el lugar.",
                "tipo": "accidente",
                "zona": "Autopista Sur",
            },
            {
                "fuente": "@metrodemedellin",
                "hora": "07:30 AM",
                "mensaje": "ℹ️ Servicio Metro operando con normalidad en todas las líneas. #MiMetro",
                "tipo": "info",
                "zona": "Todas",
            },
            {
                "fuente": "Twitter #MovilidadMed",
                "hora": "09:00 AM",
                "mensaje": "Manifestación en Centro. Cierres en Carabobo y Calle 52.",
                "tipo": "cierre_vial",
                "zona": "Centro",
            },
        ],
        "tendencias": ["#TransitoMed", "#AccidenteAutopistaSur"],
    }


def detectar_incidentes_activos(
    zona: Optional[str] = None,
    tipo: Optional[str] = None
) -> Dict[str, Any]:
    """
    Obtiene lista de incidentes activos en la ciudad.
    
    Args:
        zona: Filtrar por zona específica (Centro, Poblado, etc.)
        tipo: Filtrar por tipo (accidente, manifestacion, obra_vial, etc.)
    
    Returns:
        Lista de incidentes activos con detalles completos
    """
    incidentes = INCIDENTES_ACTIVOS_MOCK.copy()
    
    # Aplicar filtros
    if zona:
        incidentes = [i for i in incidentes if zona.lower() in i["ubicacion"].lower()]
    if tipo:
        incidentes = [i for i in incidentes if i["tipo"] == tipo]
    
    # Clasificar por severidad
    criticos = [i for i in incidentes if i["severidad"] == "critica"]
    graves = [i for i in incidentes if i["severidad"] == "grave"]
    moderados = [i for i in incidentes if i["severidad"] == "moderada"]
    leves = [i for i in incidentes if i["severidad"] == "leve"]
    
    return {
        "timestamp": datetime.now().isoformat(),
        "total_incidentes": len(incidentes),
        "por_severidad": {
            "criticos": len(criticos),
            "graves": len(graves),
            "moderados": len(moderados),
            "leves": len(leves),
        },
        "incidentes_activos": incidentes,
        "zona_mas_afectada": "Autopista Sur" if not zona else zona,
    }


def consultar_estado_metro() -> Dict[str, Any]:
    """
    Consulta estado actual del Metro de Medellín (todas las líneas).
    
    Returns:
        Estado operativo de cada línea, alertas y contingencias
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "estado_general": "NORMAL",
        "lineas": {
            "Linea_A": {
                "estado": "OPERATIVA",
                "estaciones_cerradas": [],
                "frecuencia": "4-6 minutos",
                "nota": "Servicio normal",
            },
            "Linea_B": {
                "estado": "OPERATIVA",
                "estaciones_cerradas": [],
                "frecuencia": "6-8 minutos",
                "nota": "Servicio normal",
            },
            "Metrocable_K": {
                "estado": "OPERATIVA",
                "estaciones_cerradas": [],
                "frecuencia": "10 minutos",
                "nota": "Servicio normal",
            },
            "Metrocable_J": {
                "estado": "OPERATIVA",
                "estaciones_cerradas": [],
                "frecuencia": "10 minutos",
                "nota": "Servicio normal",
            },
        },
        "alertas": ALERTAS_METRO_MOCK,
        "ultima_actualizacion": "2025-10-29T08:00:00",
        "fuente": "API Metro de Medellín",
    }


def generar_rutas_alternativas(
    incidente_id: str,
    origen: Optional[str] = None,
    destino: Optional[str] = None
) -> Dict[str, Any]:
    """
    Genera rutas alternativas para evitar zona de incidente.
    
    Args:
        incidente_id: ID del incidente a evitar
        origen: Punto de partida del usuario
        destino: Punto de llegada del usuario
    
    Returns:
        Rutas alternativas sugeridas con tiempo adicional estimado
    """
    # Buscar incidente
    incidente = next((i for i in INCIDENTES_ACTIVOS_MOCK if i["id"] == incidente_id), None)
    
    if not incidente:
        return {"error": "Incidente no encontrado"}
    
    return {
        "incidente": incidente["ubicacion"],
        "alternativas": [
            {
                "opcion": 1,
                "nombre": "Usar Metro Línea A + caminata",
                "descripcion": "Evitar Autopista Sur completamente",
                "tiempo_estimado": 45,
                "tiempo_adicional": 15,  # vs ruta normal
                "costo": 3150,
                "recomendacion": "Opción más confiable",
            },
            {
                "opcion": 2,
                "nombre": "Desvío por Avenida El Poblado",
                "descripcion": "Ruta vehicular alternativa",
                "tiempo_estimado": 38,
                "tiempo_adicional": 8,
                "costo": 15000,  # taxi
                "recomendacion": "Si vas en vehículo",
            },
            {
                "opcion": 3,
                "nombre": "Tomar Calle 10 vía Las Palmas",
                "descripcion": "Ruta más larga pero sin tráfico",
                "tiempo_estimado": 42,
                "tiempo_adicional": 12,
                "costo": 15000,
                "recomendacion": "Para evitar congestión",
            },
        ],
        "nota": "Tiempos actualizados según tráfico en tiempo real",
    }


def consultar_eventos_masivos(
    fecha: Optional[str] = None,
    zona: Optional[str] = None
) -> Dict[str, Any]:
    """
    Consulta eventos masivos programados que afectan movilidad.
    
    Args:
        fecha: Fecha a consultar (ISO format), None para hoy
        zona: Zona específica (Estadio, Centro, etc.)
    
    Returns:
        Lista de eventos con impacto en movilidad
    """
    eventos = EVENTOS_MASIVOS_MOCK.copy()
    
    if zona:
        eventos = [e for e in eventos if zona.lower() in e["lugar"].lower() or 
                  any(zona.lower() in z.lower() for z in e["zonas_afectadas"])]
    
    return {
        "fecha_consulta": fecha or datetime.now().date().isoformat(),
        "eventos_encontrados": len(eventos),
        "eventos": eventos,
        "recomendaciones_generales": [
            "Planifique su viaje con anticipación",
            "Use transporte público cuando sea posible",
            "Evite las zonas cercanas al evento 1 hora antes y después",
        ],
    }


# Exportar todas las tools
__all__ = [
    "monitorear_redes_sociales",
    "detectar_incidentes_activos",
    "consultar_estado_metro",
    "generar_rutas_alternativas",
    "consultar_eventos_masivos",
]
