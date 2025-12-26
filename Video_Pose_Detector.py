"""
Video Pose Detector - Detecta esqueleto com YOLOv8-Pose
Processa video e salva com overlay de keypoints + esqueleto em vermelho
"""
import cv2
from ultralytics import YOLO
import os

# Configuracoes
VIDEO_INPUT = "mick_fanning_slowmo.mp4"
VIDEO_OUTPUT = "mick_fanning_detected.mp4"

# Limite de tempo para teste (em segundos)
START_SECOND = 15  # Comecar no segundo 15
END_SECOND = 30    # Terminar no segundo 30

# Cor vermelho em BGR (OpenCV usa BGR, nao RGB)
RED = (0, 0, 255)
KEYPOINT_RADIUS = 5
LINE_THICKNESS = 2

# Conexoes do esqueleto (indices dos keypoints COCO)
# 0=nariz, 1-2=olhos, 3-4=orelhas, 5-6=ombros, 7-8=cotovelos,
# 9-10=pulsos, 11-12=quadris, 13-14=joelhos, 15-16=tornozelos
SKELETON_CONNECTIONS = [
    (5, 6),             # ombro a ombro
    (5, 7), (7, 9),     # braco esquerdo (ombro -> cotovelo -> pulso)
    (6, 8), (8, 10),    # braco direito
    (5, 11), (6, 12),   # tronco (ombros -> quadris)
    (11, 12),           # quadril a quadril
    (11, 13), (13, 15), # perna esquerda (quadril -> joelho -> tornozelo)
    (12, 14), (14, 16), # perna direita
]


def processar_video():
    # Caminho absoluto do diretorio do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(script_dir, VIDEO_INPUT)
    output_path = os.path.join(script_dir, VIDEO_OUTPUT)

    # Verifica se o video existe
    if not os.path.exists(video_path):
        print(f"[ERRO] Video nao encontrado: {video_path}")
        return

    print(f"[INFO] Carregando modelo YOLOv8-Pose...")
    model = YOLO('yolov8n-pose.pt')

    print(f"[INFO] Abrindo video: {video_path}")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("[ERRO] Nao foi possivel abrir o video")
        return

    # Propriedades do video
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calcular frames de inicio e fim
    start_frame = int(fps * START_SECOND)
    end_frame = int(fps * END_SECOND)
    frames_to_process = end_frame - start_frame

    print(f"[INFO] Video: {width}x{height} @ {fps:.1f} FPS")
    print(f"[INFO] Processando do segundo {START_SECOND} ao {END_SECOND} ({frames_to_process} frames)")

    # Pular para o frame inicial
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    print(f"[INFO] Pulando para frame {start_frame}...")

    # Configurar VideoWriter para salvar
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        print("[ERRO] Nao foi possivel criar o arquivo de saida")
        cap.release()
        return

    print(f"[INFO] Iniciando processamento...")
    print("-" * 40)

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Parar se atingiu o frame final
        current_frame = start_frame + frame_count
        if current_frame >= end_frame:
            print(f"[INFO] Segundo {END_SECOND} atingido")
            break

        # Rodar YOLO Pose detection
        results = model(frame, conf=0.5, verbose=False)

        # Processar cada pessoa detectada
        for result in results:
            if result.keypoints is not None and len(result.keypoints) > 0:
                # Iterar sobre cada pessoa detectada
                for person_idx, kpts in enumerate(result.keypoints.xy):
                    keypoints = kpts.cpu().numpy()

                    # Desenhar linhas do esqueleto primeiro (para ficarem atras dos pontos)
                    for (i, j) in SKELETON_CONNECTIONS:
                        if i < len(keypoints) and j < len(keypoints):
                            pt1 = keypoints[i]
                            pt2 = keypoints[j]

                            # Verifica se ambos os pontos foram detectados (x,y > 0)
                            if pt1[0] > 0 and pt1[1] > 0 and pt2[0] > 0 and pt2[1] > 0:
                                x1, y1 = int(pt1[0]), int(pt1[1])
                                x2, y2 = int(pt2[0]), int(pt2[1])
                                cv2.line(frame, (x1, y1), (x2, y2), RED, LINE_THICKNESS)

                    # Desenhar circulos nos keypoints
                    for kpt in keypoints:
                        x, y = int(kpt[0]), int(kpt[1])
                        # So desenha se o ponto foi detectado
                        if x > 0 and y > 0:
                            cv2.circle(frame, (x, y), KEYPOINT_RADIUS, RED, -1)

        # Salvar frame processado
        out.write(frame)

        # Mostrar progresso a cada 10 frames
        if frame_count % 10 == 0:
            progress = (frame_count / frames_to_process) * 100
            print(f"Frame {frame_count}/{frames_to_process} ({progress:.0f}%)", flush=True)

    # Liberar recursos
    cap.release()
    out.release()

    print(f"\n[SUCESSO] Video salvo em: {output_path}")
    print(f"[INFO] Total de frames processados: {frame_count}")


if __name__ == "__main__":
    print("=" * 50)
    print("  Video Pose Detector - YOLOv8")
    print("=" * 50)
    processar_video()
