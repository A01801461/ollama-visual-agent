import ollama
import os

# 1. Configuración
MODELO = "qwen3.5:4b"  # Asegúrate de usar el modelo que tengas instalado
CARPETA = "./imagenes"
# PROMPT = "Describe detalladamente qué ves en esta imagen."
PROMPT = "Di lo mas rapido que puedas lo qué ves en esta imagen."

if not os.path.exists(CARPETA):
    os.makedirs(CARPETA)
    print(f"Carpeta '{CARPETA}' creada. Por favor coloca tus imágenes ahí.")
    exit()

archivos = os.listdir(CARPETA)
imagenes = [f for f in archivos if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

if not imagenes:
    print("No encontré imágenes en la carpeta.")
    exit()

print(f"Procesando {len(imagenes)} imágenes con {MODELO}...\n")

for imagen in imagenes:
    ruta_completa = os.path.join(CARPETA, imagen)
    print(f"--- Analizando: {imagen} ---")

    try:
        # Llamada al modelo
        response = ollama.chat(
            model=MODELO,
            messages=[{
                'role': 'user',
                'content': PROMPT,
                'images': [ruta_completa]
            }]
        )
        
        # --- Obtención de Métricas ---
        # Ollama devuelve los tiempos en nanosegundos (1s = 1,000,000,000 ns)
        # 1. Tiempo total de la inferencia (carga + prompt + generación)
        tiempo_total_s = response['total_duration'] / 1e9
        
        # 2. Tokens generados (respuesta del modelo)
        tokens_generados = response['eval_count']
        
        # 3. Velocidad de generación (Tokens por segundo)
        # Se calcula usando 'eval_duration' (tiempo dedicado solo a generar texto)
        tiempo_generacion_s = response['eval_duration'] / 1e9
        tokens_por_segundo = tokens_generados / tiempo_generacion_s if tiempo_generacion_s > 0 else 0

        # --- Imprimir Resultados ---
        print("\nDESCRIPCIÓN:")
        print(response['message']['content'])
        print("\n" + "="*40)
        print(f"📊 ESTADÍSTICAS DE RENDIMIENTO:")
        print(f"⏱️  Tiempo total:      {tiempo_total_s:.2f} s")
        print(f"📝 Tokens generados:  {tokens_generados}")
        print(f"🚀 Velocidad:         {tokens_por_segundo:.2f} tokens/s")
        print("="*40 + "\n")

    except Exception as e:
        print(f"Error con la imagen {imagen}: {e}")