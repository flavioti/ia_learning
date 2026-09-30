[[AI agent]]
from [[LangChain Inc]]

```mermaid
flowchart LR
B[1 before_agent]
C[2 before_model]
subgraph wrap_tool_call
	S1[3 Tools]
end
subgraph wrap_model_call
	S2[4 Model]
end
E["5 after_model\n(postmodel)"]
F["6 after_model"]
B-->C
C-->wrap_tool_call
C-->wrap_model_call
wrap_tool_call-->E
wrap_model_call-->E
E-->F
```


- Before message reach the model, do a validation.
- If the tool make search on the internet, It must be checked

Python example
```python
agent = create_agent(
	model = agent_model,
	tools = (publish_internal_notice),
	middleware = [
		# Layers
		DeterministicInputGuardrail(banned_keywords="lack", "exploit"),
		PIIDataGuardrail(),
		HumanApprovalActionGuardrail(
			interrupt_one(
				"publish_internal_notice": {"allowed_decisions": ["approve", "edit", "reject"]}
			)
		),
		LLMJudgeOutputGuardrail(),
	],
	state_schema=LayeredAuditState,
	checkpointer=InMemorySaver(),
	system_prompt=(
		"Responda de forma objetiva. Use a tool publish_internal_notice apenas quando o usuário pedir explicitamente para publicar"
	)
)
diplay(Image(agent.get_graph().draw_mermaid_png()))
```


> [!NOTE] [[MCP]] and [[Tools]]
> TIP: Langchain workflow can call tool directly, use [[MCP]] for standardaize and if the tool will be reused between systems.

Examples:
[[ExampleLangchainCreateAgent.ipynb]]
