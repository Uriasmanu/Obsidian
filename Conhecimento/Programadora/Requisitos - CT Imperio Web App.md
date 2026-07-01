# Documento de Requisitos - CT Império Web App

PWA mobile-first para iPhone (versão web do app de gestão da academia).

---

## Visao Geral

**Objetivo:** Permitir que usuarios do iPhone marquem presenca e gerenciem seus dados.

**Plataforma:** Progressive Web App (PWA) - Mobile-first

---

## Stack Tecnologico

| Camada | Tecnologia |
|--------|-----------|
| Framework | Next.js 16.2.3 |
| Linguagem | TypeScript 5 |
| React | 19.2.4 |
| Estilizacao | Tailwind CSS 4 |
| UI Components | Base UI, shadcn/ui |
| Backend | Firebase (Auth + Firestore) |
| Hospedagem | Vercel |

---

## Modulos Funcionais

### Modulo 1: Autenticacao

| ID | Requisito |
|----|----------|
| RF-001 | Login (email/senha, Firebase) |
| RF-002 | Cadastro (registro + Firestore) |
| RF-003 | Sessao persistente (24h cache) |

### Modulo 2: Perfil e Dados

| ID | Requisito |
|----|----------|
| RF-004 | Visualizar/editar perfil |
| RF-005 | Gerenciar modalidades (5 modalidades) |
| RF-006 | Gerenciar filhos dependentes |

### Modulo 3: Presenca

| ID | Requisito |
|----|----------|
| RF-007 | Marcar presenca (1x/dia) |
| RF-008 | Dashboard de frequencia |
| RF-009 | Modal de calendario |
| RF-010 | Calculo de frequencia por semestre |

### Modulo 4: Pagamento

| ID | Requisito |
|----|----------|
| RF-011 | Visualizar status de pagamento |

### Modulo 5: PWA

| ID | Requisito |
|----|----------|
| RF-012 | Service Worker + manifest |

### Modulo 6: Admin

| ID | Requisito |
|----|----------|
| RF-013 | Confirmar presencas (painel professor) |

---

## Requisitos Nao Funcionais

| Categoria | Requisito |
|-----------|-----------|
| Performance | Carregamento < 3s em 4G |
| Seguranca | HTTPS, tokens JWT, Regras Firestore |
| Compatibilidade | iOS 14+, navegadores modernos |
| Usabilidade | Interface intuitiva, feedback visual |
| Manutenibilidade | TypeScript 100%, testes > 80% |

---

## Fluxos Principais

### Fluxo: Novo Usuario
1. Acessa app → Login → Registrar → Preenche dados → Login → Perfil

### Fluxo: Marcar Presenca
1. Perfil → Botao "Marcar Presenca" → Pendente → Professor confirma → Confirmado

### Fluxo: Adicionar Filho
1. Perfil → Filhos → Adicionar → Preenche dados → Salvar

---

## Estrutura de Dados

```
Usuario {
  id, nome, email, telefone, observacao
  admin, pagamento, avisoPagamento
  dataPagamento, dataUltimoPagamento
  modalidades[], filhos[]
}

Filho {
  id, nome, idade, observacao
  pagamento, modalidades[], presenca[]
}

ModalidadeAluno {
  modalidade, graduacao, dataInicio, ativo, professor
}

PresencaRecord {
  date, modalidade, confirmada, recusada
}
```

---

## Modalidades Disponiveis

- Jiu-Jitsu
- Muay Thai
- Boxe
- MMA
- No-Gi

---

## Graduacoes

**Muay Thai:** Branco → Preto (12 niveis)

**Jiu-Jitsu:** Branca → Preta (5 cores × 5 graus = 25 niveis)

---

## Roadmap

| Fase | Funcionalidades |
|------|---------------|
| MVP | Login, Perfil, Presenca, Modalidades, Filhos |
| v1.1 | Notificacoes push, Relatorios PDF |
| v1.2 | Autenticacao social, Modo offline |
| v2.0 | App nativo iOS/Android |

---

## Referencia

Tech Stack: Next.js 16.2.3, TypeScript 5, React 19.2.4, Tailwind CSS 4, Firebase