# Modulo de Relatorios - App Academia

Modulo de relatorios para o app de gestao de academia de luta (React Native).

---

## Visao Geral

Novo modulo de relatorios que substituira o componente `ListaAlunosRelatorio` atual.

**Problema atual:**
- Periodo fixo (apenas 10 a 9 do mes seguinte)
- Sem flexibilidade de datas
- Funcionalidade subutilizada

**Solucao:**
- Resumo mensal automatico ao abrir
- Relatorio de graduacao semestral

---

## Estrutura de Arquivos

```
components/Admin/relatorios/
├── RelatoriosScreen.tsx              # Container principal (SUBSTITUI ListaAlunosRelatorio)
├── GraficoModalidades.tsx            # Grafico de barras por modalidade
├── ListaAlunosSemPresenca.tsx        # Lista de alunos sem presenca no mes
├── RelatorioAptosGraduacao.tsx       # Relatorio semestral de graduacao
├── hooks/
│   ├── useAlunosPorModalidade.ts   # Logica do grafico
│   ├── useAlunosSemPresenca.ts     # Logica da lista de ausentes
│   └── useRelatorioGraduacao.ts   # Logica do relatorio de graduacao
├── utils/
│   ├── presencaUtils.ts           # contarPresencas, filtrarPresencasPorPeriodo
│   └── pdfUtils.ts               # gerarHTMLRelatorio, exportarPDF
└── styles/
    └── relatorioStyles.ts         # Estilos compartilhados
```

---

## 2 Telas/Componentes

### Tela 1: Resumo Mensal (automatico ao abrir)

1. **GraficoModalidades** - Barras por modalidade (mes atual vs mes anterior)
2. **ListaAlunosSemPresenca** - Alunos sem presenca este mes
3. **Botao** - Acesso ao relatorio de graduacao

### Tela 2: Relatorio de Graduacao (sob demanda)

- Selecao de periodo livre (De / Ate)
- Campo presenca minima (padrao: 12)
- Lista separada em grupos:
  - Aptos (presenca >= minima + pagamento em dia)
  - Em Progresso (< minima + pagamento em dia)
  - Inelegiveis (pagamento atrasado)
- Exportar PDF

---

## Informacoes Criticas

### Estrutura de Dados (Firestore)

```typescript
{
  id: string;
  nome: string;
  Presenca?: {           // Campo com P maiuscula
    date: "YYYY-MM-DD";  // String, nao Date
    confirmada: boolean;
    modalidade?: string;
  }[];

  filhos?: {
    id: string;
    nome: string;
    Presenca?: [...];
  }[];

  modalidades?: {
    modalidade: string;
    graduacao?: string;
  }[];

  pagamento?: boolean;
  dataUltimoPagamento?: string;  // "YYYY-MM-DD"
}
```

### Regras

- Usar `Presenca` (maiuscula) - NAO `presenca` ou `presencas`
- Datas em formato "YYYY-MM-DD" (string)
- Contar APENAS presencas com `confirmada: true`
- Iterar usuarios > para cada > iterar filhos
- Pagamento ativo = dataUltimoPagamento nos ultimos 30 dias

---

## Tasks de Desenvolvimento

| Task | Descricao | Status |
|------|----------|--------|
| TASK-01 | Extrair presencaUtils.ts | ⬜ |
| TASK-02 | Extrair pdfUtils.ts | ⬜ |
| TASK-03 | Hook useAlunosPorModalidade | ⬜ |
| TASK-04 | Hook useAlunosSemPresenca | ⬜ |
| TASK-05 | Hook useRelatorioGraduacao | ⬜ |
| TASK-06 | Componente GraficoModalidades | ⬜ |
| TASK-07 | Componente ListaAlunosSemPresenca | ⬜ |
| TASK-08 | Componente RelatorioAptosGraduacao | ⬜ |
| TASK-09 | Componente RelatoriosScreen (container) | ⬜ |
| TASK-10 | Integracao em adminScreen | ⬜ |

---

## Tempo Estimado

| Fase | Tempo |
|------|-------|
| Utils (TASK-01, 02) | 1.5h |
| Hooks (TASK-03, 04, 05) | 3h |
| Componentes (TASK-06 a 09) | 4h |
| Integracao (TASK-10) | 0.5h |
| Testes | 2h |
| **Total** | **~11h** |

---

## Referencia

Spec completa em: `docs/` ou outro local do projeto