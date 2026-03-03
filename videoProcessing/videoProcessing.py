import cv2
import os

def extraer_fotogramas(video_path, output_dir, sparsity=1):
    """
    Extrae fotogramas de un video según la esparcidad indicada.
    
    :param video_path: Ruta al archivo de video de entrada.
    :param output_dir: Carpeta donde se guardarán los fotogramas.
    :param sparsity: 1 = todos, 2 = uno sí uno no, 3 = uno sí dos no, etc.
    """
    
    # 1. Crear la carpeta de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Carpeta '{output_dir}' creada exitosamente.")

    # 2. Cargar el video
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el video en {video_path}")
        return

    # Obtener el total de fotogramas (solo para información)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"El video tiene un total de {total_frames} fotogramas.")
    print(f"Extrayendo con sparsity={sparsity}...")

    frame_count = 0
    saved_count = 0

    # 3. Leer el video fotograma a fotograma
    while True:
        ret, frame = cap.read()
        
        # Si ret es False, significa que el video terminó o hubo un error
        if not ret:
            break
            
        # 4. Lógica de "Sparsity" (Esparcidad)
        # Solo guardamos el fotograma si es múltiplo de la variable sparsity
        if frame_count % sparsity == 0:
            # Generar el nombre del archivo (ej. frame_0000.jpg, frame_0002.jpg)
            nombre_archivo = f"frame_{frame_count:04d}.jpg"
            ruta_guardado = os.path.join(output_dir, nombre_archivo)
            
            # Guardar la imagen
            cv2.imwrite(ruta_guardado, frame)
            saved_count += 1
            
        frame_count += 1

    # 5. Liberar el video de la memoria
    cap.release()
    print(f"Proceso terminado. Se extrajeron y guardaron {saved_count} fotogramas en la carpeta '{output_dir}'.")

# ==========================================
# CONFIGURACIÓN Y EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # Cambia "mi_video.mp4" por el nombre real de tu archivo
    ruta_entrada = os.path.join("videoProcessing/video", "moose.mp4") 
    carpeta_salida = "videoProcessing/frames"
    
    # Define tu sparsity aquí:
    # 1 = Guarda todos los fotogramas
    # 2 = Guarda 1, ignora 1 (ej. frame 0, 2, 4...)
    # 3 = Guarda 1, ignora 2 (ej. frame 0, 3, 6...)
    esparcidad_deseada = 5
    
    extraer_fotogramas(ruta_entrada, carpeta_salida, sparsity=esparcidad_deseada)