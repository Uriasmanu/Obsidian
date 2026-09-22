# MCP (Model Context Protocol)

Protocolo aberto que padroniza como um modelo de IA se conecta a ferramentas e fontes de dados externas — banco de dados, Slack, Gmail, um sistema interno.

---

## O que é

**Analogia:** pensa no USB-C. Antes dele, cada fabricante tinha seu próprio conector — um cabo pra cada celular, outro pra cada notebook. Hoje qualquer dispositivo com USB-C conversa com qualquer outro que também tenha USB-C, sem adaptador proprietário.

MCP é isso pra IA: em vez de cada aplicação de IA precisar de uma integração escrita à mão pra cada ferramenta, a ferramenta implementa o protocolo **uma vez** como servidor, e qualquer aplicação de IA que "fale" MCP consegue usá-la.

**Problema que resolve:** sem um padrão, se você tem *N* aplicações de IA e quer conectar a *M* ferramentas, acaba escrevendo *N × M* integrações diferentes (o "problema N×M"). MCP elimina isso.

---

## As três peças

| Termo | Tradução prática |
|---|---|
| **Host** | A aplicação de IA em si (ex: Claude Code, Claude Desktop) — quem decide usar uma ferramenta |
| **Client** | Componente dentro do host, um para cada servidor conectado — cuida da conexão técnica |
| **Server** | Processo separado que expõe capacidades: *tools* (ações), *resources* (dados legíveis) e *prompts* (templates prontos) |

---

## Como o fluxo funciona, passo a passo

1. O **host** inicia e lê a config de quais servidores MCP existem (ex: servidor de Gmail, servidor de banco de dados).
2. O **client** (dentro do host) abre conexão com o **server** — via stdio (processo local) ou HTTP/SSE (remoto).
3. O client pergunta ao server: "o que você sabe fazer?" — isso é o **discovery**.
4. O server responde com a lista de tools/resources, cada um com nome, descrição e schema de parâmetros (um contrato em JSON).
5. O usuário faz um pedido em linguagem natural (ex: "manda um email pro fulano").
6. O **modelo (LLM)** decide, com base nas descrições recebidas no passo 4, qual tool chamar.
7. O client executa a chamada no server, que roda a ação de verdade e devolve o resultado.
8. O resultado volta pro contexto do modelo, que continua a resposta usando essa informação.

Repara: o LLM nunca fala direto com o Gmail. Ele só vê a "prateleira de ferramentas" que o servidor MCP expôs e decide qual pegar.

---

## MCP x REST API x Function Calling

| Aspecto | REST API tradicional | MCP |
|---|---|---|
| Quem consome | Código específico, escrito à mão pra aquele endpoint | Qualquer LLM host compatível, sem código customizado |
| Descoberta do que existe | Você lê a documentação (Swagger, etc.) e programa contra ela | O client pergunta em tempo real ("list tools") e o LLM decide sozinho |
| Formato da conversa | HTTP + JSON, livre | JSON-RPC 2.0, com schema padronizado de mensagens |
| Quem decide chamar | Seu código, com `if`/lógica fixa | O modelo, interpretando linguagem natural |

MCP não substitui REST — muitas vezes um servidor MCP é só uma casca em volta de uma API REST já existente. O que ele padroniza é a **camada de exposição pro LLM**, não necessariamente o transporte de dados por trás.

---

## Exemplo real (Node/TypeScript)

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "clientes-db", version: "1.0.0" });

server.tool(
  "buscar_cliente",
  { cpf: z.string() },        // schema de parâmetros — o "contrato" do discovery
  async ({ cpf }) => {
    const cliente = await db.query("SELECT * FROM clientes WHERE cpf = $1", [cpf]);
    return { content: [{ type: "text", text: JSON.stringify(cliente) }] };
  }
);

server.connect(new StdioServerTransport());
```

O `server.tool(...)` é exatamente o passo 4 do fluxo: registra o que o LLM vai "ver" quando perguntar o que esse servidor sabe fazer.

---

## Conceitos relacionados

- **Function calling / tool use**: mecanismo do lado do LLM que decide *qual* função chamar — MCP padroniza *como* essa função é descoberta e chamada entre aplicações diferentes.
- **API REST**: MCP frequentemente embrulha uma API REST já existente.
- **Webhook**: também conecta sistemas, mas ao contrário — o servidor externo *empurra* dados, não o LLM que *pede*.

---

## Erros Comuns

| Erro | Por que está errado |
|---|---|
| "MCP é exclusivo da Anthropic" | É um protocolo aberto — qualquer empresa pode implementar client ou server |
| "O servidor MCP decide o que fazer" | Quem decide é o LLM no host; o servidor só expõe capacidades e executa quando chamado |
| "MCP é só uma API REST com outro nome" | MCP padroniza discovery + formato de mensagens (JSON-RPC) especificamente para consumo por LLM |

**Resumo em uma frase:** MCP é o protocolo padrão que permite qualquer LLM host descobrir e chamar ferramentas/dados externos de forma uniforme, eliminando a necessidade de integração customizada para cada par aplicação-ferramenta.

---

## Quiz

**1. No fluxo do MCP, quem decide qual tool chamar?**

A) O server

~~B) O modelo (LLM), com base no discovery~~

C) O client

**2. Qual a maior diferença entre MCP e uma API REST tradicional?**

A) MCP é mais rápido

~~B) MCP padroniza discovery e formato de mensagens pra consumo por LLM~~

C) MCP não usa JSON

**3. O que resolve o "problema N×M" que o MCP ataca?**

A) Excesso de servidores rodando ao mesmo tempo

~~B) A necessidade de escrever uma integração customizada para cada par aplicação × ferramenta~~

C) Lentidão de rede em APIs REST

---

## Links

- [[Manu/Indice|Voltar ao Indice]]
