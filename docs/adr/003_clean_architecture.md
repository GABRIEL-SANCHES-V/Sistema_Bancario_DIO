
---

# 📄 003-clean-architecture.md

```markdown
# ADR 003 — Clean Architecture

Status: Accepted

---

# Context

O sistema bancário precisa ser:

- evolutivo
- testável
- independente de frameworks
- capaz de trocar interfaces (CLI, API, etc)

Misturar regras de negócio com infraestrutura pode gerar:

- forte acoplamento
- dificuldade de testes
- dependência de frameworks

---

# Decision

O sistema seguirá os princípios de **Clean Architecture**, separando responsabilidades em camadas.

Estrutura adotada:
