# Ground Truth

## O que é?

**Ground Truth** = Os **rótulos/respostas reais e corretos** para os dados.

É a "verdade do terreno" - aquilo que realmente aconteceu ou é correto, não a previsão do modelo.

**Dataset de treino = Features + Ground Truth**

---

## Exemplo Prático

```
Dados (Input):                Ground Truth (Output Real):
├─ Email: "Olá, ganhaste..."  ├─ Spam: SIM ✅
├─ Email: "Reunião amanhã"    ├─ Spam: NÃO ✅
└─ Email: "Compre agora!"     └─ Spam: SIM ✅

Modelo prediz:                 Comparação:
├─ Spam: SIM ✅ (correto)     ├─ Correto (acerto)
├─ Spam: NÃO ✅ (correto)     ├─ Correto (acerto)
└─ Spam: NÃO ❌ (errado)      └─ **ERRO** (modelo falhou)
```

---

## Onde Vem Ground Truth?

### 1. **Rótulos Humanos** (Mais Comum)

Humanos anotam manualmente os dados.

```
Processo:
├─ Coletar dados brutos
├─ Humanos anotam/rotulam
├─ Revisor verifica qualidade
└─ Usar como ground truth
```

**Exemplos:**
- 📧 Classificar emails como spam/legítimo
- 🏠 Precificar imóveis (avaliar valor real)
- 🖼️ Descrever conteúdo de imagens
- 🔬 Diagnosticar doença em raio-X

**Custo:** Alto (humanos precisam de tempo)
**Qualidade:** Depende da expertise dos anotadores

---

### 2. **Dados Históricos** (Natural)

Ground truth já existe em registros históricos.

```
Exemplo: Prever se cliente vai comprar

Dados: Cliente clicou em anúncio, viu produto, etc
Ground Truth: Comprou ou não? (histórico diz!)

Coleta automática, sem custos! ✅
```

**Exemplos:**
- 💳 Fraude (transação foi ou não fraudulenta - histórico sabe)
- 🎯 Conversão (cliente comprou - venda realizada)
- 🏥 Diagnóstico (paciente tinha doença - resultado de teste confirma)

**Custo:** Baixo (já existe)
**Qualidade:** Alta (fatos históricos)

---

### 3. **Feedback de Usuários** (Online)

Usuários fornecem feedback em produção.

```
Modelo prediz spam → Usuário clica "Não é spam"
Feedback = Ground Truth para aquela amostra
```

**Exemplos:**
- 👍 Rating "Isso foi útil?" / "Não foi útil"
- ⭐ Reviews de produtos
- 📸 Feedback em recomendações

**Custo:** Muito baixo (usuários fornecem)
**Qualidade:** Pode variar (nem todos respondem)
**Tempo:** Lento (feedback leva dias/semanas)

---

## Usos do Ground Truth

### 1. **Treinar o Modelo**

Ground truth é essencial para treinar.

```python
X_train = dados_de_treino
y_train = ground_truth_de_treino  # Labels corretos

modelo.fit(X_train, y_train)  # Aprender com truth
```

---

### 2. **Avaliar Accuracy**

Ground truth permite calcular accuracy real.

```python
y_pred = modelo.predict(X_test)
y_true = ground_truth_test  # Labels reais

accuracy = (y_pred == y_true).mean()  # Compara com verdade
```

**Sem ground truth, não dá pra saber se está certo!** ❌

---

### 3. **Detectar [[Model drift|Model Drift]]**

Em produção, ground truth ajuda detectar quando modelo degrada.

```python
# Produção por 3 meses
y_pred = [previsões do modelo]
y_true = [ground truth que apareceu depois]

accuracy = calcular_accuracy(y_pred, y_true)

if accuracy < threshold:
    print("⚠️ Model drift detectado!")
    retrain_model()
```

**Problema:** Ground truth leva tempo para aparecer!

---

## Desafios do Ground Truth

### 1. **Custo**

Coletar e anotar dados é **muito caro**.

```
100k amostras × $5 por amostra = $500k! 💸

Alternativas:
├─ Data augmentation (criar dados)
├─ Active learning (pedir ótimas amostras)
└─ Transfer learning (usar dados similares)
```

---

### 2. **Tempo de Latência**

Ground truth muitas vezes **leva dias/semanas para aparecer**.

```
Exemplo: Score de crédito

t=0:   Modelo prediz "Aprovar crédito"
t=0:   Cliente recebe cartão
t=30:  Cliente paga/não paga (ground truth!)
t=40:  Sabemos se acertamos

⏳ 40 dias de latência! Problema para monitoramento rápido
```

---

### 3. **Qualidade Inconsistente**

Anotadores humanos podem discordar.

```
Imagem ambígua: "É gato ou outro felino?"

Anotador A: Gato ✅
Anotador B: Lince (não é gato) ✅
Anotador C: Gato ✅

Qual é a "verdade"? 🤔
```

**Solução:** Inter-rater agreement (múltiplos anotadores)

---

### 4. **Viés nos Rótulos**

Anotadores podem introduzir viés.

```
Classificar imagens por gênero:

Anotador com viés:
├─ "Pessoa em cozinha" → Mulher
├─ "Pessoa com ferramenta" → Homem

Viés no ground truth → Viés no modelo! 😞
```

---

## Ground Truth vs Previsão

```
Ground Truth:
├─ Real (verdade)
├─ Sempre correto
├─ Caro de obter
└─ Usado para avaliar

Previsão do Modelo:
├─ Estimativa
├─ Pode estar errada
├─ Rápido e barato
└─ O que queremos melhorar
```

---

## Exemplo Completo: Detecção de Fraude

```python
# TREINO
X_train = [transação 1, transação 2, ...]
y_train = [fraudulenta?, fraudulenta?, ...]  # Ground truth
                ↑
         Histórico diz a verdade

modelo.fit(X_train, y_train)

# TESTE
X_test = [nova transação 1, nova transação 2, ...]
y_pred = modelo.predict(X_test)  # Previsão

# AVALIAR (depois que ground truth aparece)
y_true = [fraude confirmada?, ...]  # Ground truth do teste
              ↑
       Histórico de 30 dias depois

accuracy = (y_pred == y_true).mean()
print(f"Accuracy: {accuracy:.2%}")
```

---

## Estratégias para Reduzir Custo de Ground Truth

### 1. **Active Learning**

Pedir rótulo apenas para amostras incertas.

```
Modelo prevê:
├─ Email 1: "99% spam" → Confiante, não pede rótulo
├─ Email 2: "50% spam" → Incerto, pede rótulo ao humano
└─ Email 3: "95% legítimo" → Confiante, não pede rótulo
```

**Resultado:** 50% menos anotação, 90% da qualidade

---

### 2. **Weak Labels**

Usar rótulos automáticos (menos acurados).

```
❌ Ideal: Humano anota cada email manualmente ($$$)
✅ Prático: Usar regra automática "Contém palavra X = spam" ($)
```

**Trade-off:** Menos caro, menos preciso

---

### 3. **Transfer Learning**

Usar dados de um problema similar.

```
Problema: Classificar frutas (caro coletar)
Solução: Usar dados de classificação de plantas similares
```

**Resultado:** Menos dados novos necessários

---

### 4. **Crowdsourcing**

Usar múltiplos anotadores baratos.

```
Amazon Mechanical Turk:
├─ Múltiplos anotadores baratos
├─ Vote para determinar truth
└─ Custo total mais baixo
```

**Trade-off:** Qualidade variable, mas mais barato

---

## Checklist: Garantir Qualidade do Ground Truth

- ✅ Definir diretrizes claras para anotadores
- ✅ Ter múltiplos anotadores (inter-rater agreement)
- ✅ Revisor qualidade verifica aleatoriamente
- ✅ Documentar ambiguidades e exceções
- ✅ Medir concordância entre anotadores (Cohen's Kappa)
- ✅ Distribuir uniformemente entre classes
- ✅ Reanalisar ground truth periodicamente
- ✅ Testar impacto de "rótulos ruidosos" no modelo

---

## Ground Truth em Produção ([[Monitorar accuracy em produção continuamente|Monitoring]])

```
Ideal:           Realidade:
Tempo Real       Latência de dias/semanas
╔═════════╗      ╔═════════════════════════╗
║ Prediz  ║      ║ Prediz                  ║
║   ↓     ║      ║   ↓                     ║
║ Truth   ║      ║ ... 30 dias depois ...  ║
║ Accuracy║      ║   Ground Truth aparece  ║
║ Agora!  ║      ║   Calcula accuracy      ║
╚═════════╝      ╚═════════════════════════╝
```

**Soluções:**
- Usar [[Monitorar accuracy em produção continuamente|proxy metrics]] enquanto aguarda truth
- Monitorar distribuição dos dados (mais rápido)
- Usar modelo de confiança como alerta rápido

---

## Resumo

| Aspecto | Descrição |
|--------|-----------|
| **O quê** | Labels reais e corretos |
| **Fonte** | Humanos, histórico, usuários |
| **Uso** | Treinar, avaliar, monitorar |
| **Vantagem** | Saber a verdade exata |
| **Desafio** | Caro, lento, ambíguo |
| **Alternativa** | Proxy metrics, weak labels |

**Ground Truth é o alicerce de ML. Sem ela, não dá pra saber se está funcionando!** 📊
