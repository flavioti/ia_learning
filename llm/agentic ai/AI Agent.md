Is a specialized software component designed to perform a specific, narrow task autonomously using tools and memory.
Basic example: Components of an AI agent
```mermaid
flowchart LR
    %% Styling
    classDef business fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef foundational fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef associate fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef micro fill:#eceff1,stroke:#455a64,stroke-width:2px;
    
	A([Human]):::micro
	subgraph Agent Mesh
		subgraph AI Agent
			B([Model + Harness]):::business
			C([🧰 Tools]):::associate	
		end
		subgraph AI Agent
			G([Model + Harness]):::business
		end
	end
	E([⚙ MCP]):::foundational
	F([🧰 Tools]):::associate
	H([⚙ MCP]):::foundational
	I([🧰 Tools]):::associate
	A<--HTTP-->B
	B<-->C
	B--discovery-->E
	E<-->F
	G<--A2A protocol-->B
	G<--discovery-->H
	H<-->I
```

> [!NOTE] About
> Model + Harness = AI Agent
> 

## References
[[MCP]]
[[Harness]]
