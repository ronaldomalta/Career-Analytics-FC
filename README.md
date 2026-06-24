# FC Career Tracker

Aplicação desktop desenvolvida em Python para monitoramento e análise de carreiras no **EA FC 26**, utilizando captura de tela, OCR e banco de dados local.

O objetivo do projeto é permitir que jogadores do Modo Carreira acompanhem suas temporadas, partidas, estatísticas, histórico de clubes, seleções e títulos de forma prática, eliminando a necessidade de planilhas e registros manuais.

---

## Status do Projeto

🚀 **Versão 0.6 Beta**

O projeto já possui interface gráfica completa, sistema de múltiplas carreiras, dashboard avançado, estatísticas detalhadas, calendário de partidas, histórico de clubes e seleções, sistema de títulos, OCR para importação de partidas, backup automático e exportação de dados.

---

## Screenshots

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Calendário

![Calendário](screenshots/calendario.png)

### OCR / Captura

![OCR](screenshots/ocr.png)

---

## Destaques

✅ Sistema de múltiplas carreiras

✅ OCR para importação automática de partidas

✅ Dashboard avançado

✅ Calendário da carreira

✅ Histórico de clubes e seleções

✅ Hall da Fama

✅ Estatísticas por competição

✅ Estatísticas por adversário

✅ Estatísticas por temporada

✅ Sistema de títulos

✅ Backup automático

✅ Exportação CSV

✅ Banco de dados local SQLite

---

## Funcionalidades

### Sistema de Carreiras

* Criação de múltiplas carreiras
* Definição de carreira ativa
* Exclusão segura de carreiras
* Suporte ao modo treinador
* Histórico de clubes
* Histórico de seleções
* Alteração de clube durante a carreira
* Alteração de seleção durante a carreira
* Partidas vinculadas à carreira ativa

### Sistema de Partidas

* Cadastro manual de partidas
* Importação automática por OCR
* Captura de pré-jogo
* Captura de pós-jogo
* Identificação automática de competição
* Identificação automática de data
* Identificação automática de times
* Identificação automática de placar
* Verificação de partidas duplicadas
* Listagem completa de partidas
* Associação automática à carreira ativa

### Estatísticas

* Estatísticas gerais da carreira
* Estatísticas por time
* Estatísticas por adversário
* Estatísticas por competição
* Estatísticas por temporada
* Histórico completo de confrontos
* Últimas partidas
* Forma recente
* Aproveitamento geral
* Média de gols marcados
* Média de gols sofridos
* Gols marcados
* Gols sofridos
* Saldo de gols
* Melhor vitória da carreira
* Pior derrota da carreira
* Sequência de vitórias
* Sequência invicta
* Jogos sem vencer

### Dashboard Avançado

* Resumo da carreira ativa
* Clube atual
* Seleção atual
* Total de jogos
* Vitórias, empates e derrotas
* Gols marcados e sofridos
* Médias ofensivas e defensivas
* Aproveitamento geral
* Total de títulos
* Último título conquistado
* Forma recente com indicadores visuais
* Maior vitória
* Pior derrota
* Sequência de vitórias
* Jogos sem vencer
* Últimas partidas registradas
* Melhor competição da carreira
* Pior competição da carreira

### Sistema de Títulos

* Cadastro manual de títulos
* Títulos vinculados à carreira ativa
* Estatísticas por clube
* Estatísticas por seleção
* Agrupamento por competição
* Contagem de conquistas
* Exibição da última temporada conquistada

### Hall da Fama

* Ranking dos adversários com melhor aproveitamento
* Ranking dos adversários com pior aproveitamento
* Histórico de confrontos
* Aproveitamento por adversário

### Calendário da Carreira

* Visualização mensal das partidas
* Resultados coloridos
* Identificação de partidas em casa e fora
* Histórico por mês e temporada

### Configurações

* Backup automático do banco de dados
* Exportação CSV
* Limpeza de arquivos temporários
* Informações do sistema

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

### Controle de Versão

* Git
* GitHub

---

## Estrutura do Projeto

```text
Career-Analytics-FC/
├── backups/
├── exports/
├── data/
│   ├── career_tracker.db
│   └── config.json
│
├── screenshots/
│
├── temp/
│
├── src/
│   ├── interface_v2.py
│   ├── database.py
│   ├── carreira_ativa.py
│   ├── captura_teclas.py
│   ├── importar_partida.py
│   ├── estatisticas.py
│   ├── capture.py
│   ├── extrair_dados.py
│   ├── ocr_pre_jogo.py
│   └── ...
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

## Como Executar

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Criar ou Atualizar o Banco

```bash
python src/database.py
```

### Abrir a Interface

```bash
python src/interface_v2.py
```

### Captura por Atalhos

```bash
python src/captura_teclas.py
```

Atalhos disponíveis:

```text
F7  → Capturar tela pré-jogo
F8  → Capturar tela pós-jogo
ESC → Encerrar captura
```

---

## OCR de Partidas

O sistema utiliza OCR para automatizar a importação das partidas.

Fluxo recomendado:

1. Capturar a tela de pré-jogo
2. Capturar a tela de pós-jogo
3. Gerar prévia
4. Conferir os dados detectados
5. Corrigir manualmente se necessário
6. Confirmar o salvamento

### Recomendações

* Utilizar o jogo em modo janela sem borda
* Capturar o pré-jogo na apresentação da partida
* Capturar o pós-jogo com o placar visível
* Conferir a prévia antes de salvar
* Informar o ano da partida antes da confirmação

---

## Aprendizados

Durante o desenvolvimento do FC Career Tracker foram aplicados conceitos de:

* Programação Orientada a Objetos
* Banco de Dados SQLite
* Estruturas de Dados
* Processamento de Imagens
* OCR com Tesseract
* Desenvolvimento Desktop com Python
* Controle de Versão com Git e GitHub
* Arquitetura em Camadas
* Manipulação de Arquivos
* Interface Gráfica com CustomTkinter

---

## Roadmap

### Versão 0.1 ✅

* Banco de dados SQLite
* Cadastro manual de partidas
* Estatísticas básicas
* Menu em terminal

### Versão 0.2 ✅

* Estatísticas por adversário
* Melhor vitória
* Pior derrota
* Histórico de confrontos
* Sequências de resultados

### Versão 0.3 ✅

* Interface gráfica
* Sistema de carreiras
* Histórico de clubes
* Histórico de seleções

### Versão 0.4 ✅

* OCR de partidas
* Captura automática
* Importação automática
* Verificação de duplicidade

### Versão 0.5 ✅

* Dashboard inicial
* Sistema de títulos
* Estatísticas por competição
* Histórico detalhado
* Calendário

### Versão 0.6 ✅

* Dashboard avançado
* Hall da Fama
* Calendário visual
* Configurações
* Backup automático
* Exportação CSV
* Exclusão de carreiras
* OCR com prévia editável

### Versão 1.0

* Dashboard gráfico
* Calendário completo estilo EA FC
* Estatísticas avançadas por temporada
* Classificações das competições
* Escudos de clubes e seleções
* Instalador Windows
* Primeira versão pública

---

## Aviso

Este projeto é independente e não possui qualquer vínculo com a EA Sports ou com a franquia EA FC.

EA FC é uma marca registrada da Electronic Arts.

---

## Autor

**Ronaldo Malta**

🎓 Ciência da Computação - UNICAP

💻 Python • SQLite • OCR • CustomTkinter

🔗 GitHub: https://github.com/ronaldomalta
