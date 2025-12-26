# Projeto: AI Surf Coach - Análise Biomecânica Comparativa

**Versão:** 1.0  
**Status:** Planejamento Técnico  
**Core Tech:** Computer Vision, Deep Learning, Signal Processing

---

## 1. Resumo Executivo
O **AI Surf Coach** é um sistema de visão computacional projetado para democratizar o coaching de elite. O sistema utiliza vídeos de surfistas profissionais para criar um "Golden Standard" biomecânico. Ao receber o vídeo de um usuário amador, o sistema sincroniza temporalmente os movimentos e projeta um "Ghost Overlay" (esqueleto do profissional) sobre o vídeo do usuário, destacando visualmente onde a postura, compressão ou rotação diferem do ideal.

---

## 2. Fluxo do Usuário (User Journey)

1.  **Upload:** O usuário envia um vídeo de uma manobra (ex: "Cutback de Frontside").
2.  **Identificação:** O sistema detecta o surfista e classifica a manobra.
3.  **Processamento:**
    * O sistema busca no banco de dados a execução perfeita daquela manobra por um Pro.
    * Alinha a velocidade do Pro para coincidir com a velocidade do usuário (Sync).
    * Ajusta a altura e proporções do esqueleto do Pro para o corpo do usuário.
4.  **Feedback Visual (Output):**
    * O usuário vê seu vídeo com um esqueleto translúcido (Ghost) sobreposto.
    * Linhas vermelhas aparecem onde o erro é crítico (ex: braço muito baixo, falta de flexão).
    * Dashboard com métricas: "Velocidade de Entrada", "Ângulo de Ataque", "Score de Fluidez".

---

## 3. Arquitetura Técnica

### Fase A: Ingestão e Treinamento (O "Golden Standard")
*Objetivo: Criar uma biblioteca vetorial de movimentos perfeitos.*

1.  **Coleta de Dados:** Curadoria de vídeos da WSL/Free Surf em alta resolução (4k/60fps).
2.  **Pose Extraction (YOLOv8-Pose):**
    * Extração de 17 keypoints (COCO Format) frame a frame.
    * *Output:* Array de vetores `(x, y, confidence)` por frame.
3.  **Lifting 3D (VideoPose3D):**
    * Conversão de coordenadas 2D para 3D `(x, y, z)` para mitigar diferenças de ângulo de câmera.
4.  **Normalização:**
    * Translação: Centralizar o quadril no ponto (0,0,0).
    * Escala: Normalizar altura do esqueleto para 1.0 unidade.
5.  **Armazenamento:** Salvar a sequência temporal normalizada em um Banco Vetorial (ex: FAISS ou JSON estruturado) rotulado por manobra.

### Fase B: A Engine de Comparação (O Core)
*Objetivo: Comparar matematicamente o Amador vs. Pro.*

1.  **Pose Extraction (Usuário):** Mesmo processo da Fase A.
2.  **Alinhamento Temporal (DTW - Dynamic Time Warping):**
    * *Problema:* O Pro faz a cavada em 0.5s; o Amador leva 1.2s. A comparação frame-a-frame falharia.
    * *Solução:* O algoritmo DTW encontra o caminho ideal de alinhamento, "esticando" o tempo do Pro para casar com os picos de movimento do usuário.
3.  **Cálculo de Delta (Erro):**
    * Calcular a distância Euclidiana ou Cosine Similarity entre os vetores de juntas (ombros, joelhos) sincronizados.
    * Se `Erro > Limiar`, marcar frame como "Correção Necessária".

### Fase C: Renderização e UI
1.  **Projeção do Ghost:**
    * Pegar o esqueleto 3D do Pro (já sincronizado).
    * Reprojetar para 2D usando a perspectiva da câmera do usuário.
    * Desenhar sobre o frame original com opacidade 50%.
2.  **Highlight de Erro:**
    * Usar gradiente de cor: Verde (Alinhado) -> Vermelho (Desalinhado).

---

## 4. Stack Tecnológico Sugerido

| Área | Tecnologia | Justificativa |
| :--- | :--- | :--- |
| **Linguagem** | Python 3.9+ | Padrão industrial para Data Science/CV. |
| **CV Model** | **YOLOv8-Pose** (Ultralytics) | Rápido, robusto a oclusões (água/espuma) e fácil implementação. |
| **3D Math** | **VideoPose3D** (Facebook) | Essencial para comparar ângulos de filmagem diferentes. |
| **Sync Algo** | **FastDTW** (Python Lib) | Biblioteca eficiente para alinhamento temporal de séries. |
| **Backend** | FastAPI | Para servir o modelo como API. |
| **Frontend** | Streamlit (MVP) / React | Visualização rápida para validar o produto. |
| **Processamento** | OpenCV + NumPy | Manipulação de imagem e cálculo vetorial. |

---

## 5. Dicionário de Métricas (Biomecânica do Surf)

Para o MVP, focaremos em 3 métricas críticas:

1.  **Compression Ratio (Compressão):**
    * *Definição:* Ângulo interno do joelho no ponto mais baixo da cavada (Bottom Turn).
    * *Fórmula:* Ângulo entre vetores (Quadril-Joelho) e (Joelho-Tornozelo).
    * *Feedback:* "Dobre mais os joelhos para gerar projeção."

2.  **Torque (Rotação de Tronco):**
    * *Definição:* Diferença angular entre a linha dos ombros e a linha da prancha/quadril.
    * *Importância:* Define a radicalidade da manobra no Top Turn.

3.  **Gaze (Foco Visual):**
    * *Definição:* Vetor da cabeça (Nariz-Orelhas).
    * *Regra:* "Para onde você olha é para onde você vai". O sistema verifica se o usuário está olhando para o lip ou para a base.

---

## 6. Roadmap de Implementação

### Sprint 1: Prova de Conceito (PoC)
- [ ] Script Python simples (input imagem -> output esqueleto desenhado).
- [ ] Cálculo estático de ângulo de joelho em 1 imagem.

### Sprint 2: Análise de Vídeo (Single)
- [ ] Processar vídeo completo frame-a-frame.
- [ ] Plotar gráfico de variação do ângulo do joelho ao longo do tempo.

### Sprint 3: O "Ghost" (Diferencial)
- [ ] Implementar DTW para sincronizar dois vídeos.
- [ ] Gerar vídeo de saída com o esqueleto do Pro sobreposto ao do amador.

### Sprint 4: Interface
- [ ] Criar WebApp onde usuário faz upload e vê o resultado lado a lado.