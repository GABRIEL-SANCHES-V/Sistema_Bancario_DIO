# ADR 001 — Use Value Objects

Status: Accepted

---

# Context

O sistema bancário possui diversos conceitos do domínio que não possuem identidade própria, mas representam valores com significado específico.

Exemplos:

- dinheiro
- número de conta
- limite de saque
- saldo

Representar esses conceitos como tipos primitivos (int, float, string) pode gerar:

- lógica duplicada
- validações espalhadas
- baixo expressividade no domínio

---

# Decision

O projeto adotará **Value Objects** para representar conceitos importantes do domínio.

Value Objects:

- são **imutáveis**
- **não possuem identidade**
- são comparados por **valor**
- encapsulam **regras e validações**

Exemplo:

```python
Money(100)