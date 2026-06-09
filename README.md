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

### Versão 0.3 🚧 Em desenvolvimento

* [ ] Interface gráfica (CustomTkinter)
* [ ] Cadastro de partidas pela interface
* [ ] Estatísticas gerais pela interface
* [ ] Consulta de adversários pela interface
* [ ] Configuração dinâmica do time do usuário
* [ ] Navegação entre telas

### Versão 0.4

* [ ] OCR com Tesseract
* [ ] Leitura automática dos nomes dos clubes
* [ ] Leitura automática do placar
* [ ] Registro automático das partidas

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
