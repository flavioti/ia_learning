# Categorical Columns

## 1. By Order (Primary Classification)

| Type        | Definition                           | Examples                                    | Encoding                                | ML Impact                                                             |
| ----------- | ------------------------------------ | ------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------- |
| **Nominal** | No inherent order between categories | color, country, gender, brand               | One-hot, label (with caution)           | Trees handle naturally; linear models need one-hot                    |
| **Ordinal** | Natural ordering between categories  | education level, rating, shirt size (S<M<L) | Ordinal encoding, one-hot (loses order) | Ordinal encoding preserves relationship; important for distance-based |

## 2. By Number of Categories

| Type | Definition | Examples | Encoding | Cardinality |
|------|-----------|----------|----------|------------|
| **Binary** | Exactly 2 categories | yes/no, true/false, male/female | 0/1, boolean | 2 values |
| **Multiclass** | More than 2 categories | countries, product types, segments | One-hot, label, target encoding | >2 values |

## 3. By Cardinality (Unique Values)

| Type | Definition | Examples | Safe for One-Hot? | Best Encoding |
|------|-----------|----------|------------------|----------------|
| **Low Cardinality** | Few unique values (< 20) | country, gender, category | ✅ Yes | One-hot encoding |
| **High Cardinality** | Many unique values (1000s+) | user ID, address, postal code | ❌ No | Target encoding, embeddings, frequency encoding |

## 4. By Temporal/Cyclic Nature

| Type | Definition | Examples | Encoding | Why Important |
|------|-----------|----------|----------|---------------|
| **Cyclic** | Categories that repeat | month, day of week, season, hour | Sine/cosine transform, circular one-hot | Dec ≠ Jan distance should be 1, not 11 |
| **Non-Cyclic** | Regular categories | color, country, category | Standard one-hot or ordinal | Regular distance metrics apply |

## 5. By Relationship Structure

| Type | Definition | Examples | Encoding |
|------|-----------|----------|----------|
| **Hierarchical** | Parent-child relationships | Country→State→City, Category→Subcategory | Target encoding respecting hierarchy, graph embeddings |
| **Independent** | No relationships | gender, color, brand | Standard encoding (one-hot, ordinal) |

---

## Encoding Strategy by Type

| Categorical Type | Best Encoding | Tree-Based | Linear Models | Distance-Based | Neural Networks |
|-----------------|---------------|-----------|----------------|-----------------|-----------------|
| Nominal, Low Card | One-hot | ✅ Native | ✅ Required | ⚠️ With caution | ✅ Embeddings |
| Ordinal | Ordinal encoding | ✅ Native | ✅ Recommended | ✅ Preserves order | ✅ Embeddings |
| High Cardinality | Target, Embeddings | ✅ Native | ✅ Recommended | ✅ Reduces dims | ✅ Embeddings |
| Cyclic | Sine/Cosine | ✅ Native | ✅ Recommended | ✅ Captures cycle | ✅ Embeddings |
| Binary | 0/1 or Label | ✅ Native | ✅ Native | ✅ Native | ✅ Native |

---

## Fictional Dataset Example: E-commerce Customer Dataset

Complete example showing all categorical variable types:

| Customer_ID | Product_Color | Product_Brand | Country | Product_Quality | Subscription_Status | Purchase_Day | Season | Price_Tier | Product_Category | Rating | Membership_Status |
|-------------|---------------|---------------|---------|-----------------|---------------------|--------------|--------|------------|------------------|--------|-------------------|
| CUST001 | Red | Nike | USA | High | Active | Monday | Spring | Premium | Shoes | 5 Stars | Gold |
| CUST002 | Blue | Adidas | Brazil | Medium | Inactive | Tuesday | Summer | Standard | Apparel | 4 Stars | Silver |
| CUST003 | Black | Puma | Germany | Low | Active | Wednesday | Fall | Basic | Accessories | 3 Stars | Bronze |
| CUST004 | Green | Nike | Japan | High | Active | Thursday | Winter | Premium | Shoes | 5 Stars | Gold |
| CUST005 | White | Adidas | Canada | Medium | Inactive | Friday | Spring | Standard | Apparel | 2 Stars | Bronze |
| CUST006 | Yellow | Reebok | France | High | Active | Saturday | Summer | Premium | Accessories | 4 Stars | Silver |
| CUST007 | Purple | Nike | Australia | Medium | Active | Sunday | Fall | Standard | Shoes | 3 Stars | Gold |

### Column Classification:

| Column                | Type    | Subtype      | Values                                                 | Cardinality | Encoding Suggestion      | Exemplo de Encoding                                    |
| --------------------- | ------- | ------------ | ------------------------------------------------------ | ----------- | ------------------------ | ------------------------------------------------------ |
| `Product_Color`       | Nominal | Independent  | Red, Blue, Black, Green, White, Yellow, Purple         | Low         | One-hot encoding         | Red → [1,0,0,0,0,0,0], Blue → [0,1,0,0,0,0,0]          |
| `Product_Brand`       | Nominal | Independent  | Nike, Adidas, Puma, Reebok                             | Low         | One-hot encoding         | Nike → [1,0,0,0], Adidas → [0,1,0,0]                   |
| `Country`             | Nominal | Hierarchical | USA, Brazil, Germany, Japan, Canada, France, Australia | Medium      | One-hot encoding         | USA → [1,0,0,0,0,0,0], Brazil → [0,1,0,0,0,0,0]        |
| `Product_Quality`     | Ordinal | Independent  | Low < Medium < High                                    | Low         | Ordinal: [1, 2, 3]       | Low → 1, Medium → 2, High → 3                          |
| `Price_Tier`          | Ordinal | Independent  | Basic < Standard < Premium                             | Low         | Ordinal: [1, 2, 3]       | Basic → 1, Standard → 2, Premium → 3                   |
| `Rating`              | Ordinal | Independent  | 2 Stars < 3 Stars < 4 Stars < 5 Stars                  | Low         | Ordinal: [1, 2, 3, 4, 5] | 2 Stars → 1, 3 Stars → 2, 4 Stars → 3, 5 Stars → 4     |
| `Membership_Status`   | Ordinal | Independent  | Bronze < Silver < Gold                                 | Low         | Ordinal: [1, 2, 3]       | Bronze → 1, Silver → 2, Gold → 3                       |
| `Purchase_Day`        | Cyclic  | Non-Cyclic   | Monday-Sunday                                          | Low (7)     | Sine/Cosine transform    | Monday → sin(0), cos(0); Sunday → sin(2π), cos(2π)     |
| `Season`              | Cyclic  | Cyclic       | Spring, Summer, Fall, Winter                           | Low (4)     | Sine/Cosine transform    | Spring → sin(0), cos(0); Winter → sin(3π/2), cos(3π/2) |
| `Subscription_Status` | Binary  | Independent  | Active, Inactive                                       | 2 values    | 0/1 encoding             | Active → 1, Inactive → 0                               |
| `Product_Category`    | Nominal | Independent  | Shoes, Apparel, Accessories                            | Low         | One-hot encoding         | Shoes → [1,0,0], Apparel → [0,1,0]                     |
| `Customer_ID`         | Nominal | Independent  | CUST001, CUST002, ...                                  | High        | Embeddings or exclude    | Embedding: [0.12, -0.45, 0.78, ...] (vector 128-dim)   |
One-hot encoding: Cria uma coluna binaria para cada valor unico da variável categórica (==Aumenta== dimensão da tabela)
Ordinal encoding: Mantém a coluna, mas converte para valores numéricos (==Não aumenta== dimensão da tabela)
