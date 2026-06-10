# FC Career Tracker

Aplicação para monitoramento e análise de carreiras no EA FC 26 através de captura de tela, visão computacional e OCR.

O objetivo do projeto é permitir que jogadores do Modo Carreira acompanhem automaticamente suas temporadas, estatísticas e histórico de partidas sem precisar registrar informações manualmente.

---

## Status do Projeto

🚧 Em desenvolvimento

Atualmente o projeto possui um sistema funcional de armazenamento e análise de partidas utilizando SQLite. As próximas etapas incluem captura de tela, OCR e automação da coleta de dados diretamente do EA FC 26.

---

## Funcionalidades Atuais

### Sistema de Partidas

* Cadastro manual de partidas
* Armazenamento em SQLite
* Listagem de partidas cadastradas
* Estatísticas por adversário
* Menu principal em terminal

### Estatísticas Disponíveis

* Jogos disputados contra um adversário
* Vitórias
* Empates
* Derrotas
* Gols marcados
* Gols sofridos

---

## Funcionalidades Planejadas

### Modo Carreira de Técnico

* Registro automático de partidas
* Identificação de clubes
* Leitura automática de placares
* Controle de vitórias, empates e derrotas
* Histórico completo da temporada
* Estatísticas de gols marcados e sofridos
* Registro de títulos conquistados
* Dashboard de desempenho

### Modo Carreira de Jogador

* Estatísticas de gols
* Estatísticas de assistências
* Nota média das partidas
* Evolução de Overall
* Histórico de transferências
* Conquistas e títulos

### Estatísticas Avançadas

* Aproveitamento geral
* Melhor vitória
* Pior derrota
* Sequência de vitórias
* Ranking de adversários
* Desempenho por competição
* Desempenho por temporada
* Comparação entre temporadas
* Exportação de dados

---

## Tecnologias

### Backend

* Python 3

### Banco de Dados

* SQLite

### Processamento de Imagem

* OpenCV
* Tesseract OCR

### Interface

* Em definição

---

## Roadmap

### Versão 0.1 ✅ Concluída

* [x] Configuração do projeto
* [x] Banco de dados SQLite
* [x] Cadastro manual de partidas
* [x] Listagem de partidas
* [x] Estatísticas por adversário
* [x] Menu principal em terminal

### Versão 0.2 ✅ Concluída

* [x] Estatísticas gerais
* [x] Melhor vitória
* [x] Pior derrota
* [x] Histórico detalhado de confrontos
* [x] Último confronto
* [x] Estatísticas por competição
* [x] Sequência de vitórias
* [x] Sequência invicta
* [x] Ordenação cronológica dos confrontos

### Versão 0.3 ✅ Concluída

* [x] Interface gráfica (CustomTkinter)
* [x] Cadastro de partidas pela interface
* [x] Estatísticas gerais pela interface
* [x] Consulta de adversários pela interface
* [x] Configuração dinâmica do time do usuário
* [x] Navegação entre telas
* [x] Sistema de múltiplas carreiras
* [x] Carreira ativa
* [x] Histórico de clubes
* [x] Histórico de seleções
* [x] Alteração de clube durante a carreira
* [x] Alteração de seleção durante a carreira
* [x] Partidas vinculadas à carreira ativa
* [x] Suporte para modo treinador

### Versão 0.4 🚧 Em desenvolvimento

* [ ] Captura de tela em tempo real
* [ ] OCR para leitura automática de partidas
* [ ] Identificação automática de competição
* [ ] Identificação automática de data
* [ ] Identificação automática de times
* [ ] Cadastro automático de partidas
* [ ] Importação de partidas por imagem

### Versão 0.5

* [ ] Integração com calendário da carreira
* [ ] Integração com classificação das competições
* [ ] Estatísticas completas da temporada

### Versão 1.0

* [ ] Dashboard gráfico
* [ ] Exportação de dados
* [ ] Instalador Windows
* [ ] Documentação completa
* [ ] Primeira versão pública

---

## Progresso Atual

- Banco SQLite funcional
- Cadastro de partidas
- Listagem de partidas
- Estatísticas gerais
- Confrontos diretos
- Histórico de partidas
- Estatísticas por competição

## Estrutura do Projeto

```text
fc-career-tracker/
├── data/
│   └── career_tracker.db
├── src/
│   ├── main.py
│   ├── database.py
│   └── capture.py
├── tests/
├── docs/
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

---

## Aviso

Este projeto é independente e não possui qualquer vínculo com a EA Sports ou com a franquia EA FC.

EA FC é uma marca registrada da Electronic Arts.

---

## Autor

Desenvolvido por Ronaldo Malta.

GitHub: @ronaldomalta
