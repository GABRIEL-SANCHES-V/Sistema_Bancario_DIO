# Domain Driven Design

O projeto aplica princípios de **Domain Driven Design (DDD)** para modelar o domínio bancário.

DDD ajuda a criar software que reflete fielmente o domínio de negócio.

---

# Conceitos Utilizados

O projeto utiliza os seguintes conceitos de DDD:

* Entities
* Value Objects
* Domain Services
* Aggregates
* Domain Exceptions

---

# Entities

Entities são objetos que possuem **identidade própria**.

Exemplo futuro no sistema bancário:

```
Account
Transaction
Customer
```

Esses objetos são identificados por um **ID único**.

---

# Value Objects

Value Objects representam conceitos definidos apenas por seus **valores**.

Eles são:

* imutáveis
* comparáveis por valor
* responsáveis por validação e normalização

Exemplos no sistema:

| Value Object | Representa           |
| ------------ | -------------------- |
| Name         | nome de usuário      |
| Email        | endereço de email    |
| CPF          | documento brasileiro |
| Money        | valor monetário      |
| PhoneNumber  | telefone             |

---

# Linguagem Ubíqua

DDD incentiva o uso de **Ubiquitous Language**, ou seja, uma linguagem comum entre:

* desenvolvedores
* especialistas de domínio
* stakeholders

No projeto, exemplos incluem:

* Account
* Transaction
* Balance
* Deposit
* Withdraw

Esses termos aparecem tanto na documentação quanto no código.

---

# Benefícios do DDD

* domínio mais claro
* código mais expressivo
* regras de negócio centralizadas
* melhor comunicação entre equipe técnica e negócio
