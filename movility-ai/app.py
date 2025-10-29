"""
Servidor web para MovilityAI usando Gemini API directamente
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
CORS(app)  # Permitir CORS para el frontend

# Configurar Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Contexto del sistema
SYSTEM_CONTEXT = """Eres MovilityAI, un asistente inteligente de movilidad urbana para Medellín, Colombia.

CAPACIDADES:
🚇 PathFinder Agent: Planifica rutas óptimas usando Metro, buses y bicicletas
🚦 FlowSense Agent: Predice tráfico y sugiere rutas alternativas  
📊 Insight Agent: Analiza patrones de movilidad urbana
⚡ Pulse Agent: Monitorea tráfico en tiempo real
🌱 EcoTrack Agent: Calcula huella de carbono del transporte

DATOS DE MEDELLÍN:
- Metro: Tarifa $3,150 COP, horario 4:30 AM - 11:00 PM
- Líneas: Línea A (Niquía-La Estrella), Línea B (San Antonio-San Javier)
- Zonas principales: Poblado, Centro, Laureles, Envigado, Bello, Itagüí, Robledo, Belén
- Principales vías: La 10, La 33, La 80, Las Palmas, Regional, Guayabal, Autopista Sur
- Aeropuerto: José María Córdova (Rionegro)

FORMATO DE RESPUESTA:
- Usa emojis para mejor UX
- Sé conciso pero completo
- Proporciona alternativas cuando sea posible
- Incluye tiempos estimados
- Menciona costos cuando sea relevante

Responde de forma amigable y profesional."""

# Configurar modelo
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    generation_config={
        'temperature': 0.7,
        'max_output_tokens': 2000,
    }
)

@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "MovilityAI API Server",
        "version": "1.0.0",
        "endpoints": {
            "/generate": "POST - Generar respuesta",
            "/health": "GET - Estado del servidor"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "model": "gemini-2.0-flash-exp"})

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400
        
        user_prompt = data['prompt']
        
        # Crear chat con contexto
        chat = model.start_chat(history=[])
        
        # Enviar mensaje con contexto
        full_prompt = f"{SYSTEM_CONTEXT}\n\nUsuario pregunta: {user_prompt}"
        response = chat.send_message(full_prompt)
        
        return jsonify({
            "response": response.text,
            "model": "gemini-2.0-flash-exp",
            "status": "success"
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    print("🚀 MovilityAI Server")
    print("=" * 60)
    print(f"✅ Google API Key configurada")
    print(f"✅ Modelo: gemini-2.0-flash-exp")
    print()
    print("🌐 Servidor iniciando en http://localhost:8083")
    print("📱 Abre http://localhost:8090/app.html en tu navegador")
    print()
    print("⏹️  Presiona Ctrl+C para detener")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8083, debug=False)
