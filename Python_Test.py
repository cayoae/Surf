import cv2
from ultralytics import YOLO
import os
import sys

def detectar_esqueleto(path_imagem):
    # 1. Verifica se o arquivo existe
    if not os.path.exists(path_imagem):
        print(f"\n[ERRO] O arquivo não foi encontrado: {path_imagem}")
        print("Verifique o caminho e tente novamente.")
        return

    print(f"\n[INFO] Carregando modelo e processando imagem...")

    # 2. Carrega o modelo YOLOv8 pré-treinado para Pose
    # 'yolov8n-pose.pt' é a versão 'nano' (mais leve e rápida).
    # Na primeira execução, ele fará o download automático do arquivo .pt
    try:
        model = YOLO('yolov8n-pose.pt')
    except Exception as e:
        print(f"[ERRO] Falha ao baixar ou carregar o modelo YOLO: {e}")
        return

    # 3. Roda a inferência na imagem
    # conf=0.5 significa que só queremos detecções com mais de 50% de certeza
    results = model(path_imagem, conf=0.5)

    # 4. Processa os resultados para visualização
    # results[0] é o resultado da primeira imagem (caso passássemos um lote)
    result_imagem = results[0]

    # Verifica se alguém foi detectado
    if len(result_imagem.keypoints) == 0:
         print("\n[AVISO] Nenhuma pessoa/esqueleto foi detectado na imagem.")
         # Mostra a imagem original mesmo sem detecção
         annotated_frame = cv2.imread(path_imagem)
    else:
        print(f"[INFO] Sucesso! Detectadas {len(result_imagem.keypoints)} pessoa(s).")
        # A função .plot() desenha automaticamente as caixas e o esqueleto (os 17 pontos COCO)
        annotated_frame = result_imagem.plot()

    # 5. Exibe a imagem resultante usando OpenCV
    nome_janela = "YOLOv8 Pose - Resultado (Pressione Q para sair)"
    cv2.namedWindow(nome_janela, cv2.WINDOW_NORMAL) # Permite redimensionar a janela
    cv2.imshow(nome_janela, annotated_frame)

    print("\n[ON-SCREEN] Veja a janela aberta com o resultado.")
    print("Pressione a tecla 'Q' na janela da imagem para fechar o script.")

    # Espera até que a tecla 'q' seja pressionada
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()

    # Opcional: Salvar a imagem no disco
    # nome_saida = "resultado_esqueleto.jpg"
    # cv2.imwrite(nome_saida, annotated_frame)
    # print(f"[INFO] Imagem salva como {nome_saida}")


if __name__ == "__main__":
    # Pede o caminho ao usuário no terminal
    # Exemplo de input Windows: C:\Users\SeuNome\Imagens\surfista.jpg
    # Exemplo de input Linux/Mac: /home/seunome/imagens/surfista.jpg
    print("--- Detector de Esqueleto 2D (YOLOv8 Pose) ---")
    user_path = input("Digite o caminho completo (full path) do arquivo JPG e aperte Enter:\n> ").strip()
    
    # Remove aspas que o Windows às vezes adiciona ao copiar caminho
    user_path = user_path.replace('"', '')
    
    detectar_esqueleto(user_path)