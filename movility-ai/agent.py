"""
Punto de entrada para el servidor web de ADK.
Este archivo exporta el agente raíz para que ADK lo pueda descubrir.
"""
import sys
import os
from pathlib import Path

# Agregar el directorio del módulo movility_ai al path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent

# Agregar ambos directorios al path
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(current_dir))

# Cambiar al directorio correcto para las importaciones
os.chdir(str(parent_dir))

# Importar el agente raíz del módulo principal
from movility_ai.agent import root_agent as main_root_agent

# Exportar como root_agent para que ADK lo encuentre
root_agent = main_root_agent

__all__ = ['root_agent']
