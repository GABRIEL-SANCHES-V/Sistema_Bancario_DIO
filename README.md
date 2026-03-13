# 🏦 Sistema Bancário

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://img.shields.io/badge/tests-pytest-green)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
![Architecture](https://img.shields.io/badge/architecture-Clean%20Architecture-orange)
![DDD](https://img.shields.io/badge/pattern-DDD-blueviolet)

---

# 📖 Visão Geral

Este projeto implementa um **Sistema Bancário** utilizando:

* Domain Driven Design (DDD)
* Clean Architecture
* Value Objects
* Testes automatizados

O objetivo é construir um domínio robusto e bem modelado que possa evoluir para um sistema bancário completo.

---

# 🏗️ Arquitetura

O projeto segue **Clean Architecture**, separando responsabilidades em camadas:

* **Domain** → regras de negócio
* **Application** → casos de uso
* **Infrastructure** → persistência e integrações
* **Interfaces** → CLI / API

Mais detalhes:

* [Arquitetura](docs/architecture.md)
* [DDD](docs/ddd.md)

---

# 🏦 Regras do Sistema Bancário — Versão 1

O sistema possui três operações principais:

### Depósito

* qualquer valor positivo

### Saque

* limite de **R$ 500 por saque**
* máximo de **3 saques por dia**
* deve possuir **saldo suficiente**

### Extrato

Deve exibir:

* todas as movimentações
* saldo final

Caso não haja movimentações:

```
Não foram realizadas movimentações
```

Regras completas:

→ `docs/banking_rules_v1.md`

---

# 📚 Documentação

* Arquitetura → `docs/architecture.md`
* Domain Driven Design → `docs/ddd.md`
* Value Objects → `src/domain/value_objects/README.md`
* Test Strategy(Value Objects) → `tests/unit/domains/value_objects/README.md`
* ADR → `docs/adr/`

---

# 🚀 Evolução do Projeto

Próximas implementações incluem:

* Entities (`Account`, `Transaction`)
* Casos de uso (`Deposit`, `Withdraw`)
* API REST
* Persistência
* Sistema de autenticação
* Logs e auditoria
