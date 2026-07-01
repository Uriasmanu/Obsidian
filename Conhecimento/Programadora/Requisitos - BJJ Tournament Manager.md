# Documento de Requisitos - BJJ Tournament Manager

Projeto pessoal para estudo de IA + spec.Sistema web Next.js para gerenciamento de torneios de Brazilian Jiu-Jitsu.

---

## Visao Geral

Gerenciamento completo de torneios BJJ: cadastro de competidores, arbitros, areas de luta, chaves e placar eletronico em tempo real.

---

## Stack Tecnologico

| Camada | Tecnologia |
|--------|-----------|
| Framework | Next.js 16 |
| Linguagem | TypeScript 5 |
| UI | shadcn/ui, Radix UI |
| Armazenamento | Arquivos JSON locais |
| Validacao | Zod, React Hook Form |

---

## Modulos

### Modulo 1: Competidores

| ID | Requisito |
|----|----------|
| RF-1.1 | Cadastrar competidor (nome, equipe, peso, faixa, nascimento, tecnico) |
| RF-1.2 | Editar competidor |
| RF-1.3 | Desativar/reativar competidor |
| RF-1.4 | Filtrar por faixa, equipe, nome |
| RF-1.5 | Importar CSV |
| RF-1.6 | Exportar CSV |
| RF-1.7 | Validar duplicatas (nome + equipe) |

### Modulo 2: Arbitros

| ID | Requisito |
|----|----------|
| RF-2.1 | Cadastrar arbitro (nome, cidade, faixa) |
| RF-2.2 | Editar arbitro |
| RF-2.3 | Atribuir a area de luta |
| RF-2.4 | Import/Export CSV |

### Modulo 3: Areas de Luta

| ID | Requisito |
|----|----------|
| RF-3.1 | Criar area com nome e arbitros |
| RF-3.2 | Atribuir luta atual |
| RF-3.3 | Visualizar status (livre/ocupada) |

### Modulo 4: Chaves (Brackets)

| ID | Requisito |
|----|----------|
| RF-4.1 | Criar chave por faixa e peso |
| RF-4.2 | Selecionar competidores |
| RF-4.3 | Gerar lutas automaticas (eliminacao simples) |
| RF-4.4 | Visualizar progresso |

### Modulo 5: Placar

| ID | Requisito |
|----|----------|
| RF-5.1 | Selecionar area ativa |
| RF-5.2 | Exibir lutadores |
| RF-5.3 | Adicionar pontos (2, 3, 4) |
| RF-5.4 | Registrar vantagens |
| RF-5.5 | Aplicar penalidades |
| RF-5.6 | Marcar finalizacao (submissao) |
| RF-5.7 | Desfazer ultima acao |
| RF-5.8 | Finalizar luta |

### Modulo 6: Tempo

| ID | Requisito |
|----|----------|
| RF-6.1 | Iniciar/parar cronometro |
| RF-6.2 | Resetar |
| RF-6.3 | Configurar tempo limite |
| RF-6.4 | Alerta visual |
| RF-6.5 | Suporte golden score |

### Modulo 7: Relatorios

| ID | Requisito |
|----|----------|
| RF-7.1 | Gerar relatorio final |
| RF-7.2 | Listar vencedores por chave |
| RF-7.3 | Exportar formato imprimivel |

---

## Estrutura de Dados

```
Competidor { id, name, team, weight, belt, dateBirth, coach, isActive }

Arbitro { id, name, city, beltReferee, isActive }

Area { id, name, refereeId, assistantRefereeId, currentMatchId, status }

Chave { id, title, belt, status, matches[], winners }

Luta { id, fighter1, fighter2, score1, score2, winnerId, round, finished }
```

---

## Regras de Pontuacao BJJ

- Pontos: 2, 3, 4
- Vantagens: ate 99
- Penalidades: ate 99
- Submissao finaliza luta
- Vencedor por pontos ou submissao

---

## Faixas Disponiveis

Adulto: WHITE, BLUE, PURPLE, BROWN, BLACK

Infantil: GRAY, YELLOW, ORANGE, GREEN

---

## Histórias de Usuário

> **Nota:** A única razão prática válida para usar histórias de usuário é ter **critérios de aceitação claros** - definindo quando a funcionalidade está "pronta".

### Template

```
Como [usuário], quero [funcionalidade], para [benefício].

Critérios de Aceitação:
- [ ] ...
- [ ] ...
```

### Exemplo Aplicado

**RF-1.1 - Cadastrar competidor**

```
Como organizador de torneo, quero cadastrar competidores com nome, equipe,
peso, faixa e nascimento, para ter uma base de dados organizada.

Critérios de Aceitação:
- [ ] Todos os campos obrigatórios validam entrada
- [ ] Não permite duplicata (nome + equipe)
- [ ] Após salvar, exibe mensagem de sucesso
- [ ] Permite editar depois
```

---

## Objetivo de Estudo

Este projeto foi criado para estudar:
- Desenvolvimento guiado por especificacao (SDD)
- Integracao com ferramentas de IA
- Estrutura de requisitos bem definidos
- Implementacao baseada em spec