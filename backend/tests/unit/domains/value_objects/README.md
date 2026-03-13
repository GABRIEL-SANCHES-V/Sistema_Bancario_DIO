# Test Strategy

Este projeto utiliza **testes unitários com pytest**.

Objetivos:

* validar regras de domínio
* garantir consistência dos Value Objects
* prevenir regressões

---

# Estrutura

```
tests/
└── unit/
    └── domains/
        └── value_objects/
```

---

# Tipos de testes

* criação válida
* valores inválidos
* normalização
* igualdade por valor
* hash
* imutabilidade

---

# Exemplo

```python
def test_create_valid_email():
    email = Email("user@email.com")
    assert email.value == "user@email.com"
```
