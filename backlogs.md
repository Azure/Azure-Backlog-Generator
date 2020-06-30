# Backlogs
AzBacklog currently supports creating backlogs for the following processes.

| Backlog      | Command-line Option (see below: `-b`)        |
|--------------|---------------|
| [Cloud Adoption Framework (CAF)](#cloud-adoption-framework-caf)        | `caf`      |
| [Enterprise-scale Architecture](#enterprise-scale-architecture)     | `esa`     |
| _(Coming Soon)_ [Team Foundation Server (TFS) to Azure DevOps](#team-foundation-server-tfs-to-azure-devops)   | `tfs`        |

## Backlog Descriptions

### Cloud Adoption Framework (CAF)
The [Microsoft Cloud Adoption Framework for Azure](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/) is the One Microsoft approach to cloud adoption in Azure, consolidating and shaping proven practices from Microsoft employees, partners, and customers.

Proper implementation of CAF, in order to establish a foundational landing zone, requires solid architecture and migration experience along with rigorous amounts of effort by Microsoft and the customer. Migration of on-premises workloads to the cloud is no small feat and includes many steps. Therefore, in order to assist cloud architects with migrating customers, those necessary steps have been compiled into a list of backlog items. This backlog will enable the cloud architect to manage an adoption and migration path in alignment to CAF to "land" the customer workloads in Azure.
<!--
**Roles & Tags**  
```json
{
    ...
    "tag": ["Strategy | Plan | Ready | Innovation | Migration | First Workload | First Host | Workload Template"],
    "roles": ["Infra | AppDev | Data | Security"]
}
```
-->
### Enterprise-scale Architecture
Enterprise-scale is an architecture approach and reference implementation that enables effective construction and operationalization of landing zones on Azure, at scale and aligned with the Azure roadmap and the Microsoft Cloud Adoption Framework for Azure.

The CAF [enterprise-scale landing zone architecture](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/architecture) represents the strategic design path and target technical state for the customer's Azure environment. It will continue to evolve in lockstep with the Azure platform and is ultimately defined by the various design decisions the customer organization must make to define their Azure journey.

### Team Foundation Server (TFS) to Azure DevOps
Teams seeking to move source code repositories from an on-premsises TFS or Azure DevOps Server to Azure DevOps Services (cloud) can utilize the [Migration Guide and Data Migration Tool](https://www.microsoft.com/en-us/download/details.aspx?id=54274). The generated backlog is based on the steps identified in the migration guide.