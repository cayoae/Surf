# Prompt Master - Coleta de Videos para Treinamento

Copie e cole este prompt em ferramentas de AI (Perplexity, ChatGPT, Gemini).
Adapte a secao [MANOBRA ESPECIFICA] conforme necessario.

---

## PROMPT COMPLETO

```
Estou desenvolvendo um sistema de analise de surf usando inteligencia artificial. O sistema usa YOLOv8-Pose para detectar a pose do surfista (esqueleto com 17 pontos do corpo) e compara com um modelo "ideal" para dar feedback visual e tecnico.

OBJETIVO DO PROJETO:
- Classificar automaticamente o nivel do surfista (iniciante ou intermediario)
- Detectar erros de tecnica comparando com execucao profissional
- Sobrepor um "esqueleto fantasma" do movimento ideal no video do usuario
- Gerar feedback especifico como "flexione mais os joelhos" ou "olhe para frente"

O QUE PRECISO AGORA:
Preciso coletar videos do YouTube para criar meu dataset de treinamento. Esses videos serao processados frame-a-frame para extrair as poses dos surfistas e criar uma biblioteca de "movimentos ideais".

[MANOBRA ESPECIFICA]
Neste momento, estou focando em videos de POP-UP / TAKE-OFF (o movimento de levantar na prancha ao pegar a onda).

CRITERIOS TECNICOS DOS VIDEOS:

1. QUALIDADE DE IMAGEM
   - Minimo 720p (ideal 1080p ou 4K)
   - Imagem nitida onde se veja claramente o corpo do surfista
   - Sem muita espuma ou spray bloqueando a visao
   - Boa iluminacao (evitar contra-luz forte)

2. ANGULO DA CAMERA
   - Preferencia: angulo LATERAL (camera na praia ou na agua, filmando de lado)
   - Tambem util: angulo traseiro (de tras do surfista)
   - Evitar: angulo muito frontal onde nao se ve bem a postura

3. ENQUADRAMENTO
   - Surfista deve ocupar boa parte do frame
   - Corpo inteiro visivel (da cabeca aos pes)
   - Evitar videos muito distantes onde o surfista e pequeno

4. VELOCIDADE
   - MUITO IMPORTANTE: videos em CAMERA LENTA (slow motion)
   - Ideal: 60fps ou superior
   - Videos que mostrem o movimento frame-by-frame

5. CONTEUDO
   - Surfistas executando a tecnica CORRETAMENTE
   - Profissionais ou instrutores qualificados
   - Demonstracoes didaticas com boa execucao
   - Se possivel, multiplas repeticoes da mesma manobra

FONTES CONFIAVEIS:
- Canais de escolas de surf: Barefoot Surf Travel, OMBE Surf, Surf Simply, Kale Brock
- Canais de analise tecnica: How to Rip, Surf Mastery
- Producoes profissionais: WSL, Red Bull Surfing, Stab Magazine
- Surfistas profissionais com canais proprios

O QUE EVITAR:
- Videos muito antigos com baixa qualidade
- Compilacoes rapidas sem foco tecnico
- Videos onde o surfista esta muito longe/pequeno
- Filmagens tremidas ou instáveis
- Videos com muitos cortes rapidos (preciso de takes continuos)

FORMATO DA RESPOSTA:
Para cada video encontrado, me de:

1. URL do YouTube
2. Titulo do video
3. Canal/Autor
4. Timestamp especifico (se a parte relevante nao for no inicio)
5. Por que este video e bom para o meu proposito
6. Qualidade estimada (720p, 1080p, 4K)
7. Angulo da camera (lateral, frontal, drone, etc)

Organize os resultados do MELHOR para o menos ideal, priorizando:
- Camera lenta
- Alta resolucao
- Angulo lateral
- Execucao tecnica perfeita

Encontre pelo menos 10 videos que atendam a esses criterios.
```

---

## VARIACOES DO PROMPT

### Para BOTTOM TURN:
Substitua a secao [MANOBRA ESPECIFICA] por:

```
[MANOBRA ESPECIFICA]
Neste momento, estou focando em videos de BOTTOM TURN (a curva que o surfista faz na base da onda para ganhar velocidade e direcao).

Pontos importantes para esta manobra:
- Momento da compressao (joelhos flexionados)
- Rotacao do tronco e ombros
- Posicao dos bracos para equilibrio
- Direcao do olhar (para onde o surfista esta olhando)
- Angulacao da prancha (rail na agua)

Preciso de videos tanto de FRONTSIDE (de frente para a onda) quanto BACKSIDE (de costas para a onda).
```

### Para REMADA:
Substitua a secao [MANOBRA ESPECIFICA] por:

```
[MANOBRA ESPECIFICA]
Neste momento, estou focando em videos de REMADA e POSICIONAMENTO NA PRANCHA.

Pontos importantes:
- Posicao correta deitado na prancha (nem muito atras, nem muito na frente)
- Tecnica de bracada eficiente
- Posicao da cabeca e do olhar durante a remada
- Momento de transicao da remada para o pop-up
- Como remar para entrar na onda

Videos com visao lateral ou levemente elevada (drone baixo) sao ideais.
```

### Para ERROS COMUNS (dataset de comparacao):
Substitua a secao [MANOBRA ESPECIFICA] por:

```
[MANOBRA ESPECIFICA]
Neste momento, preciso de videos que mostrem ERROS COMUNS de surfistas iniciantes, para criar um dataset de comparacao.

Erros que preciso identificar:
- Pop-up muito lento ou em duas etapas (joelho primeiro)
- Olhar para baixo (para a prancha) em vez de para frente
- Corpo muito rigido/reto, sem flexao de joelhos
- Bracos descontrolados ou grudados no corpo
- Stance errado (pes muito juntos ou muito separados)
- Perda de equilibrio por posicionamento incorreto

Ideal: videos educativos que mostrem "o que NAO fazer" ou comparacoes "errado vs certo".
Tambem util: compilacoes de fails onde o erro tecnico e claramente visivel.
```

### Para VIDEOS DE PROFISSIONAIS:
Substitua a secao [MANOBRA ESPECIFICA] por:

```
[MANOBRA ESPECIFICA]
Neste momento, preciso de videos de SURFISTAS PROFISSIONAIS executando manobras basicas com tecnica perfeita.

Surfistas de interesse:
- John John Florence (conhecido pela tecnica fluida)
- Gabriel Medina (explosao e precisao)
- Italo Ferreira (estilo agressivo)
- Filipe Toledo (aereos e progressao)
- Carissa Moore (tecnica feminina de referencia)
- Kelly Slater (tecnica classica perfeita)

Manobras de interesse:
- Take-off / Drop
- Bottom turn (frontside e backside)
- Cutback
- Top turn / re-entry

Preferencia por highlights da WSL ou free surfs em alta qualidade com slow motion.
```

---

## DICA EXTRA

Apos receber os resultados, voce pode fazer um follow-up:

```
Otimo! Agora, para os 3 melhores videos que voce listou, me de:

1. Os timestamps exatos dos melhores momentos para extrair poses
2. Descricao do que acontece em cada momento (ex: "0:45 - pop-up lateral perfeito em slow motion")
3. Se ha alguma repeticao da mesma manobra no video e em quais timestamps

Isso vai me ajudar a ir direto aos frames mais uteis para o treinamento.
```

---

*Criado para o projeto Surf Analyzer - Dezembro 2024*
