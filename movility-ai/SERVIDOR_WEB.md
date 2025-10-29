# 🌐 MovilityAI - Servidor Web ADK

## ✅ Servidor Activo

**URL:** http://127.0.0.1:8080

---

## 🎯 Cómo Usar la Interfaz

### 1. **Abrir en el navegador:**
   - Ve a: http://127.0.0.1:8080
   - La interfaz web de Google ADK se cargará automáticamente

### 2. **Seleccionar el agente:**
   - En la interfaz, selecciona **"movility-ai"**
   - Aparecerá un chat interactivo

### 3. **Consultas de ejemplo:**

#### Para PathFinder (Rutas):
```
¿Cómo llego del Centro a El Poblado?
Dame la ruta más rápida de Laureles a Universidad
Quiero ir en bici y metro combinados
```

#### Para FlowSense (Tráfico):
```
¿Cómo está el tráfico en Medellín ahora?
¿Habrá congestión en la Autopista Norte?
Muéstrame las zonas congestionadas
```

#### Para Insight (Analytics):
```
Dame un dashboard de movilidad
¿Cuáles son las zonas más críticas?
Muéstrame métricas de sostenibilidad
```

---

## 🔧 Solución de Problemas

### Si el agente no responde:

1. **Verifica que el servidor esté corriendo:**
   - Busca en la terminal: `Uvicorn running on http://127.0.0.1:8080`

2. **Revisa que la API key esté configurada:**
   - Archivo `.env` debe tener: `GOOGLE_API_KEY=tu_api_key`

3. **Consulta los logs:**
   - La terminal mostrará errores si algo falla

4. **Refresca la página:**
   - Presiona F5 en el navegador

---

## 🛑 Detener el Servidor

Presiona `CTRL+C` en la terminal donde está corriendo

---

## 📝 Notas

- El servidor tiene **auto-reload** activado
- Los cambios en el código se reflejan automáticamente
- Las sesiones se guardan en memoria

---

**🎊 ¡Sistema listo para la hackathon!**
