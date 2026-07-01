# Documento de Requisitos - CT Império App

Especificação completa dos requisitos funcionais e não funcionais do app de gestão da academia CT Império.

---

## 1. Introdução

### 1.1 Propósito

Documento de referência para desenvolvedores, testadores e stakeholders.

### 1.2 Escopo

Aplicativo mobile Android para academia de artes marciais:
- Gestão de aulas e presenças
- Controle de pagamentos e mensalidades
- Catálogo de produtos e pedidos
- Comunicação via avisos
- Perfil de usuários com múltiplas modalidades

### 1.3 Usuários-Alvo

- **Alunos**: Praticantes de artes marciais
- **Administradores**: Gestão operacional
- **Pais/Responsáveis**: Cadastro de filhos

### 1.4 Contexto

Academia em Marília-SP oferecendo: Muay Thai, Jiu-Jitsu, Boxe, MMA e No-Gi.

---

## 2. Requisitos Funcionais

### 2.1 Autenticação e Segurança

| ID | Requisito |
|----|------------|
| RF-001 | Registro com email/senha + Firestore |
| RF-002 | Login com persistência 24h |
| RF-003 | Controle de acesso admin |
| RF-004 | Logout (limpa cache) |

### 2.2 Perfil e Modalidades

| ID | Requisito |
|----|------------|
| RF-005 | Gerenciar perfil (nome, email, telefone, modalidades) |
| RF-006 | Sistema de graduações (Muay Thai, Jiu-Jitsu) |
| RF-007 | Cadastro de filhos |
| RF-008 | Seleção de professores |

### 2.3 Presença e Frequência

| ID | Requisito |
|----|------------|
| RF-009 | Marcar presença (aluno) |
| RF-010 | Calendário de frequência |
| RF-011 | Cálculo por semestre |
| RF-012 | Confirmação de presença (admin) |
| RF-013 | Restrições (1 presença/dia, bloqueio 1º janeiro) |

### 2.4 Aulas e Grade Horária

| ID | Requisito |
|----|------------|
| RF-014 | Visualização de grade de aulas |
| RF-015 | Próxima aula (cálculo automático) |

### 2.5 Avisos e Comunicados

| ID | Requisito |
|----|------------|
| RF-016 | Exibir avisos |
| RF-017 | Gerenciar avisos (admin) |

### 2.6 Pagamentos e PIX

| ID | Requisito |
|----|------------|
| RF-018 | Status de pagamento |
| RF-019 | QR Code PIX |
| RF-020 | Planos de mensalidades |

### 2.7 Produtos e Estoque

| ID | Requisito |
|----|------------|
| RF-021 | Catálogo de produtos |
| RF-022 | Carrinho de compras |
| RF-023 | Criação de pedidos |
| RF-024 | Acompanhamento de pedidos |
| RF-025 | Gerenciamento de estoque (admin) |

### 2.8 FAQ e Informações

| ID | Requisito |
|----|------------|
| RF-026 | Sistema FAQ |
| RF-027 | Contato WhatsApp |

### 2.9 Funcionalidades Administrativas

| ID | Requisito |
|----|------------|
| RF-028 | Dashboard admin |
| RF-029 | Gestão de alunos |
| RF-030 | Detalhes do aluno |
| RF-031 | Relatórios em PDF |
| RF-032 | Confirmação de presenças |
| RF-033 | Estatísticas e KPIs |

### 2.10 Onboarding

| ID | Requisito |
|----|------------|
| RF-034 | Fluxo de boas-vindas |

---

## 3. Requisitos Não Funcionais

| Categoria | Requisito |
|----------|----------|
| Performance | Cache 24h, lazy loading, offline-first |
| Segurança | SecureStore, Firebase Auth, regras Firestore |
| Disponibilidade | Detecção online/offline |
| Escalabilidade | Firestore + Storage |
| Usabilidade | Português, datas pt-BR |
| Compatibilidade | Android 5+, React Native 0.81.5 |
| Manutenibilidade | TypeScript, estrutura modular |

---

## 4. Stack Tecnológico

- **Frontend**: React Native 0.81.5
- **Backend**: Firebase (Auth, Firestore, Storage, Functions)
- **Navegação**: React Navigation (Stack + Drawer + Tabs)
- **Bibliotecas**: React Native Calendars, QR Code, Date-fns, AsyncStorage

---

## 5. Fluxos Principais

### Fluxo: Novo Aluno
1. Onboarding → Login → Registro → Perfil → Modalidades → Home

### Fluxo: Marcar Presença
1. Botão → Confirmação → Status "Pendente" → Admin confirma

### Fluxo: Realizar Pedido
1. Produtos → Carrinho → Finalizar → Status "Pendente" → Admin atualiza

### Fluxo: Pagamento PIX
1. Status "Pendente" → QR Code → Pagamento bancário → Confirma manual

---

## 6. Estrutura de Dados (Firestore)

```
Usuarios/
├── id
├── nome
├── email
├── telefone
├── observacoes
├── modalidades[] (modalidade, professor, graduacao)
├── Presenca[] (date, confirmada, modalidade)
├── filhos[] (mesma estrutura)
├── pagamento (boolean)
├── dataUltimoPagamento
├── isAdmin (boolean)
```

---

## 7. Modalidades

- Muay Thai (Adulto e Infantil)
- Jiu-Jitsu (Adulto e Infantil)
- Boxe
- MMA
- No-Gi

---

## 8. Graduações

### Muay Thai Adulto
Branco → Amarelo → Verde → Azul → Marrom → Vermelho → Preto (12 níveis)

### Jiu-Jitsu Adulto
Branca → Azul → Roxa → Marrom → Preta (5 cores × 5 graus = 25 níveis)