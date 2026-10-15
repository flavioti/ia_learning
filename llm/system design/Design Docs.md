## Status

Draft -> Proposed --> Accepted --> Deprecated or superseded
## Documents

### Hierarchy
`PRD → RFC → ADR → FDD`

1. [[RFC - Request for comments]] #low-level 
	1. Consolide a proposta técnica em cima das decisões, deve haver links apontando para [[ADR - Architecture Decision Record]]
2. [[ADR - Architecture Decision Record]] #high-level 
	- Registram decisões arquiteturais ao longo de todo processo
	- Leve e rastreável. Registra decisões arquiteturais ao longo do tempo. É o padrão ouro de governança técnica moderna. 
- [[FDD - Feature Design Doc]] #low-level
	- Como a feature especifica será implementada
	- Define o “como implementar” de uma feature. É o sucessor direto do FRD, mas focado em clareza e execução técnica. Mostra a arquitetura geral, componentes e integrações. É o alicerce técnico de toda a documentação moderna.
	- Usa linguagem [[Gherkin]]
- [[PRD - Product Requirement Document]] #mid-level
	- Liga visão de negócio à execução técnica. Define propósito, valor e métricas. É leve, iterativo e coescrito por PMs e tech leads.
- [[HLD - High Level Design]] #high-level 
	- Como o sistema é estruturado
	- Mostra a arquitetura geral, componentes e integrações. É o alicerce técnico de toda a documentação moderna.
- [[LLD - Low Level Design]] #low-level 
	- Detalhes de implementação, como por exemplo o contrato de uma API
- Runbooks / Playbooks #low-level 
	- Essenciais em DevOps e SRE. Documentam operação, reinício de serviços e resposta a incidentes.
- Security Design Doc #low-level 
