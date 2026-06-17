# FC Career Tracker

Aplicação desktop para monitoramento e análise de carreiras no **EA FC 26**, utilizando captura de tela, OCR e banco de dados local.

O objetivo do projeto é permitir que jogadores do Modo Carreira acompanhem suas temporadas, partidas, estatísticas, histórico de clubes, seleções e títulos de forma mais prática, reduzindo a necessidade de registros manuais.

---

## Status do Projeto

🚧 **Em desenvolvimento ativo**

O projeto já possui uma base funcional com interface gráfica, banco SQLite, múltiplas carreiras, histórico de clubes e seleções, estatísticas avançadas, sistema de títulos e importação de partidas por OCR.

Atualmente, o foco está na melhoria da interface e na automação do fluxo de captura por teclas de atalho.

---

## Funcionalidades Atuais

### Sistema de Carreiras

* Criação de múltiplas carreiras
* Definição de carreira ativa
* Suporte inicial ao modo treinador
* Histórico de clubes da carreira
* Histórico de seleções comandadas
* Alteração de clube durante a carreira
* Alteração de seleção durante a carreira
* Partidas vinculadas à carreira ativa

### Sistema de Partidas

* Cadastro manual de partidas
* Importação automática de partidas por OCR
* Captura de pré-jogo com F7
* Captura de pós-jogo com F8
* Identificação automática de competição
* Identificação automática de data
* Identificação automática de times
* Identificação automática de placar
* Verificação de partidas duplicadas
* Listagem de partidas cadastradas

### Estatísticas e Análises

* Estatísticas gerais da carreira
* Estatísticas por adversário
* Estatísticas por time
* Estatísticas por competição
* Últimas partidas
* Forma recente
* Melhor vitória da carreira
* Pior derrota da carreira
* Sequência de vitórias
* Sequência invicta
* Gols marcados
* Gols sofridos
* Saldo de gols
* Aproveitamento

### Sistema de Títulos

* Cadastro manual de títulos conquistados
* Estatísticas de títulos por clube
* Estatísticas de títulos por seleção
* Títulos agrupados por competição
* Títulos vinculados à carreira ativa
* Títulos exibidos no histórico detalhado dos times

### Dashboard

* Resumo da carreira ativa
* Clube atual
* Seleção atual
* Total de jogos
* Vitórias, empates e derrotas
* Gols marcados e sofridos
* Aproveitamento
* Total de títulos
* Última partida registrada

---

## Tecnologias Utilizadas

### Linguagem

* Python 3

### Interface

* CustomTkinter

### Banco de Dados

* SQLite

### OCR e Captura

* Tesseract OCR
* PyTesseract
* PyAutoGUI
* Keyboard
* Pillow

### Processamento de Imagem

* OpenCV

---

## Roadmap

### Versão 0.1 ✅ Concluída

* [x] Configuração inicial do projeto
* [x] Banco de dados SQLite
* [x] Cadastro manual de partidas
* [x] Listagem de partidas
* [x] Estatísticas por adversário
* [x] Menu principal em terminal

### Versão 0.2 ✅ Concluída

* [x] Estatísticas gerais
* [x] Melhor vitória por adversário
* [x] Pior derrota por adversário
* [x] Histórico detalhado de confrontos
* [x] Último confronto
* [x] Estatísticas por competição
* [x] Sequência de vitórias
* [x] Sequência invicta
* [x] Ordenação cronológica dos confrontos

### Versão 0.3 ✅ Concluída

* [x] Interface gráfica com CustomTkinter
* [x] Cadastro de partidas pela interface
* [x] Estatísticas gerais pela interface
* [x] Consulta de adversários pela interface
* [x] Navegação entre telas
* [x] Sistema de múltiplas carreiras
* [x] Carreira ativa
* [x] Histórico de clubes
* [x] Histórico de seleções
* [x] Alteração de clube durante a carreira
* [x] Alteração de seleção durante a carreira
* [x] Partidas vinculadas à carreira ativa
* [x] Suporte inicial para modo treinador

### Versão 0.4 ✅ Concluída

* [x] OCR para leitura automática de partidas
* [x] Identificação automática de competição
* [x] Identificação automática de data
* [x] Identificação automática de times
* [x] Identificação automática de placar
* [x] Cadastro automático de partidas
* [x] Importação de partidas por imagem
* [x] Captura de pré-jogo com F7
* [x] Captura de pós-jogo com F8
* [x] Verificação de partidas duplicadas

### Versão 0.5 🚧 Em desenvolvimento

* [x] Estatísticas gerais da carreira
* [x] Estatísticas por time
* [x] Estatísticas por competição
* [x] Últimas partidas / forma recente
* [x] Melhor vitória e pior derrota da carreira
* [x] Sistema de títulos
* [x] Estatísticas de títulos
* [x] Dashboard da carreira
* [x] Histórico detalhado por time
* [x] Detalhamento por competição dentro do histórico
* [ ] Integração com calendário da carreira
* [ ] Integração com classificação das competições
* [ ] Estatísticas completas da temporada

### Versão 0.6

* [ ] Nova interface
* [ ] Menu lateral
* [ ] Agrupamento das estatísticas
* [ ] Autocomplete de times e seleções
* [ ] Escudos dos clubes e seleções
* [ ] Cards visuais no dashboard
* [ ] Melhor organização das telas

### Versão 1.0

* [ ] Dashboard gráfico
* [ ] Exportação de dados
* [ ] Instalador Windows
* [ ] Documentação completa
* [ ] Primeira versão pública

---

## Estrutura do Projeto

```text
Career-Analytics-FC/
├── data/
│   ├── career_tracker.db
│   └── config.json
│
├── screenshots/
│   ├── pre_jogo.png
│   └── pos_jogo.png
│
├── temp/
│   ├── pre_jogo.png
│   └── pos_jogo.png
│
├── src/
│   ├── main.py
│   ├── interface.py
│   ├── database.py
│   ├── carreira_ativa.py
│   ├── criar_carreira.py
│   ├── importar_partida.py
│   ├── captura_teclas.py
│   ├── listar_partidas.py
│   ├── estatisticas.py
│   ├── capture.py
│   ├── screen_capture.py
│   ├── ocr_image.py
│   ├── ocr_pre_jogo.py
│   ├── ocr_test.py
│   ├── extrair_placar.py
│   ├── extrair_pre_jogo.py
│   ├── extrair_dados.py
│   ├── teste_carreiras.py
│   └── verificar_banco.py
│
├── README.md
├── LICENSE
├── requirements.txt
└── Project_ideias.md
```

---

## Como Executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Criar/atualizar banco de dados

```bash
python src/database.py
```

### 3. Abrir a interface

```bash
python src/interface.py
```

### 4. Iniciar captura por teclas

```bash
python src/captura_teclas.py
```

Atalhos:

```text
F7  -> Capturar tela pré-jogo
F8  -> Capturar tela pós-jogo e tentar importar a partida
ESC -> Encerrar captura
```

---

## Observações sobre OCR

A importação automática depende da qualidade da tela capturada.

Para melhores resultados:

* Usar o jogo em modo janela sem borda
* Capturar o pré-jogo na tela de apresentação da partida
* Capturar o pós-jogo em tela com placar visível
* Conferir a prévia antes de salvar
* Evitar que janelas externas cubram informações importantes da tela

---

## Próximas Melhorias

* Nova interface com menu lateral
* Agrupamento das estatísticas em uma única área
* Autocomplete para clubes e seleções
* Escudos dos times
* Captura F7/F8 integrada diretamente na interface
* Melhorias visuais no dashboard
* Estatísticas completas por temporada
* Integração com calendário e classificação

---

## Aviso

Este projeto é independente e não possui vínculo com a EA Sports ou com a franquia EA FC.

EA FC é uma marca registrada da Electronic Arts.

---

## Autor

Desenvolvido por **Ronaldo Malta**.

GitHub: [@ronaldomalta](https://github.com/ronaldomalta)
