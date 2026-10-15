Standard descriptive file (typically a JSON file located at a standardized path like `/.well-known/agent.json`). 
This card outlines the agent's capabilities, what it specializes in, and how to contact it.
## Agent Card schema (example) - https://docs.cloud.google.com/agent-registry/json-schemas

```json
{
  "name": "string",
  "description": "string",
  "version": "string",
  "supportedInterfaces": [
    {
      "url": "string",
      "protocolBinding": "string",
      "protocolVersion": "string",
      "tenant": "string"
    }
  ],
  "capabilities": {
    "streaming": false,
    "pushNotifications": false,
    "extendedAgentCard": false
  },
  "defaultInputModes": [
    "text/plain"
  ],
  "defaultOutputModes": [
    "text/plain"
  ],
  "skills": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "tags": [
        "string"
      ],
      "examples": [
        "string"
      ]
    }
  ]
}
```
## Reference
[[A2A]]
