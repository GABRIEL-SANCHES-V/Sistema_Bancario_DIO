# Value Objects

Este módulo contém os **Value Objects** utilizados no domínio do sistema bancário.

Value Objects são objetos:

* imutáveis
* comparáveis por valor
* responsáveis por validação e normalização de dados

---

# Estrutura

```
value_objects/
│
├── address.py
├── birth_date.py
├── cpf.py
├── email.py
├── money.py
├── name.py
├── password.py
├── phone_number.py
├── state.py
└── zip_code.py
```

Cada arquivo representa um conceito do domínio.

---

# Princípios de Design

## Imutabilidade

Todos os Value Objects são imutáveis.

```python
def __setattr__(self, key, value):
    raise ValueError("Objeto imutável")
```

---

## Comparação por valor

```python
Email("user@email.com") == Email("user@email.com")
```

Resultado:

```
True
```

---

## Normalização de dados

| VO          | Normalização           |
| ----------- | ---------------------- |
| Name        | capitalização          |
| Email       | minúsculas             |
| PhoneNumber | remove caracteres      |
| CPF         | remove pontuação       |
| ZipCode     | remove hífen           |
| Money       | Decimal com duas casas |

---

# Tratamento de erros

```
DomainError
   └── ValueObjectError
        ├── InvalidTypeError
        └── InvalidValueError
```

---

# Exemplos de Uso

### Email

```python
email = Email("USER@EMAIL.COM")
print(email.value)
```

Saída:

```
user@email.com
```

---

### Money

```python
valor = Money("100.50")
```

---

# Guidelines para novos Value Objects

1. Representar um conceito real do domínio
2. Ser imutável
3. Validar no construtor
4. Normalizar dados
5. Implementar `__eq__` e `__hash__`
