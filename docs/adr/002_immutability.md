
---

# 📄 002-immutability.md

```markdown
# ADR 002 — Immutability

Status: Accepted

---

# Context

Objetos do domínio representam estados do sistema bancário.

Permitir mutação direta desses objetos pode causar:

- estados inconsistentes
- efeitos colaterais inesperados
- dificuldade de rastrear mudanças
- maior complexidade de testes

Especialmente em **Value Objects**, mutabilidade pode quebrar o conceito de igualdade por valor.

---

# Decision

Objetos de domínio devem ser **imutáveis sempre que possível**.

Isso significa:

- após criação, seu estado não pode ser alterado
- qualquer mudança gera **um novo objeto**

Exemplo:

```python
new_balance = balance.add(Money(100))