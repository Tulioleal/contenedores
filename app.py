from flask import Flask
import os
import redis

# --- Configuración a través de Variables de Entorno ---
# Puerto de la aplicación (por defecto 5000)
APP_PORT = int(os.environ.get('APP_PORT', 5000))
# Host de Redis (debe coincidir con el nombre del servicio, por defecto 'redis')
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
# Puerto de Redis (por defecto 6379)
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
# Contraseña de Redis (None si no hay)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

app = Flask(__name__)

# --- Conexión a Redis ---
try:
    # Intenta conectarse a Redis al inicio
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    r.ping()
    print(f"Conexión exitosa a Redis en {REDIS_HOST}:{REDIS_PORT}")
except redis.exceptions.ConnectionError as e:
    r = None
    print(f"ERROR: No se pudo conectar a Redis: {e}")

@app.route('/')
def hello():
    hostname = os.environ.get('HOSTNAME', 'unknown')
    
    visit_count = 'N/A'
    if r:
        try:
            # Incrementa el contador de visitas
            visit_count = r.incr('visits')
        except Exception as e:
            visit_count = f"Error al contar: {e}"
            
    return f'''
    <h1>¡Hola desde Docker! 🐳</h1>
    <p>Container ID: **{hostname}**</p>
    <p>Has visitado esta página **{visit_count}** veces (Contador con Redis)</p>
    <p>Esta aplicación está corriendo en el puerto **{APP_PORT}**.</p>
    '''

# Endpoint de Health Check
@app.route('/health')
def health_check():
    # Verifica si la conexión a Redis es funcional.
    if r and r.ping():
        return "OK - Redis OK", 200
    else:
        # Esto puede indicar un problema de conexión con Redis
        return "ERROR: Redis no disponible", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_PORT)