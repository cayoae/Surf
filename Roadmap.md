# Surf Analyzer - Roadmap & Checklist

**Versao:** 2.0
**Status:** Em Desenvolvimento
**Inicio:** Dezembro 2024

---

## Visao Geral

Sistema de analise de surf usando IA que:
1. Classifica o nivel do surfista (Beginner/Intermediate)
2. Detecta erros de tecnica
3. Sobrepoe "Ghost" do movimento ideal para comparacao visual
4. Gera feedback personalizado

---

## Arquitetura do Sistema

```
Usuario faz Upload
        |
        v
+------------------+
|  VIDEO ANALYSIS  |
+------------------+
        |
        v
+------------------+     +------------------+
| YOLO Detection   |---->| Wave Detection   |
| - Surfista       |     | - Bounding box   |
| - Pose (17 kpts) |     | - Pocket zone    |
| - Prancha        |     | - Whitewash      |
+------------------+     +------------------+
        |
        v
+------------------+
| PHASE DETECTION  |
| Remada -> Drop   |
| -> Bottom Turn   |
| -> Trim          |
+------------------+
        |
        v
+------------------+
| LEVEL CLASSIFIER |
| Beginner or      |
| Intermediate     |
+------------------+
        |
        v
+------------------+
| SYNC & OVERLAY   |
| T=0 no drop      |
| Ghost do modelo  |
| ideal sobreposto |
+------------------+
        |
        v
+------------------+
|  OUTPUT VIDEO    |
| + Feedback texto |
+------------------+
```

---

## Sistema de Classificacao de Niveis

### Beginner (L1-L2)
| Criterio | Valor |
|----------|-------|
| Experiencia | < 20 horas |
| Ondas | Whitewash, < 1ft |
| Pop-up | Inconsistente, > 2 segundos |
| Manobras | Nenhuma |
| Foco do Sistema | Remada, Pop-up, Equilibrio |

### Intermediate (L3)
| Criterio | Valor |
|----------|-------|
| Experiencia | 40+ sessoes |
| Ondas | 2-3ft, ondas verdes |
| Pop-up | Consistente, < 1.5 segundos |
| Manobras | Bottom turn, Cutback |
| Foco do Sistema | Bottom turn, Trim, Leitura de onda |

### Metricas para Classificacao Automatica

```python
# BEGINNER detectado quando:
- pop_up_time > 2.0 segundos
- head_angle > 30 graus (olhando para baixo)
- knee_angle > 150 graus (pernas retas)
- keypoint_variance > threshold (instavel)
- no_bottom_turn_detected == True

# INTERMEDIATE detectado quando:
- pop_up_time < 1.5 segundos
- head_angle < 20 graus (olhando para frente)
- knee_angle entre 90-120 graus
- keypoint_variance < threshold (estavel)
- bottom_turn_detected == True
```

---

## Fases do Surf para Analise

### Para Beginner
1. **Remada** - Posicao deitado, bracadas
2. **Pop-up/Drop** - Levantar na prancha
3. **Equilibrio** - Stance, centro de gravidade

### Para Intermediate
1. **Drop** (refinamento)
2. **Bottom Turn** - Curva na base da onda
3. **Trim** - Manter linha na face

---

## Erros Comuns para Detectar

### Beginner
| Erro | Deteccao (Keypoints) | Feedback |
|------|---------------------|----------|
| Olhar para baixo | angulo cabeca > 30 graus | "Olhe para onde quer ir" |
| Corpo muito alto | pouca compressao quadril-tornozelo | "Abaixe mais, flexione joelhos" |
| Pop-up lento | tempo > 2s | "Pratique explosao no pop-up" |
| Stance errado | pes muito juntos/separados | "Ajuste posicao dos pes" |
| Bracos soltos | bracos longe do corpo | "Use bracos para equilibrio" |

### Intermediate
| Erro | Deteccao (Keypoints) | Feedback |
|------|---------------------|----------|
| Overturning | mudanca brusca + queda | "Curvas mais suaves" |
| Digging rail | inclinacao excessiva | "Menos inclinacao lateral" |
| Peso atras | centro massa deslocado | "Distribua peso no centro" |
| Sem compressao | joelho > 140 graus na curva | "Comprima antes da curva" |
| Timing errado | bottom turn muito tarde | "Inicie curva mais cedo" |

---

## CHECKLIST DE IMPLEMENTACAO

### FASE 1: Infraestrutura Base
- [x] Setup do repositorio Git
- [x] Conectar GitHub com Netlify
- [x] Criar landing page basica
- [ ] Configurar Supabase (banco + storage)
- [ ] Criar estrutura de pastas do projeto

### FASE 2: Coleta de Dados (Golden Standard)
- [ ] Criar lista de manobras para coletar
  - [ ] Remada
  - [ ] Pop-up/Drop
  - [ ] Bottom turn frontside
  - [ ] Bottom turn backside
  - [ ] Trim
- [ ] Coletar videos de profissionais (WSL, tutoriais)
  - [ ] Minimo 10 videos por manobra
  - [ ] Resolucao minima 720p
  - [ ] Angulos variados (lateral, frontal)
- [ ] Coletar videos de instrutores demonstrando tecnica
- [ ] Organizar videos por nivel e manobra

### FASE 3: Modelo de Deteccao de Onda
- [ ] Pesquisar datasets de ondas existentes
- [ ] Anotar dataset proprio (se necessario)
  - [ ] Bounding box da onda
  - [ ] Zona do "pocket"
  - [ ] Whitewash
- [ ] Treinar YOLOv8 customizado para ondas
- [ ] Testar e validar deteccao

### FASE 4: Pose Extraction & Normalizacao
- [ ] Implementar extracao de pose com YOLOv8-Pose
- [ ] Salvar keypoints por frame (JSON/CSV)
- [ ] Implementar normalizacao:
  - [ ] Centralizar quadril em (0,0)
  - [ ] Normalizar escala (altura = 1.0)
- [ ] Opcional: Lifting 3D com VideoPose3D

### FASE 5: Deteccao de Fase
- [ ] Definir criterios para cada fase:
  - [ ] Remada: surfista deitado, atras da onda
  - [ ] Drop: transicao deitado -> em pe
  - [ ] Bottom turn: na base da onda, curvando
  - [ ] Trim: na face da onda, horizontal
- [ ] Implementar classificador de fase
- [ ] Testar com videos diversos

### FASE 6: Classificador de Nivel
- [ ] Implementar calculo de metricas:
  - [ ] Tempo de pop-up
  - [ ] Angulo do joelho
  - [ ] Angulo da cabeca (olhar)
  - [ ] Variancia dos keypoints (estabilidade)
  - [ ] Deteccao de bottom turn
- [ ] Definir thresholds para cada nivel
- [ ] Treinar/ajustar classificador
- [ ] Validar com videos reais

### FASE 7: Biblioteca de Movimentos Ideais
- [ ] Processar videos de profissionais
- [ ] Extrair poses normalizadas por fase
- [ ] Criar "pose media ideal" para cada:
  - [ ] Beginner: Remada ideal
  - [ ] Beginner: Pop-up ideal
  - [ ] Beginner: Stance ideal
  - [ ] Intermediate: Bottom turn ideal
  - [ ] Intermediate: Trim ideal
- [ ] Armazenar em banco vetorial (FAISS ou JSON)

### FASE 8: Sincronizacao Temporal (DTW)
- [ ] Implementar Dynamic Time Warping
- [ ] Definir T=0 como momento do drop
- [ ] Alinhar video do usuario com modelo ideal
- [ ] Testar sincronizacao com casos diversos

### FASE 9: Sistema de Overlay (Ghost)
- [ ] Implementar projecao do esqueleto ideal
- [ ] Sistema de cores:
  - [ ] Verde = alinhado com ideal
  - [ ] Amarelo = pequeno desvio
  - [ ] Vermelho = erro critico
- [ ] Ajustar opacidade do ghost
- [ ] Renderizar video final com overlay

### FASE 10: Sistema de Feedback
- [ ] Criar banco de mensagens de feedback
- [ ] Mapear erros -> mensagens especificas
- [ ] Implementar geracao de relatorio:
  - [ ] Nivel detectado
  - [ ] Erros encontrados
  - [ ] Sugestoes de melhoria
  - [ ] Score geral

### FASE 11: Backend API
- [ ] Criar API com FastAPI
- [ ] Endpoints:
  - [ ] POST /upload - receber video
  - [ ] GET /status/{id} - status processamento
  - [ ] GET /result/{id} - video + feedback
- [ ] Integrar com Supabase Storage
- [ ] Implementar fila de processamento

### FASE 12: Frontend Dashboard
- [ ] Pagina de upload de video
- [ ] Visualizador de video processado
- [ ] Display do nivel detectado
- [ ] Lista de erros e sugestoes
- [ ] Comparacao lado-a-lado (usuario vs ideal)
- [ ] Historico de analises

### FASE 13: Integracao & Deploy
- [ ] Conectar frontend com backend API
- [ ] Deploy do backend (Railway/Render)
- [ ] Configurar Supabase producao
- [ ] Testes end-to-end
- [ ] Monitoramento e logs

---

## Stack Tecnologico

| Area | Tecnologia | Uso |
|------|------------|-----|
| **Linguagem** | Python 3.11+ | Backend, ML |
| **CV Model** | YOLOv8-Pose | Deteccao de pose |
| **Wave Detection** | YOLOv8 custom | Detectar ondas |
| **3D Lifting** | VideoPose3D | Converter 2D->3D |
| **Sync** | FastDTW | Alinhamento temporal |
| **Backend** | FastAPI | API REST |
| **Frontend** | HTML/JS ou React | Dashboard |
| **Hosting** | Netlify | Frontend |
| **Database** | Supabase | PostgreSQL + Storage |
| **Processing** | OpenCV, NumPy | Video/Imagem |

---

## Metricas de Sucesso (MVP)

- [ ] Detectar pose em 95%+ dos frames
- [ ] Classificar nivel com 80%+ precisao
- [ ] Detectar fase correta em 85%+ dos casos
- [ ] Overlay Ghost sincronizado visivelmente correto
- [ ] Tempo de processamento < 2x duracao do video
- [ ] Feedback relevante e acionavel

---

## Referencias e Fontes

- [Swell Surf Camp - Niveis de Surfista](https://swellsurfcamp.com/what-level-of-surfer-am-i/)
- [Solid Surf House - L1 a L4](https://solidsurfhouse.com/surf/surfing-skill-levels-explained-from-l1-to-l4/)
- [ML Surfing - Pocket Detection](https://medium.com/@2oliver.ricken/machine-learning-surfing-15b2ad1158c4)
- [The Inertia - Erros no Bottom Turn](https://www.theinertia.com/surf/5-common-mistakes-surfers-make-with-their-bottom-turn/)
- [YOLOv8 Pose Documentation](https://docs.ultralytics.com/tasks/pose/)

---

*Ultima atualizacao: Dezembro 2024*
