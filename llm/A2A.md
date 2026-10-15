**Agent-to-Agent (A2A)** refers to an open communication protocol and interoperability standard that allows autonomous AI agents from different platforms, frameworks, or vendors to ==🟣discover each other, share context, and collaborate== on complex tasks.
Introduced by Google and hosted by the Linux Foundation, it establishes a universal "language" so that AI systems are not locked into closed, siloed ecosystems.
## How A2A Works
1. **The [[Agent Card]]:** Every AI agent publishes a standard descriptive file (typically a JSON file located at a standardized path like `/.well-known/agent.json`). This card outlines the agent's capabilities, what it specializes in, and how to contact it.
2. **Discovery & Interoperability:** An AI agent can read another agent's Card to automatically understand what that agent is capable of doing.
3. **Standardized Communication:** Agents exchange goals, feedback, and execution steps using open standards (such as HTTPS, JSON-RPC 2.0, and Server-Sent Events).
4. **Task Delegation:** If "Agent A" (e.g., a travel planning agent) needs a highly specific subtask done that it cannot do itself (e.g., booking a niche local tour via a specialized local vendor's agent), it uses A2A to securely hand off that specific part of the job.
## A2A & MCP
While both aim to make LLM applications more capable, they serve completely different purposes in the AI tech stack:
- **MCP:** Connects an AI model to **data sources and infrastructure** (like a database, local files, or developer tools). It acts like a universal adapter/USB cable for a single AI to access tools.
- **A2A:** Connects **one AI mind to another AI mind** directly. It is a *peer-to-peer* collaboration protocol for independent autonomous agents to work together.
