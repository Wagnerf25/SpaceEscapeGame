# 🚀 Space Escape - 3 Fases

**Space Escape** é um jogo de tiro vertical (shoot 'em up) estilo arcade desenvolvido em Python utilizando a biblioteca `pygame`. O jogo apresenta mecânicas progressivas, diferentes comportamentos de inimigos, power-ups e um sistema de ranking local.

## ✨ Funcionalidades

  * **3 Fases Distintas:** Cada fase possui música, fundo e velocidade de inimigos diferentes.
  * **Mecânicas Variadas:**
      * Meteoros simples.
      * Meteoros que aceleram.
      * Meteoros com movimento em zigue-zague.
      * **Meteoro Especial:** Causa morte instantânea (Game Over imediato).
      * **Invencibilidade:** Power-up que protege a nave temporariamente.
  * **Controles Híbridos:** Suporte tanto para Teclado quanto para Mouse.
  * **Sistema de Ranking:** Salva as 10 melhores pontuações localmente (`ranking.txt`).
  * **Animações:** Efeitos de motor da nave e transições de fase.
  * **Áudio:** Suporte para trilha sonora e efeitos sonoros (com tratamento de erro caso falte hardware de áudio).

## 🛠️ Pré-requisitos

Para rodar este jogo, você precisa ter instalado em sua máquina:

1.  **Python 3.x**
2.  **Biblioteca Pygame**

### Instalação das Dependências

Abra seu terminal ou prompt de comando e execute:

```bash
pip install pygame
```

## 📂 Estrutura de Arquivos

Para que o jogo funcione corretamente (carregando imagens e sons), você deve organizar seus arquivos da seguinte maneira. O código espera que exista uma pasta chamada `assets` no mesmo local do script Python.

```text
SpaceEscape/
├── game.py              # O código fonte do jogo
├── ranking.txt          # (Gerado automaticamente pelo jogo)
└── assets/              # Pasta obrigatória para imagens e sons
    ├── fundo_espacial.png
    ├── fundo_espacial2.png
    ├── fundo_espacial3.png
    ├── nave001.png
    ├── meteoro001.png
    ├── meteoro002.png
    ├── meteoro003.png
    ├── meteoroespecial.png
    ├── meteorovermelho.png
    ├── laserbeam.png
    ├── Game-over.png
    ├── insertcoin.png
    ├── classic-game-action-positive-5-224402.mp3
    ├── stab-f-01-brvhrtz-224599.mp3
    ├── distorted-future-363866.mp3
    ├── ThemeSpace2.mp3
    └── ThemeSpace3.mp3
```

> **Nota:** Se os arquivos de imagem ou som não forem encontrados na pasta `assets`, o jogo **não travará**. Ele criará retângulos coloridos como substitutos (placeholders) e rodará sem som.

## 🎮 Como Jogar

### Controles

| Ação | Teclado | Mouse |
| :--- | :--- | :--- |
| **Mover** | Setas `⬅️` e `➡️` | Mover o mouse lateralmente |
| **Atirar** | Barra de `Espaço` | (Automático ao segurar Espaço) |
| **Confirmar** | `Enter` ou `Espaço` | Clique Esquerdo |
| **Sair** | `Esc` | Botão "Sair" na tela |

### Regras

1.  **Vidas:** Você começa com 3 vidas. Colidir com meteoros normais retira 1 vida.
2.  **Pontuação:**
      * Desviar de meteoro: +1 ponto.
      * Destruir meteoro: +5 pontos.
3.  **Itens Especiais:**
      * 🔴 **Meteoro Vermelho:** Power-up de Invencibilidade (5 segundos).
      * 🔥 **Meteoro Laranja (Especial):** Cuidado\! Morte instantânea se tocar.
4.  **Fases:** Alcance a pontuação necessária para avançar para a próxima fase (Fase 1 → Fase 2 → Fase 3).

## 🚀 Executando o Jogo

Navegue até a pasta do projeto via terminal e execute:

```bash
python game.py
```

## 📝 Detalhes Técnicos

  * **Resolução:** 800x600 pixels.
  * **Taxa de Atualização:** 60 FPS.
  * **Persistência de Dados:** O ranking é salvo em um arquivo de texto plano (`ranking.txt`) codificado em UTF-8.
  * **Robustez:** O código inclui blocos `try/except` para garantir que o jogo inicie mesmo se o mixer de áudio falhar ou se imagens estiverem faltando.

## 🤝 Contribuição

Sinta-se à vontade para fazer um fork deste projeto, adicionar novos tipos de inimigos, melhorar os gráficos ou implementar um sistema de níveis infinitos\!

-----

**Divirta-se jogando Space Escape\!** 🌌
