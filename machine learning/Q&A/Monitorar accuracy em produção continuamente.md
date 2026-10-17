# Monitorar Accuracy em Produção Continuamente

## Por que Monitorar?

Em produção, o modelo **está sujeito a [[Model drift|model drift]]**. A [[machine learning/quality/development/Accuracy|Accuracy]] **degrada com o tempo** se não for monitorada e retrainada.

```
Sem Monitoramento:
├─ Mês 1:  85% (Deploy)
├─ Mês 3:  78% (Ninguém sabe)
├─ Mês 6:  65% (Descobrem por reclamações)
└─ Mês 12: 45% (Desastre!)

Com Monitoramento:
├─ Mês 1:  85% ✅ (OK)
├─ Mês 3:  78% ⚠️ (Alerta enviado)
├─ Mês 6:  77% (Retreinado) → 83% ✅
└─ Mês 12: 82% ✅ (Controlado)
```

---

## Arquitetura de Monitoramento

### Componentes Necessários

```
┌─────────────────────────────────────────────┐
│         Dados em Produção                   │
│  (Previsões do modelo + Rótulos reais)      │
└────────────┬────────────────────────────────┘
             │
    ┌────────▼────────┐
    │ Collector       │ ← Coleta logs continuamente
    │ (Logs/Database) │
    └────────┬────────┘
             │
    ┌────────▼────────────┐
    │ Monitore            │ ← Calcula métricas
    │ (Daily/Hourly Job)  │  (accuracy, drift, etc)
    └────────┬────────────┘
             │
    ┌────────▼────────────┐
    │ Alert System        │ ← Envia alertas
    │ (Email, Slack, etc) │  se accuracy baixa
    └────────┬────────────┘
             │
    ┌────────▼────────────┐
    │ Dashboard           │ ← Visualiza histórico
    │ (Grafana, Tableau)  │
    └─────────────────────┘
```

---

## Métodos de Monitoramento

### 1. **[[machine learning/concepts/Ground Truth|Ground Truth]] (Ideal mas Caro)**

Coletar **rótulos reais** e comparar com previsões.

```python
# No banco de dados
previsão = modelo.predict(cliente_novo)
salvar_previsão(cliente_id, previsão, timestamp)

# Depois que o rótulo real fica disponível (dias/semanas depois)
rótulo_real = obter_rótulo_real(cliente_id)
salvar_rótulo_real(cliente_id, rótulo_real)

# Calcular accuracy com dados reais
y_real = carregar_rótulos_últimos_7_dias()
y_pred = carregar_previsões_últimos_7_dias()
accuracy = accuracy_score(y_real, y_pred)
```

**Problemas:**
- Rótulos reais levam tempo para aparecer (dias/semanas)
- Caro (precisa de feedback humano em alguns casos)
- Nem sempre disponível

**Latência Típica:**
```
t=0:   Modelo prediz "Approve crédito"
t=30:  Ground truth aparece (cliente pagou/não pagou)
t=30:  Calcula accuracy, descobre drift
```

---

## Quando NÃO Temos Ground Truth Imediato

**PROBLEMA:** Em um endpoint em produção, você não consegue calcular accuracy imediatamente. Precisa esperar dias/semanas por ground truth.

**SOLUÇÃO:** Use métricas alternativas rápidas!

---

### 2. **Confidence/Probability Scores** (⚡ Segundos)

Usar a **[[Confidence]] que o modelo tem** em sua previsão.

```python
# Modelo retorna probabilidade
y_pred_proba = modelo.predict_proba(X_novo)

# [0.2, 0.8] = 80% confiança em classe 1
confidence = max(y_pred_proba)

if confidence < 0.5:
    print("⚠️ Predição incerta, desconfia!")
    # Opções: pedir revisão humana, usar modelo alternativo
    
# Monitorar confiança média ao longo do tempo
confidence_mean = confidence.mean()
if confidence_mean < 0.65:  # Caiu confiança
    print("⚠️ Confiança média caiu!")
```

**Vantagem:** Instantâneo, simples
**Desvantagem:** Não é accuracy real, é proxy

---

### 3. **[[Proxy Metrics]] (⚡ Minutos/Horas)**

Usar métricas **proxy** que correlacionam com accuracy.

```python
# Exemplo: Detecção de fraude
# ✅ Proxy: Taxa de falsos positivos é aceitável?
# ✅ Proxy: Scores preditos mudaram de distribuição?

fraud_scores_prod = carregar_scores_último_dia()
fraud_scores_train = carregar_scores_treino()

# Comparar distribuição
from scipy.stats import ks_2samp
stat, pvalue = ks_2samp(fraud_scores_train, fraud_scores_prod)

if pvalue < 0.05:
    print("⚠️ Distribuição mudou! (Possível drift)")
```

**Vantagem:** Detecção rápida (minutos/horas)
**Desvantagem:** Não é accuracy real, é uma aproximação

---

### 4. **[[Prediction Distribution Monitoring]]** (⚡ Minutos)

Monitorar a **distribuição das previsões do modelo**.

```python
# Previsões de hoje
y_pred_hoje = modelo.predict(X_prod_hoje)
pred_dist_hoje = (y_pred_hoje == 1).mean()  # % classe 1

# Previsões de treino (baseline)
pred_dist_treino = (y_train == 1).mean()

# Comparar
if abs(pred_dist_hoje - pred_dist_treino) > 0.15:
    print("⚠️ Distribuição de previsões mudou!")
    print("   → 15% de mudança em taxa de positivos")
    print("   → Possível drift ou dados diferentes")
```

**Vantagem:** Rápido, não precisa de ground truth
**Desvantagem:** Não mede accuracy, detecta anomalia

---

### 5. **[[Modelo de Confiança]]** (⚡ Segundos)

Usar um **segundo modelo simples** para detectar quando o modelo principal erraria.

```python
# Modelo principal: XGBoost complexo
y_pred_main = xgboost_model.predict(X_prod)

# Modelo de confiança: Árvore simples (rápida)
y_pred_confidence = decision_tree.predict(X_prod)

# Se discordam, pode ser erro
disagreement_rate = (y_pred_main != y_pred_confidence).mean()

if disagreement_rate > 0.15:  # 15% de discordância
    print("⚠️ Modelos discordam muito! Possível erro")
    enviar_alerta()
```

**Vantagem:** Detecta erro sem ground truth
**Desvantagem:** Depende de modelo simples bem treinado

---

### 6. **[[User Feedback Loop]]** (📊 Dias)

Coletar feedback dos usuários sobre as previsões.

```python
# Após fazer previsão
previsão_id = "pred_12345"
previsão = modelo.predict(X)  # Prediz "não-fraud"

# Usuário clica "Isso está certo?"
# → "Sim" ou "Não"
feedback = obter_feedback_usuario(previsão_id)

if feedback == "não":
    # Isso é ground truth! Salvar
    salvar_ground_truth(previsão_id, y_real=verdadeiro)
    y_true_feedback.append(y_real)
    
# Calcular accuracy com feedback coletado
if len(y_true_feedback) > 50:
    accuracy_feedback = accuracy_score(y_pred_feedback, y_true_feedback)
    print(f"Accuracy (com feedback): {accuracy_feedback:.2%}")
```

**Vantagem:** Ground truth real
**Desvantagem:** Lento (dias/semanas), nem todos respondem

---

### 7. **[[champion and challenger]]: Retraining Automático Semanal** (📅 Semana)

Em vez de monitorar continuamente, **treinar novo modelo semanalmente** e comparar com o campeão.

```python
class ChampionChallengerPipeline:
    def treinar_semanalmente(self, X_recente, y_recente):
        """Executar a cada semana"""
        
        # 1. TREINAR CHALLENGER com dados novos
        challenger = RandomForestClassifier()
        challenger.fit(X_recente, y_recente)
        challenger_accuracy = challenger.score(X_test, y_test)
        
        # 2. CARREGAR CHAMPION (modelo em produção)
        champion = self.carregar_champion()
        champion_accuracy = champion.score(X_test, y_test)
        
        # 3. COMPARAR: Quem vence?
        if challenger_accuracy > champion_accuracy:
            print(f"🎉 CHALLENGER VENCEU! (+{challenger_accuracy - champion_accuracy:.1%})")
            self.deploy_challenger(challenger)  # Novo modelo para produção
        else:
            print(f"❌ Challenger perdeu")
            # Mantém modelo anterior
```

**Vantagem:** Automático, adapta-se a drift rápido
**Desvantagem:** Caro (retrain semanal), pode piorar

---

## Comparação de Métodos

| Método                                                       | Tempo      | Acurácia | Custo | Uso        |
| ------------------------------------------------------------ | ---------- | -------- | ----- | ---------- |
| **[[machine learning/concepts/Ground Truth\|Ground Truth]]** | ⏳ Semanas  | ✅ 100%   | $$$   | Referência |
| **[[Confidence]]**                                           | ⚡ Segundos | ~70%     | $     | Rápido     |
| **[[Proxy Metrics]]**                                        | ⚡ Minutos  | ~60%     | $     | Rápido     |
| **[[Prediction Distribution Monitoring]]**                   | ⚡ Minutos  | ~70%     | $     | Rápido     |
| **[[Modelo de Confiança]]**                                  | ⚡ Segundos | ~75%     | $$    | Rápido     |
| **[[User Feedback Loop]]**                                   | 📊 Dias    | ~90%     | $$    | Médio      |
| **[[champion and challenger]]**                              | 📅 Semana  | ✅ Real   | $$$   | Automático |

## Resumo

| Aspecto | Descrição |
|--------|-----------|
| **Por quê** | Detectar [[Model drift]] cedo |
| **O quê** | Accuracy (real), confiança, distribuição (proxy) |
| **Quando** | Diariamente (monitoramento) + Semanalmente (retrain) |
| **Como** | **Rápido:** Confidence → Proxy → Distribuição |
| | **Real:** Ground Truth → Accuracy → Alert |
| | **Automático:** Champion-Challenger semanal |
| **Ação** | Alerta → Investigação → Retrain → Deploy |
