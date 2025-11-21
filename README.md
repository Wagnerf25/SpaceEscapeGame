🚀 Space Escape

Um jogo de arcade "Shoot 'em Up" vertical desenvolvido em Python com Pygame.

Space Escape é um jogo de sobrevivência espacial onde o jogador deve pilotar uma nave, desviar de chuvas de meteoros, utilizar power-ups e acumular a maior pontuação possível através de 3 fases de dificuldade progressiva.

📋 Índice

Sobre o Projeto

Funcionalidades

Pré-requisitos e Instalação

Como Jogar

Mecânicas e Fases

Estrutura de Arquivos

Autor

📖 Sobre o Projeto

Este projeto foi desenvolvido como parte de um trabalho acadêmico de implementação de jogos utilizando a biblioteca Pygame. O foco do desenvolvimento foi criar uma arquitetura de código limpa, com tratamento de erros robusto (I/O e Áudio) e mecânicas de jogo progressivas.

O jogo conta com sistema de ranking persistente, animações procedurais (partículas do motor) e suporte a controles híbridos (Teclado e Mouse).

✨ Funcionalidades

Dificuldade Progressiva: 3 Fases com aumento de velocidade e novos comportamentos inimigos.

Sistema de Ranking: As 10 melhores pontuações são salvas localmente em ranking.txt.

Power-ups:

🛡️ Invencibilidade: Imunidade temporária contra meteoros comuns.

Inimigos Especiais:

☠️ Meteoro Caveira: Causa morte instantânea ("Insta-kill").

Efeitos Visuais: Animação do propulsor da nave gerada via código (sem uso de sprites estáticos para o fogo).

Controles Híbridos: Jogue usando o teclado ou o mouse.

🛠 Pré-requisitos e Instalação

Para executar o jogo, você precisa ter o Python 3 instalado.

1. Clonar o Repositório

git clone [https://github.com/Wagnerf25/SpaceEscapeGame.git](https://github.com/Wagnerf25/SpaceEscapeGame.git)
cd SpaceEscapeGame


2. Instalar Dependências

O jogo utiliza apenas a biblioteca pygame.

pip install pygame


3. Configurar Assets

Certifique-se de que a pasta assets esteja no mesmo diretório do script main.py e contenha todos os recursos (imagens e sons) necessários.

4. Executar o Jogo

python main.py


🎮 Como Jogar

O objetivo é sobreviver e destruir meteoros. Você tem 3 vidas.

Controles

Ação

Teclado

Mouse

Mover Nave

Setas ⬅️ e ➡️

Mover cursor horizontalmente

Mover Rápido

-

Segurar Botão Esquerdo

Atirar

ESPAÇO

-

Confirmar

ENTER

Clique nos botões

Pausar/Sair

ESC

Botão na tela

Pontuação

+1 Ponto: Sobreviver a um meteoro (quando ele sai da tela).

+5 Pontos: Destruir um meteoro com laser.

⚙️ Mecânicas e Fases

O jogo evolui automaticamente conforme sua pontuação:

🌑 Fase 1: Início

Meta: Chegar a 30 pontos.

Inimigos: 5 meteoros simultâneos.

Comportamento: Queda vertical simples.

Velocidade: Lenta.

🌘 Fase 2: Aceleração

Meta: Chegar a 150 pontos.

Inimigos: 7 meteoros simultâneos.

Novo Comportamento: Meteoros aceleram enquanto caem.

Velocidade: Média.

🌕 Fase 3: Caos (Loop Infinito)

Meta: Sobreviver o máximo possível.

Inimigos: 10 meteoros simultâneos.

Novo Comportamento: Movimento em Zig-Zag (senoidal) e aceleração.

Velocidade: Rápida.

📂 Estrutura de Arquivos

SpaceEscapeGame/
│
├── main.py              # Código fonte principal
├── ranking.txt          # Arquivo de persistência de pontuação (gerado automaticamente)
├── README.md            # Documentação do projeto
└── assets/              # Pasta obrigatória com imagens e sons
    ├── fundo_espacial.png
    ├── nave001.png
    ├── meteoro001.png
    ├── ...


👨‍💻 Autor

<table align="center">
<tr>
<td align="center">
<a href="https://www.google.com/search?q=https://github.com/Wagnerf25">
<img src="https://www.google.com/search?q=https://github.com/Wagnerf25.png" width="100px;" alt="Foto de Wagner Reis"/>




<sub><b>Wagner Reis Figueiredo</b></sub>
</a>
</td>
</tr>
</table>

Desenvolvido como referência para implementação de jogos em Python.

Este projeto é de código aberto. Sinta-se à vontade para contribuir ou usar como base para estudos.
