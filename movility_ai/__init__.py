# Copyright 2025 Google LLC
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

"""MovilityAI - Sistema multiagente de movilidad urbana inteligente para Medellín."""

import os

# Intentar configurar credenciales de Google Cloud (opcional para testing)
try:
    import google.auth
    _, project_id = google.auth.default()
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
except Exception:
    # En modo de testing o sin credenciales, usar valores por defecto
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "test-project")
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")

# Solo importar agent si no estamos en modo de testing
if not os.environ.get("TESTING"):
    try:
        from .agent import root_agent
        # Exportar el agente para que ADK lo encuentre
        __all__ = ["root_agent"]
    except ImportError:
        # ADK no disponible, probablemente en testing
        pass
