# Trilha de estudos — além do código

> Contexto: com as IAs cobrindo boa parte da escrita de código, o foco de estudo passa a ser o que torna os *prompts* e as *decisões técnicas* melhores — arquitetura, boas práticas, cibersegurança e infraestrutura.
https://github.com/littlee/littlee.github.io/blob/master/OReilly.Fundamentals.of.Software.Architecture.2020.1.pdf
---

## 1. Arquitetura de software

- **Fundamentals of Software Architecture** (Ford & Richards) — trade-offs, sem prender a uma stack específica.
- **Clean Architecture** (Uncle Bob) — por que separar camadas; conecta bem com C#/.NET.
- Prática: pegar um projeto próprio já pronto e questionar "por que essa pasta está aqui, essa dependência aponta pra onde" — entender arquitetura lendo/criticando código real rende mais que só teoria.

## 2. Boas práticas / design

- **Refactoring** (Fowler) — reconhecer *code smells*, base para revisar o que a IA gera.
- Princípios **SOLID** aplicados a C#.
- Design patterns — não decorar todos; reconhecer os mais comuns (Repository, Factory, Strategy, Observer), já que a IA os usa (ou deveria) o tempo todo.

## 3. Cibersegurança

- **OWASP Top 10** (gratuito, curto, direto).
- Foco no stack atual (.NET + PostgreSQL): SQL injection, autenticação/autorização (JWT, OAuth), gestão de secrets.

## 4. Infraestrutura

- Docker básico — containerizar a própria API já ensina muito sobre deploy.
- Conceitos de CI/CD — entender o pipeline (build → test → deploy), sem precisar aprofundar em ferramenta específica ainda.
- Se quiser ir além: fundamentos de nuvem (Azure, por sinergia com .NET).

## 5. Como isso vira "prompt melhor"

Quanto mais entendimento de arquitetura/segurança, mais constraints específicas dá pra colocar no prompt ("aplica repository pattern", "valida contra SQL injection", "separa em camada de domínio") em vez de pedir algo genérico e aceitar o que vier.

Ler sobre os temas importa menos que **praticar revisando**: pegar um PR próprio ou código gerado por IA e tentar achar 3 problemas antes de aceitar.

---

## Ritmo sugerido

Dada a rotina corrida (home office + treino pesado), evitar curso longo. Escolher **1 tema por vez**, 20–30 min encaixados entre tarefas, e aplicar direto no código do trabalho.
