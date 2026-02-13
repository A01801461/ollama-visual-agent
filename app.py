import ollama
import os

# 1. Configuración
# Ajusta el nombre según el modelo que tengas instalado (ej. qwen2.5-vl, llama3.2-vision, qwen3-vl)
MODELO = "qwen3-vl:2b" 
CARPETA = "./imagenes"
#PROMPT = "Describe detalladamente qué ves en esta imagen."
PROMPT = "Di lo mas rapido que puedas lo que ves en la imagen."

# Crear la carpeta si no existe para evitar errores
if not os.path.exists(CARPETA):
    os.makedirs(CARPETA)
    print(f"Carpeta '{CARPETA}' creada. Por favor coloca tus imágenes ahí.")
    exit()

# 2. Obtener lista de imágenes
archivos = os.listdir(CARPETA)
imagenes = [f for f in archivos if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

if not imagenes:
    print("No encontré imágenes en la carpeta.")
    exit()

# 3. Procesar cada imagen
print(f"Procesando {len(imagenes)} imágenes con {MODELO}...\n")

for imagen in imagenes:
    ruta_completa = os.path.join(CARPETA, imagen)
    print(f"--- Analizando: {imagen} ---")

    try:
        response = ollama.chat(
            model=MODELO,
            messages=[{
                'role': 'user',
                'content': PROMPT,
                'images': [ruta_completa] # Ollama lee la ruta del archivo directamente
            }]
        )
        
        # Imprimir resultado
        print(response['message']['content'])
        print("-" * 30 + "\n")

    except Exception as e:
        print(f"Error con la imagen {imagen}: {e}")