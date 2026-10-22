# EcoDrop — Tetris da Reciclagem

Jogo educativo desenvolvido em Python e Pygame, com o objetivo de incentivar a conscientização ambiental por meio de uma experiência interativa de separação e classificação de resíduos.

**Desenvolvido por Arthur Santana Santos.**

> Status: Em desenvolvimento 🚧

## Sobre o projeto

O EcoDrop é um jogo educativo que combina entretenimento e conscientização ambiental. A proposta é desafiar o jogador a identificar e classificar diferentes resíduos, aprendendo mais sobre a separação correta dos materiais recicláveis.

O projeto está sendo desenvolvido como parte de um trabalho universitário, com foco na aplicação prática dos fundamentos de programação e no desenvolvimento de jogos digitais.

## Objetivos

* Incentivar a educação ambiental por meio de uma experiência interativa.
* Ensinar a classificação de diferentes tipos de resíduos.
* Desenvolver mecânicas de jogo progressivamente mais desafiadoras.
* Aplicar conceitos de programação, organização de código e controle de versão.
* Construir um projeto documentado e organizado para o portfólio de desenvolvimento.

## Categorias de resíduos

A proposta inicial contempla cinco categorias:

* Papel.
* Plástico.
* Vidro.
* Metal.
* Orgânicos.

As regras de classificação serão implementadas e refinadas durante o desenvolvimento do jogo.

## Funcionalidades planejadas

* Sistema de movimentação e classificação de resíduos.
* Pontuação por acertos.
* Combos por classificações consecutivas.
* Progressão de dificuldade.
* Sistema de vidas.
* Feedback visual e educativo.
* Interface gráfica interativa.
* Efeitos sonoros.

As funcionalidades serão adicionadas gradualmente e documentadas conforme forem implementadas e testadas.

## Tecnologias utilizadas

* **Python:** linguagem de programação.
* **Pygame:** biblioteca utilizada para desenvolver a interface gráfica e as mecânicas do jogo.
* **Git:** controle de versão do código.
* **GitHub:** hospedagem do repositório e acompanhamento do desenvolvimento.

## Como executar

### Pré-requisitos

* Python instalado.
* Git instalado, caso queira clonar o repositório pelo terminal.

### 1. Clone o repositório

```bash
git clone https://github.com/sonArthur/ecodrop.git
```

### 2. Acesse a pasta do projeto

```bash
cd ecodrop
```

### 3. Crie um ambiente virtual

```bash
python -m venv .venv
```

### 4. Ative o ambiente virtual

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instale as dependências

```bash
python -m pip install -r requirements.txt
```

### 6. Execute o jogo

```bash
python main.py
```

> Observação: os comandos de execução correspondem à estrutura inicial do projeto e poderão mudar conforme a arquitetura evoluir.

## Estrutura do projeto

```text
ecodrop/
├── assets/
│   ├── fonts/
│   ├── images/
│   └── sounds/
├── src/
│   ├── __init__.py
│   ├── game.py
│   ├── item.py
│   ├── bin.py
│   ├── score.py
│   └── ui.py
├── tests/
├── .gitignore
├── README.md
├── main.py
└── requirements.txt
```

A estrutura representa a organização planejada para o projeto. Os módulos serão criados conforme as etapas de desenvolvimento avançarem.

## Desenvolvimento

O projeto será desenvolvido de forma incremental, com implementação, testes e registro das alterações utilizando Git.

Novas funcionalidades serão incorporadas à medida que forem concluídas e verificadas.

## Autoria

**Arthur santana Santos**
Projeto acadêmico: EcoDrop — Tetris da Reciclagem.
