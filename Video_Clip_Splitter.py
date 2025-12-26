"""
Video Clip Splitter - Separa surfistas em clips individuais
Detecta mudancas de cena e surfistas para criar clips de treino
"""
import cv2
from ultralytics import YOLO
import os
import numpy as np

# Configuracoes
VIDEO_INPUT = "pro_surfers_drops.mp4"
OUTPUT_FOLDER = "clips_treino"
MIN_CLIP_DURATION = 2.0  # segundos minimos por clip
MAX_CLIP_DURATION = 15.0  # segundos maximos por clip

# Threshold para detectar mudanca de cena
SCENE_CHANGE_THRESHOLD = 30.0  # diferenca media de pixels


def detect_scene_changes(video_path):
    """Detecta mudancas de cena no video"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    scene_changes = [0]  # Comeca no frame 0
    prev_frame = None
    frame_idx = 0

    print("[INFO] Detectando mudancas de cena...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Converter para escala de cinza e reduzir tamanho para performance
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (320, 180))

        if prev_frame is not None:
            # Calcular diferenca entre frames
            diff = cv2.absdiff(gray, prev_frame)
            mean_diff = np.mean(diff)

            # Se diferenca grande, eh mudanca de cena
            if mean_diff > SCENE_CHANGE_THRESHOLD:
                # Verificar se nao esta muito perto da ultima mudanca
                last_change_time = scene_changes[-1] / fps
                current_time = frame_idx / fps

                if current_time - last_change_time >= MIN_CLIP_DURATION:
                    scene_changes.append(frame_idx)
                    print(f"  Cena detectada no frame {frame_idx} ({current_time:.1f}s)")

        prev_frame = gray
        frame_idx += 1

        # Progress
        if frame_idx % 500 == 0:
            print(f"  Analisando frame {frame_idx}...")

    cap.release()

    # Adicionar frame final
    scene_changes.append(frame_idx)

    return scene_changes, fps


def has_surfer(model, frame):
    """Verifica se ha surfista detectado no frame"""
    results = model(frame, conf=0.3, verbose=False)

    for result in results:
        if result.keypoints is not None and len(result.keypoints) > 0:
            # Verificar se tem keypoints suficientes detectados
            for kpts in result.keypoints.xy:
                keypoints = kpts.cpu().numpy()
                valid_points = sum(1 for kpt in keypoints if kpt[0] > 0 and kpt[1] > 0)
                if valid_points >= 8:  # Pelo menos 8 pontos do corpo visiveis
                    return True
    return False


def extract_clips(video_path, scene_changes, fps, output_folder):
    """Extrai clips baseado nas mudancas de cena"""

    # Criar pasta de saida
    os.makedirs(output_folder, exist_ok=True)

    # Carregar modelo
    print("[INFO] Carregando modelo YOLOv8-Pose...")
    model = YOLO('yolov8n-pose.pt')

    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    clip_count = 0
    valid_clips = []

    print(f"\n[INFO] Processando {len(scene_changes)-1} possiveis clips...")

    for i in range(len(scene_changes) - 1):
        start_frame = scene_changes[i]
        end_frame = scene_changes[i + 1]

        duration = (end_frame - start_frame) / fps

        # Pular clips muito curtos ou muito longos
        if duration < MIN_CLIP_DURATION:
            continue
        if duration > MAX_CLIP_DURATION:
            end_frame = start_frame + int(MAX_CLIP_DURATION * fps)
            duration = MAX_CLIP_DURATION

        # Verificar se tem surfista no clip (checar alguns frames)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame + int(fps))  # 1 segundo depois do inicio
        ret, test_frame = cap.read()

        if ret and has_surfer(model, test_frame):
            clip_count += 1

            # Nome do arquivo
            clip_name = f"clip_{clip_count:03d}_frame{start_frame}_dur{duration:.1f}s.mp4"
            clip_path = os.path.join(output_folder, clip_name)

            print(f"\n[CLIP {clip_count}] Extraindo: {clip_name}")
            print(f"  Frames: {start_frame} -> {end_frame} ({duration:.1f}s)")

            # Configurar writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(clip_path, fourcc, fps, (width, height))

            # Voltar para o inicio do clip
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            frames_written = 0
            while cap.get(cv2.CAP_PROP_POS_FRAMES) < end_frame:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
                frames_written += 1

            out.release()

            valid_clips.append({
                'name': clip_name,
                'path': clip_path,
                'start_frame': start_frame,
                'end_frame': end_frame,
                'duration': duration,
                'start_time': start_frame / fps,
                'end_time': end_frame / fps
            })

            print(f"  Salvo: {frames_written} frames")
        else:
            print(f"  Pulando cena {i+1} (sem surfista detectado)")

    cap.release()
    return valid_clips


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(script_dir, VIDEO_INPUT)
    output_folder = os.path.join(script_dir, OUTPUT_FOLDER)

    # Verificar se video existe
    if not os.path.exists(video_path):
        print(f"[ERRO] Video nao encontrado: {video_path}")
        return

    print("=" * 60)
    print("  Video Clip Splitter - Surf Training Data")
    print("=" * 60)
    print(f"\nVideo: {VIDEO_INPUT}")
    print(f"Output: {OUTPUT_FOLDER}/")
    print(f"Min duracao: {MIN_CLIP_DURATION}s")
    print(f"Max duracao: {MAX_CLIP_DURATION}s")
    print()

    # Passo 1: Detectar mudancas de cena
    scene_changes, fps = detect_scene_changes(video_path)
    print(f"\n[INFO] {len(scene_changes)-1} potenciais cenas detectadas")

    # Passo 2: Extrair clips com surfistas
    valid_clips = extract_clips(video_path, scene_changes, fps, output_folder)

    # Resumo
    print("\n" + "=" * 60)
    print("  RESUMO")
    print("=" * 60)
    print(f"\nClips extraidos: {len(valid_clips)}")
    print(f"Salvos em: {output_folder}/")
    print("\nLista de clips:")

    for clip in valid_clips:
        print(f"  - {clip['name']}")
        print(f"    Tempo: {clip['start_time']:.1f}s - {clip['end_time']:.1f}s")

    # Salvar indice
    index_path = os.path.join(output_folder, "clips_index.txt")
    with open(index_path, 'w') as f:
        f.write("# Clips de Treino - Surf Analyzer\n")
        f.write(f"# Video fonte: {VIDEO_INPUT}\n")
        f.write(f"# Total clips: {len(valid_clips)}\n\n")

        for clip in valid_clips:
            f.write(f"{clip['name']}\n")
            f.write(f"  start_time: {clip['start_time']:.2f}\n")
            f.write(f"  end_time: {clip['end_time']:.2f}\n")
            f.write(f"  duration: {clip['duration']:.2f}\n\n")

    print(f"\nIndice salvo em: {index_path}")


if __name__ == "__main__":
    main()
