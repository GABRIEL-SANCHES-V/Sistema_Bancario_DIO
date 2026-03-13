# Regras do Sistema Bancário — Versão 1

Este documento descreve as regras de negócio da **primeira versão do sistema bancário**.

---

# Operações Disponíveis

O sistema possui três operações principais:

* Depósito
* Saque
* Extrato

---

# Depósito

Regras:

* qualquer valor positivo é permitido

Exemplo:

```
depositar(100)
```

---

# Saque

Regras:

* limite máximo de **R$ 500 por saque**
* máximo de **3 saques por dia**
* o usuário deve possuir **saldo suficiente**

Exemplo:

```
sacar(200)
```

---

# Extrato

O extrato deve exibir:

* todas as movimentações realizadas
* saldo atual da conta

Exemplo:

```
===== EXTRATO =====

Depósito: R$ 100.00
Saque:    R$ 50.00

Saldo atual: R$ 50.00
```

Caso não haja movimentações:

```
Não foram realizadas movimentações
```

---

# Objetivo da Versão 1

A primeira versão do sistema tem como objetivo:

* validar regras básicas de operações bancárias
* construir a base do domínio
* preparar o sistema para evoluções futuras
