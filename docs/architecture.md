# Arquitetura do Sistema

O sistema bancário segue os princípios de **Clean Architecture**, separando responsabilidades em camadas bem definidas.

Essa abordagem permite:

* baixo acoplamento
* alta coesão
* fácil manutenção
* maior testabilidade

---

# Estrutura de Camadas

```
src/
│
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── services/
│   └── exceptions/
│
├── application/
│   ├── use_cases/
│   └── dto/
│
├── infrastructure/
│   ├── repositories/
│   └── persistence/
│
└── interfaces/
    ├── cli/
    └── api/
```

---

# Camadas da Arquitetura

| Camada         | Responsabilidade                           |
| -------------- | ------------------------------------------ |
| Domain         | Regras de negócio                          |
| Application    | Casos de uso                               |
| Infrastructure | Persistência e integrações                 |
| Interfaces     | Interface com usuário ou sistemas externos |

---

# Dependências entre Camadas

A regra principal da arquitetura é:

**camadas externas dependem das internas.**

```
Interfaces
    ↓
Application
    ↓
Domain
```

O **domínio não depende de nenhuma outra camada**.

---

# Diagrama de Arquitetura

```
            ┌─────────────────┐
            │    Interfaces    │
            │   CLI / API      │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   Application    │
            │    Use Cases     │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │      Domain      │
            │ Entities / VO    │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Infrastructure   │
            │ Repositories     │
            └─────────────────┘
```

---

# Benefícios da Arquitetura

* isolamento da lógica de negócio
* facilidade de testes
* independência de frameworks
* evolução controlada do sistema
