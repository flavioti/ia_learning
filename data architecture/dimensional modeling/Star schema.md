---
tags:
  - dimensional-modeling-technique
---
É uma técnica de modelagem dimensional usada em [[OLAP Database]],  [[OLTP Database]] e [[Data Warehouse|data warehouse]].

## Componentes principais

- Tabela de fatos: Armazena dados numéricos e métricas quantificáveis, na menor granularidade possível, chaves estrangeiras que apontam para dimensões.
- Tabela de dimensões: Armazena atributos descritivos e o contexto do negócio (nome do produto, dados do cliente)

## Diagrama

```mermaid
erDiagram
    FACT_SALES {
        int date_key FK
        int product_key FK
        int customer_key FK
        int store_key FK
        int quantity
        decimal amount
    }
    DIM_DATE {
        int date_key PK
        date full_date
        int month
        int year
    }
    DIM_PRODUCT {
        int product_key PK
        string name
        string category
    }
    DIM_CUSTOMER {
        int customer_key PK
        string name
        string city
    }
    DIM_STORE {
        int store_key PK
        string name
        string region
    }

    DIM_DATE ||--o{ FACT_SALES : "date_key"
    DIM_PRODUCT ||--o{ FACT_SALES : "product_key"
    DIM_CUSTOMER ||--o{ FACT_SALES : "customer_key"
    DIM_STORE ||--o{ FACT_SALES : "store_key"
```
