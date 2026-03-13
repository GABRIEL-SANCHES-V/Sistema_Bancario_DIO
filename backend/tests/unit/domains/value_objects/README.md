# Estratégia de Testes

O projeto utiliza **testes automatizados** para garantir a confiabilidade do domínio.

Os testes são implementados utilizando **pytest**.

---

# Objetivos dos Testes

Os testes têm como objetivo:

* validar regras de negócio
* garantir integridade dos Value Objects
* prevenir regressões
* facilitar refatorações seguras

---

# Estrutura dos Testes

```
tests/
│
└── unit/
    └── domains/
        └── value_objects/
```

---

# Tipos de Testes

## Testes de criação

Verificam se objetos válidos são criados corretamente.

## Testes de validação

Verificam se valores inválidos geram exceções.

## Testes de normalização

Garantem que os dados sejam normalizados corretamente.

## Testes de igualdade

Verificam comparação por valor.

## Testes de hash

Garantem compatibilidade com estruturas hash.

## Testes de imutabilidade

Garantem que Value Objects não possam ser modificados.

---

# Exemplo de Teste

```
def test_create_valid_email():
    email = Email("user@email.com")
    assert email.value == "user@email.com"
```

---

# Benefícios da Estratégia

* maior confiabilidade do sistema
* segurança para evoluir o código
* documentação executável das regras de domínio
