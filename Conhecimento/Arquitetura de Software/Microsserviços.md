# Microsserviços

Estilo de arquitetura onde o sistema é dividido em **serviços pequenos e independentes**, cada um responsável por uma parte específica do negócio, ao invés de um único sistema grande fazendo tudo.

---

## O que é, na prática?

**Analogia:** pense num restaurante. No modelo **monolito**, uma única pessoa faz tudo — recebe o pedido, cozinha, serve, cobra. Se ela quebrar o braço, o restaurante inteiro para. No modelo de **microsserviços**, cada função é uma pessoa separada: um recebe o pedido, outro cozinha, outro serve, outro cobra. Se o garçom falta, a cozinha continua funcionando — só o atendimento é afetado.

Em software: em vez de um sistema único (`.NET` monolítico, por exemplo) que cuida de autenticação, pedidos, pagamento e notificação no mesmo processo e no mesmo deploy, você separa cada uma dessas responsabilidades em um **serviço próprio**, com seu próprio banco de dados e seu próprio ciclo de deploy, que conversam entre si pela rede (geralmente HTTP/REST ou mensageria).

---

## Monolito vs Microsserviços

| Aspecto | Monolito | Microsserviços |
|---|---|---|
| Deploy | Um único deploy para tudo | Cada serviço tem seu próprio deploy |
| Banco de dados | Um banco compartilhado | Cada serviço pode ter seu próprio banco |
| Escalabilidade | Escala o sistema inteiro | Escala só o serviço que precisa (ex: só o de pagamento em Black Friday) |
| Falha | Uma falha pode derrubar tudo | Falha isolada — só aquele serviço cai |
| Comunicação interna | Chamada de método direta (mesma memória) | Chamada de rede (HTTP, mensageria) — mais lenta e com mais pontos de falha |
| Complexidade | Simples de começar, difícil de manter conforme cresce | Complexo de operar desde o início (rede, versionamento, observabilidade) |
| Time | Um time cuida de tudo | Cada time pode ser dono de um serviço |

**Ponto central:** microsserviços não são "melhores" por padrão — trocam a complexidade de manter um sistema grande pela complexidade de operar vários sistemas pequenos conversando entre si. É um trade-off, não um upgrade automático.

---

## Como a comunicação acontece

Como cada serviço roda em processo separado, eles não podem simplesmente chamar um método um do outro como em C#. A comunicação acontece pela rede, geralmente de duas formas:

| Tipo | Como funciona | Exemplo |
|---|---|---|
| **Síncrona** | Um serviço chama o outro e espera a resposta | Serviço de Pedido chama a API do serviço de Pagamento via HTTP e aguarda o retorno |
| **Assíncrona** | Um serviço publica um evento e não espera resposta imediata | Serviço de Pedido publica "PedidoCriado" numa fila (ex: RabbitMQ), e o serviço de Notificação reage a esse evento quando puder |

### Exemplo ilustrativo (C#)

Num monolito, criar um pedido e notificar o cliente seria uma chamada direta, no mesmo processo:

```csharp
public class PedidoService
{
    private readonly NotificacaoService _notificacaoService;

    public void CriarPedido(Pedido pedido)
    {
        _repositorio.Salvar(pedido);
        _notificacaoService.Enviar(pedido.ClienteId, "Pedido criado!"); // chamada direta, mesma memória
    }
}
```

Em microsserviços, o serviço de Pedido não conhece o de Notificação diretamente — ele só publica um evento:

```csharp
public class PedidoService
{
    private readonly IEventPublisher _eventPublisher;

    public void CriarPedido(Pedido pedido)
    {
        _repositorio.Salvar(pedido);
        _eventPublisher.Publicar(new PedidoCriadoEvent(pedido.Id, pedido.ClienteId)); // publica e segue
    }
}
```

Quem cuida de notificar é outro serviço, rodando em outro processo, que está "escutando" esse evento. O de Pedido nem sabe que a notificação existe.

---

## Por que dividir assim?

1. **Deploy independente** — atualizar o serviço de Pagamento não exige redeployar o de Pedido.
2. **Escala independente** — em Black Friday, só o serviço de Pedido/Pagamento precisa de mais instâncias, não o de Relatórios.
3. **Isolamento de falha** — se o serviço de Recomendação cair, o cliente ainda consegue fechar a compra.
4. **Times autônomos** — em empresas grandes, cada time é dono de um ou poucos serviços, sem depender de coordenar deploy com todo mundo.

---

## Conceitos relacionados

- **Domain-Driven Design (DDD)** — costuma ser usado para decidir *onde* cortar um monolito em serviços (os "bounded contexts" viram candidatos a microsserviço).
- **API Gateway** — ponto único de entrada que direciona a requisição do cliente para o serviço correto.
- **Circuit Breaker** — padrão para evitar que a falha de um serviço derrube os outros em cascata.
- **Arquitetura Hexagonal / Clean Architecture** — organizam o *interior* de um serviço; microsserviços organizam o *sistema como um todo*. São camadas diferentes do mesmo problema.

---

## Erros Comuns

| Erro | Por que é um problema |
|---|---|
| Achar que microsserviços são sempre melhores que monolito | Trocam complexidade de código por complexidade operacional (rede, deploy, observabilidade) — só compensa em determinados tamanhos de time/sistema |
| Compartilhar o mesmo banco de dados entre serviços | Quebra o isolamento — um serviço muda uma tabela e derruba outro sem querer |
| Criar microsserviços "por moda", sem separar por domínio de negócio real | Gera serviços acoplados demais entre si (o pior dos dois mundos: complexidade de monolito + de rede) |
| Ignorar que chamadas de rede podem falhar | Uma chamada síncrona sem tratamento de timeout/retry pode travar o sistema inteiro em cascata |

---

## Resumo em uma frase

Microsserviços dividem um sistema em partes pequenas e independentes que conversam pela rede, trocando a complexidade de manter um código grande pela complexidade de operar vários serviços conectados.

---

## Quiz

**1. Qual a principal diferença entre monolito e microsserviços?**
- a) Microsserviços usam só C#, monolito só Java
- b) Monolito é um sistema único; microsserviços dividem o sistema em serviços independentes que se comunicam pela rede
- c) Microsserviços não usam banco de dados
- d) Não há diferença real, é só nome diferente

**2. Por que dois microsserviços normalmente não devem compartilhar o mesmo banco de dados?**
- a) Porque banco de dados compartilhado é mais caro
- b) Porque quebra o isolamento: uma mudança de um serviço pode derrubar o outro sem querer
- c) Porque bancos de dados não suportam múltiplas conexões
- d) Não há problema em compartilhar

**3. O que é comunicação assíncrona entre microsserviços?**
- a) Um serviço chama outro e espera a resposta na hora
- b) Um serviço publica um evento e outro reage quando puder, sem bloquear o primeiro
- c) Dois serviços rodando no mesmo processo
- d) Comunicação que só funciona à noite

**4. Microsserviços são sempre a escolha certa?**
- a) Sim, sempre é melhor que monolito
- b) Não — é um trade-off: resolve alguns problemas (escala, deploy independente) mas introduz outros (complexidade de rede, observabilidade)
- c) Só funcionam com Node.js
- d) Só existem em empresas pequenas

### Gabarito

| Pergunta | Resposta |
|---|---|
| 1 | b |
| 2 | b |
| 3 | b |
| 4 | b |

**Explicações:**

1. O monolito roda tudo num processo/deploy só; microsserviços separam responsabilidades em serviços que rodam independentemente e se comunicam pela rede.
2. Banco compartilhado acopla os serviços por baixo dos panos — mesmo que o código pareça independente, uma migration num serviço pode quebrar o outro.
3. Assíncrono = publica e segue; quem reage ao evento faz isso no próprio tempo, sem travar quem publicou.
4. Não existe arquitetura "sempre certa" — depende do tamanho do time, da necessidade de escala e da maturidade operacional (observabilidade, CI/CD, etc).

---

## Links

- [[Arquitetura de Software/Conhecimentos|Arquitetura de Software]]
- [[Manu/Indice|Voltar ao Indice]]
