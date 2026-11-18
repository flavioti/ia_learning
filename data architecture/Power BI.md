---
description: Power BI, Microsoft's business intelligence tool for building data models, DAX measures, dashboards and reports on top of a data warehouse or lakehouse, including refresh, gateways, row-level security and the PL-300 certification. Context is the consumption layer of a data architecture.
aliases:
  - Microsoft Power BI
  - PowerBI
tags:
  - bi
  - data-visualization
  - microsoft
---
# Power BI

**Power BI** is Microsoft's BI platform. It connects to data sources, models the data, computes measures and publishes reports to business users. In a [[Data Architecture]], it sits in the **consumption layer**, after the warehouse or lakehouse.

## Components

| Component | Role |
|---|---|
| **Power BI Desktop** | Authoring: connect, transform, model, write measures, build reports |
| **Power BI Service** | Cloud service: publish, share, schedule refresh, manage workspaces and apps |
| **Gateway** | Bridge that lets the service refresh data from on-premises sources |
| **Workspaces and apps** | Where reports and datasets are published and grouped for audiences, with permissions |

## Building a model

1. **Get data:** connect to ERP, CRM, SQL databases, files or a lakehouse.
2. **Transform with Power Query (M):** clean, reshape and combine the source tables. Every step is recorded and re-run on refresh.
3. **Model:** build a **star schema** (fact tables and dimension tables) with clear relationships. This gives "one version of the truth" for KPIs. See [[dimensional modeling]].
4. **Measures with DAX:** calculated logic such as totals, ratios and time intelligence. Measures are evaluated at query time, in the context of the filters the user applies.
5. **Visualize:** reports and dashboards with slicers, drill-through and bookmarks.

## Connection modes

| Mode | What it does | Trade-off |
|---|---|---|
| **Import** | Copies the data into the model | Fast queries, data is only as fresh as the last refresh |
| **DirectQuery** | Sends queries to the source at view time | Fresh data, slower and limited by the source |
| **Live connection** | Uses a model published elsewhere (for example Analysis Services) | Single model reused across reports |

## DAX

DAX is the formula language for measures, calculated columns and RLS. Its core ideas (filter context, row context, `CALCULATE`, time intelligence) are in the child note:

- [[data architecture/Power BI/DAX|DAX]]

## Security

- **Row-level security (RLS):** roles with DAX filters restrict the rows each user sees. Static roles use fixed values. Dynamic roles use the signed-in user, for example with `USERPRINCIPALNAME()`.
- **Workspace and app permissions** control who can edit or only view.
- RLS in Power BI is separate from row-level security in a data lake (for example AWS Lake Formation, which filters the data at the storage layer).

## Operations

- **Refresh schedules** keep imported data current. Monitor failures and duration in the service.
- **Gateway performance** matters for on-premises sources: a single gateway can become the bottleneck.
- **Version control and naming conventions** keep datasets and reports maintainable across a team.

## Certification

The **Microsoft Certified: Power BI Data Analyst Associate** certification is exam **PL-300**. It covers preparing, modeling, visualizing and managing data in Power BI. Check the current exam guide on Microsoft Learn, because the content changes with product updates.

## Related

- [[dimensional modeling]]
- [[Data Warehouse/Data Warehouse|Data Warehouse]]
- [[Data Lakehouse/Data Lakehouse|Data Lakehouse]]
- [[data quality]]
