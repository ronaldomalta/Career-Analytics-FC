# FC Career Tracker

Aplicação desktop para monitoramento e análise de carreiras no **EA FC 26**, utilizando captura de tela, OCR e banco de dados local.

O objetivo do projeto é permitir que jogadores do Modo Carreira acompanhem suas temporadas, partidas, estatísticas, histórico de clubes, seleções e títulos de forma prática, reduzindo a necessidade de planilhas e registros manuais.

---

## Status do Projeto

🚀 **Versão 0.6 Beta**

O projeto já possui uma interface gráfica funcional com sistema de múltiplas carreiras, dashboard avançado, estatísticas detalhadas, histórico de clubes e seleções, títulos, OCR para importação de partidas, backup automático e exportação de dados.

Atualmente o foco está na automação do OCR, melhorias visuais e expansão das estatísticas da temporada.

---

## Funcionalidades Atuais

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

### Estatísticas e Análises

* Estatísticas gerais da carreira
* Estatísticas por time
* Estatísticas por adversário
* Estatísticas por competição
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

### Sistema de Títulos

* Cadastro manual de títulos
* Títulos vinculados à carreira ativa
* Estatísticas por clube
* Estatísticas por seleção
* Agrupamento por competição
* Contagem de conquistas
* Exibição da última temporada conquistada

### Calendário da Carreira

* Visualização das partidas da carreira
* Separação por data
* Base pronta para calendário visual

### Configurações

* Backup automático do banco de dados
* Exportação de partidas em CSV
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

---

## Roadmap

### Versão 0.1 ✅ Concluída

* Banco de dados SQLite
* Cadastro manual de partidas
* Estatísticas básicas
* Menu em terminal

### Versão 0.2 ✅ Concluída

* Estatísticas por adversário
* Melhor vitória
* Pior derrota
* Histórico de confrontos
* Sequências de resultados

### Versão 0.3 ✅ Concluída

* Interface gráfica
* Sistema de carreiras
* Carreira ativa
* Histórico de clubes
* Histórico de seleções
* Alteração de clubes e seleções

### Versão 0.4 ✅ Concluída

* OCR de partidas
* Captura automática
* Importação automática
* Verificação de duplicidade

### Versão 0.5 ✅ Concluída

* Dashboard inicial
* Sistema de títulos
* Estatísticas por competição
* Estatísticas por time
* Histórico detalhado
* Calendário da carreira

### Versão 0.6 🚧 Em Desenvolvimento

* [x] Nova interface
* [x] Menu lateral
* [x] Dashboard avançado
* [x] Sistema de configurações
* [x] Backup automático
* [x] Exportação CSV
* [x] Exclusão de carreiras
* [ ] OCR integrado diretamente na interface
* [ ] Estatísticas completas por temporada
* [ ] Autocomplete de clubes e seleções
* [ ] Escudos dos clubes
* [ ] Escudos das seleções

### Versão 1.0

* Dashboard gráfico
* Calendário visual completo
* Classificações das competições
* Estatísticas avançadas de temporada
* Instalador Windows
* Documentação completa
* Primeira versão pública

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

Atalhos:

```text
F7  -> Capturar tela pré-jogo
F8  -> Capturar tela pós-jogo
ESC -> Encerrar captura
```

---

## Observações sobre OCR

A importação automática depende da qualidade da captura.

Para melhores resultados:

* Utilizar o jogo em modo janela sem borda
* Capturar o pré-jogo na tela de apresentação da partida
* Capturar o pós-jogo em tela com placar visível
* Conferir a prévia antes de salvar
* Informar o ano da partida antes do salvamento

---

## Próximas Melhorias

* OCR totalmente integrado à interface
* Calendário visual semelhante ao EA FC
* Estatísticas completas por temporada
* Escudos de clubes e seleções
* Dashboard gráfico
* Classificação das competições
* Exportação avançada de dados

---

## Aviso

Este projeto é independente e não possui vínculo com a EA Sports ou com a franquia EA FC.

EA FC é uma marca registrada da Electronic Arts.

---

## Autor

Desenvolvido por **Ronaldo Malta**

GitHub: https://github.com/ronaldomalta
