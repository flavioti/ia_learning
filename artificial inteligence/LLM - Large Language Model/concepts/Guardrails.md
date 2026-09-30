[[harness]]

Guardrails is a collection of static rules, best pratices to ensure that model response meet the product requirements.
- resilient
- prevent malicious atacks


Example of CREATE_AGENT from [[LangChain]]

```mermaid
flowchart TD
__start__([__start__])
__end__([__end__])
A([DeterministicInputGuardrail.before_agent])
B([PIIDataGuardrail.before_model])
C([model])
D([HumanApprovalActionGuardrail.after_model])
E([PIIDataGuardrail.after_model])
F([Tools])
G([LLMJudgeOutputGuardrail.after_agent])
__start__-->A
A-->B
B-->C
C-->D
D-->E
E-->F
E-->G
F-->B
G-->__end__
```


#bestpratice
