# AI-103 Domain 1 — Source pack (public Microsoft Learn only)

> All facts paraphrased from public Microsoft Learn documentation. Every URL was retrieved and verified.

---

## o-1-1-1 Choose an appropriate model for each task (LLMs, SLMs, multimodal, model catalog)

- The **Foundry model catalog** contains 1,900+ models from Microsoft, OpenAI, Anthropic, Mistral, xAI, Meta, DeepSeek, Hugging Face, and others — accessible at `https://ai.azure.com/explore/models`.
- Models are organized into two top-level catalog categories: **Foundry Models sold by Azure** (hosted/billed by Azure, covered by Microsoft SLAs, fungible PTU quota) and **Foundry Models from partners and community** (third-party terms, pay-as-you-go serverless or managed compute).
- **LLM selection guidance by task**:
  - `GPT-5`/`gpt-5.6-sol/terra/luna` — highest capability, complex multi-step reasoning, multimodal (text + image), 1M-token context window.
  - `GPT-4.1` / `GPT-4.1-mini` / `GPT-4.1-nano` — production workloads; mini/nano for low-latency high-throughput scenarios.
  - `Claude` (Anthropic) — strong for advanced reasoning, code generation, and multimodal tasks.
  - `DeepSeek-R1` — open-weight reasoning model at scale.
  - `Mistral` families — code generation, multilingual text, general-purpose chat.
  - `o-series` (o4-mini, o3, o1) — Azure reasoning models with extended thinking for complex problem solving.
- **Small Language Models (SLMs)** are suited for edge/on-device and resource-constrained deployments:
  - `Phi-4` (Microsoft) — strong reasoning with efficient deployment; `Phi-4 Mini Instruct` for a smaller footprint.
  - `Meta Llama 1B` and `3B` — for on-device and edge inferencing.
- **Multimodal models** process both text and images in a single call:
  - `Llama 4 Scout` (17B, 16E) and `Llama 4 Maverick` (17B, 128E) use a mixture-of-experts (MoE) architecture for text + image understanding (128K token context).
  - `GPT-4o` — accepts text and image input; multimodal by design.
  - `Whisper` — speech-to-text (audio input); GPT-4o audio models enable speech-in/speech-out interactions.
- **Model Router** (`model-router` deployment) automatically routes each prompt at runtime to the best model (GPT-4.1, GPT-4.1-mini, GPT-4.1-nano, or o4-mini) based on query complexity and cost, exposed as a single deployment via the Chat Completions API.
- **Embedded models** (e.g., `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`) are used to convert text into dense vector representations for similarity search and RAG retrieval.
- **Domain/industry models**: NVIDIA NIMs, Saifr, Rockwell, Bayer (life sciences), Cerence (automotive) — deployed only via managed compute on AI Hub resources.

```python
# Quickstart: call a Foundry model via project client (keyless)
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient(
    endpoint="https://<resource>.ai.azure.com/api/projects/<project>",
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()
response = openai.responses.create(model="gpt-5-mini", input="Explain chain-of-thought reasoning.")
print(response.output_text)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-ai-foundry
- https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/deployments-overview

---

## o-1-1-2 Choose appropriate Foundry services for generative tasks, grounding, vector search, agent workflows, or multimodal processing

- **Microsoft Foundry** is the unified Azure PaaS platform consolidating model inference, agent hosting, evaluation, fine-tuning, and observability under one resource hierarchy (`Microsoft.CognitiveServices/accounts` with kind `AIServices`).
- For **generative text completion / chat**, use the **Azure OpenAI in Foundry Models** endpoints (Chat Completions API or Responses API).
- For **grounding LLM responses in enterprise data** (RAG), the recommended pattern is: Azure AI Search → retrieval → prompt injection → LLM completion. The **Foundry IQ** capability provides a fully managed knowledge layer that turns enterprise content into permission-aware knowledge bases for agents.
- For **vector search**, **Azure AI Search** provides full-text, vector, hybrid, and multimodal retrieval. It natively underpins Foundry IQ and the Agent File Search tool.
- For **agent workflows** (multi-step task automation), use the **Foundry Agent Service** (GA as of May 2025). Agents use the Responses API and expose Conversations/Items/Runs primitives.
- For **multimodal processing** (image + text), use GPT-4o / GPT-4.1 / Llama 4 multimodal models; for audio, use Whisper or GPT-4o audio models.
- **Azure AI Content Safety** (part of Foundry Tools) provides real-time content moderation for text and images — integrated into model deployments as guardrails.
- **Foundry Agent Service tools** for grounding:
  - **File Search** — built-in RAG over Azure Blob Storage, Azure AI Search, and local files.
  - **Grounding with Bing Search** — live web grounding via Bing API.
  - **SharePoint tool** — connects to organizational documents in Microsoft SharePoint.
  - **Fabric Data Agent** — structured data Q&A over Microsoft Fabric.
- For **workflow orchestration** across multiple agents, use Foundry's multi-agent pattern with connected agents (A2A endpoints, preview) or the Responses API multi-tool flow.
- **Foundry Tools** (formerly Azure AI Services) encompasses Speech, Vision, Language, and Content Understanding services, accessible within the same Foundry resource.

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-ai-foundry
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/architecture
- https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search

---

## o-1-1-3 Choose an appropriate method for retrieval and indexing (Azure AI Search, integrated vectorization, embeddings)

- **Azure AI Search** is a fully managed cloud search service with two modes:
  - **Classic search** — index-first, single-index queries, predictable low-latency, supports full-text (BM25), vector, hybrid, and multimodal queries.
  - **Agentic retrieval** — multi-query pipeline backed by a *knowledge base*, uses LLM-assisted query planning, decomposes into sub-queries, runs parallel retrieval across knowledge sources, and returns synthesized answers with references.
- **Pricing models**: Dedicated (fixed capacity, Search Units/hr) or Serverless (consumption-based, CU/hr + per-GB storage; preview, limited regions).
- **Integrated vectorization** automates data chunking + vector embedding during indexing (no separate pipeline code):
  - Requires an **indexer** (pulls from supported data sources), a **skillset** with a chunking skill (Text Split or Azure Content Understanding) plus an embedding skill, and a **vector field** in the index schema.
  - Embedding skills supported: `AzureOpenAIEmbedding` skill (text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large), `AML skill` (Foundry model catalog models), `Azure Vision multimodal embeddings skill`.
  - At **query time**, a configured **vectorizer** automatically converts the text query to a vector — must match the embedding model used during indexing.
- **Hybrid search** = full-text BM25 + vector search combined, optionally re-ranked by **semantic ranking** (cross-encoder re-ranker). Use hybrid for best recall + precision balance.
- **Relevance scoring**: BM25 (`@search.score`) for keyword queries; semantic ranking adds `@search.rerankerScore` with a caption and answer extraction.
- **Knowledge base** (for agentic retrieval): abstracts one or more knowledge sources behind a domain concept; agents reference the knowledge base for *what* to ground on; the knowledge base handles *how*.
- **Supported data sources for indexers**: Azure Blob Storage, Azure Data Lake Storage Gen2, Azure SQL Database, Azure Cosmos DB, SharePoint Online, Microsoft Fabric OneLake, and more.
- **Embeddings workflow for RAG**:
  1. Chunk documents (Text Split skill or custom).
  2. Vectorize chunks (AzureOpenAIEmbedding skill → Azure OpenAI endpoint).
  3. Store in index with both vector and non-vector fields.
  4. At query time, vectorize the user query with a matching vectorizer, run hybrid query + semantic rank.

```json
// Minimal skillset definition (integrated vectorization)
{
  "skills": [
    { "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
      "textSplitMode": "pages", "maximumPageLength": 2000 },
    { "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
      "resourceUri": "https://<aoai>.openai.azure.com",
      "deploymentId": "text-embedding-3-small",
      "modelName": "text-embedding-3-small" }
  ]
}
```

Sources:
- https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search
- https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

---

## o-1-1-4 Choose appropriate memory, tool, and knowledge integration services for agent solutions (Foundry Agent Service, threads, tools, knowledge sources)

- **Foundry Agent Service** (GA May 2025) is the fully managed hosted runtime for building AI agents. It uses the Responses API and manages **Conversations** (threads), **Items** (messages), and **Runs** (execution cycles).
- **Key agent primitives** (new Foundry terminology):
  - **Conversation / Thread** — persists the message history between user and agent; handles automatic truncation to fit model context.
  - **Run** — one execution cycle: the agent reads the thread, calls tools/models, appends messages. Run Steps track each individual tool call or message in the run.
  - **Agent Version** — versioned agent definition with model, instructions, and tools.
- **Memory types**:
  - **Short-term (in-thread)**: conversation context within the current session, maintained automatically in the thread.
  - **Long-term (Memory Store)**: Foundry Agent Service Memory (preview) — a persistent managed memory store. Extracts and consolidates knowledge from conversations across sessions (user preferences, history). Agents query the memory store on new runs to recall prior facts.
  - BYO thread storage: Standard Agent Setup supports Azure Cosmos DB for NoSQL as bring-your-own thread storage, keeping all messages in the customer's own resources.
- **Knowledge tools** (grounding):
  - **File Search** — RAG over Azure AI Search, Azure Blob Storage, local files.
  - **Grounding with Bing Search** — live web data.
  - **Grounding with Bing Custom Search** — scoped to specific websites.
  - **SharePoint** — internal organizational documents.
  - **Fabric Data Agent** — structured data from Microsoft Fabric.
  - **Tripadvisor / Morningstar** — licensed third-party data tools.
- **Action tools** (act on the world): Azure Logic Apps triggers, Code Interpreter, custom function tools, and 1,400+ tools via the tool catalog (public and private).
- Tool resolution order: tools can be attached at agent, thread, or run level. Run-level tools override thread-level, which override agent-level.
- **One instance per knowledge tool type** per agent run (e.g., only one File Search, one Bing Search tool). Use connected agents for multiple indexes.
- **Connected agents** (GA May 2025): task-specific sub-agents that can interact with a primary agent — enables multi-agent systems without an external orchestrator.

```python
# Create an agent with File Search and memory (conceptual)
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project = AIProjectClient(endpoint="...", credential=DefaultAzureCredential())
agent = project.agents.create_version(
    agent_name="my-rag-agent",
    definition={
        "model": "gpt-4.1",
        "instructions": "Answer grounded in retrieved docs.",
        "tools": [{"type": "file_search"}]
    }
)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-ai-foundry
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/architecture

---

## o-1-2-1 Design Azure infrastructure for AI apps and agent-based solutions (Foundry hub/project resources, dependent resources)

- **Foundry resource** (`Microsoft.CognitiveServices/accounts`, kind `AIServices`) is the top-level Azure resource. It contains model deployments, security settings, connections, and one or more **Projects**.
- **Project** (`Microsoft.CognitiveServices/accounts/projects`) is a scoped development boundary inside the Foundry resource. Teams build agents, run evaluations, and store artifacts within a project. Projects reuse the parent Foundry resource's model deployments and connections.
- **Resource hierarchy**: Foundry resource → Projects → Project assets (agents, evaluations, files).
- **Connected resources** are independent Azure services linked to the Foundry resource — they have their own governance boundaries:
  - **Azure Storage** — artifact and file storage.
  - **Azure Key Vault** — secrets for API key-based connections; one Key Vault covers all project and resource-level connection secrets.
  - **Azure AI Search** — vector/hybrid knowledge retrieval.
  - **Azure Application Insights** — observability/tracing telemetry.
- **Hub-based projects** (classic Foundry): AI Hub resource (`Microsoft.MachineLearningServices/workspaces`) with AI projects — still supported in Foundry (classic) portal for serverless API and managed compute deployments; new investments are focused on the new Foundry resource model.
- **Basic vs Standard Agent Setup**:
  - *Basic*: Microsoft-managed multitenant storage (threads, files); fastest to start.
  - *Standard*: Customer brings own Azure Cosmos DB (thread storage), Azure Storage, and Azure AI Search; all data isolated in customer resources.
- **RBAC scope**: Assignments can be made at the Foundry resource level or at the individual project level. Common pattern: assign **Foundry User** role to each developer at resource scope; assign **Foundry User** to the project's managed identity at resource scope.
- **Networking**: Foundry supports Customer-managed VNet (BYO subnet delegated to `Microsoft.App/environments`) or Managed VNet (platform-managed). Private endpoints block all public access — management in this mode requires SDK/CLI (not portal).
- **Encryption**: Default Microsoft-managed keys (FIPS 140-2, AES-256). Optional customer-managed keys (CMK) require Key Vault in same region with soft delete + purge protection enabled, and managed identity with **Key Vault Crypto User** role.

```bicep
// Minimal Foundry resource + project (Bicep AVM pattern)
module aiFoundry 'br/public:avm/ptn/ai-ml/ai-foundry:<version>' = {
  params: {
    baseName: 'my-foundry'
    aiFoundryConfiguration: { createCapabilityHosts: true }
    aiModelDeployments: [
      { model: { name: 'gpt-4.1', version: '2025-04-14', format: 'OpenAI' }
        sku: { name: 'GlobalStandard', capacity: 50 } }
    ]
  }
}
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/architecture
- https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-ai-foundry

---

## o-1-2-2 Choose appropriate deployment options (standard vs global/provisioned, serverless API, managed compute)

- Foundry offers three deployment option families, with **Standard deployment in Foundry resources** as the preferred path:

| Deployment Type | Resource Required | Billing | Data Routing | Best For |
|---|---|---|---|---|
| Global Standard | Foundry resource | Pay-per-token | Cross-region (Azure-managed) | Dev/test, variable traffic |
| Data Zone Standard | Foundry resource | Pay-per-token | US or EU zone only | Zone-level data residency |
| Standard (Regional) | Foundry resource | Pay-per-token | Single region | Strict single-region residency |
| Global Provisioned (PTU) | Foundry resource | Hourly $/PTU/hr | Cross-region | High-scale production, predictable traffic |
| Data Zone Provisioned | Foundry resource | Hourly $/PTU/hr | US or EU zone | Zone residency + guaranteed throughput |
| Regional Provisioned | Foundry resource | Hourly $/PTU/hr | Single region | Strict residency + guaranteed throughput |
| Global Batch | Foundry resource | Discounted batch rate | Cross-region | Async bulk processing, no latency SLA |
| Serverless API | AI Hub (classic) | Pay-per-token² | Regional only | Partner/community models, pay-as-you-go |
| Managed Compute | AI Hub (classic) | Per compute core-hour | Regional only | Custom/Hugging Face/NVIDIA NIM models |

- **Provisioned Throughput Units (PTUs)**: unit of reserved model processing capacity. PTU quota is per-subscription, per-region, per-deployment-type. Having quota does not guarantee capacity — always verify availability before committing.
- PTU capacity can be purchased on **hourly billing** (flexible) or **Azure Reservations** (1-month or 1-year commitment, discounted $/PTU/hr).
- **Spillover** (for provisioned deployments): when a provisioned deployment is fully utilized (429 responses), automatically routes overflow to a standard deployment in the same Foundry resource. Configured per deployment or per-request via `x-ms-spillover-deployment` header.
- **Priority processing**: pay-per-token at a priority tier rate with a defined latency SLA — between standard and provisioned, without a long-term commitment.
- **Serverless API** supports pay-as-you-go for partner models (Llama, Mistral, Cohere, etc.) deployed via AI Hub; no provisioned compute required; only regional deployments.
- **Managed compute**: requires compute quota; billed per minute of uptime; required for Hugging Face, NVIDIA NIMs, industry models, and custom models; only available in AI Hub resources.
- Key capability difference: only Standard/Foundry-resource deployments support custom content filtering and keyless (Entra ID) authentication; serverless API does not support keyless auth.

```azurecli
# Deploy a global provisioned model via Azure CLI
az cognitiveservices account deployment create \
  --resource-group myRG \
  --name myFoundryResource \
  --deployment-name gpt41-prod \
  --model-name gpt-4.1 \
  --model-version "2025-04-14" \
  --model-format OpenAI \
  --sku-name GlobalProvisionedManaged \
  --sku-capacity 100
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/deployments-overview
- https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/provisioned-throughput
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/architecture

---

## o-1-2-3 Configure model and agent deployments

- **Model deployments** are configured in the Foundry portal under **Deployments → Deploy model → Deploy base model** or programmatically via Azure CLI, REST API, or Bicep.
- Key deployment parameters: model name + version, deployment name, SKU/deployment type (GlobalStandard, GlobalProvisionedManaged, etc.), TPM capacity, content filter (guardrail) assignment, auto-update policy.
- **Auto-update to latest**: when enabled, model automatically updates to a new stable version when the currently deployed version is retired. When disabled, you control the version explicitly.
- **Agent deployments** in Foundry Agent Service:
  - Create an agent version with: model deployment name, system instructions, temperature/top_p, tools list, guardrail assignment.
  - Agents can be deployed as **hosted agents** (container-based, persistent HTTP endpoint) or run on-demand via the API.
  - The Foundry VS Code Extension allows deploying and configuring agents directly from the IDE.
- **Guardrail (content filter) assignment**: each model deployment can have one named guardrail assigned; agents can override the model's guardrail with their own. The agent's guardrail fully overrides the model's.
- **Model deployment via SDK** (Python azure-ai-projects):

```python
# List and update a deployment's TPM (via management REST, illustrative)
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

client = CognitiveServicesManagementClient(DefaultAzureCredential(), os.environ["SUBSCRIPTION_ID"])
deployment = client.deployments.get(
    resource_group_name="myRG",
    account_name="myFoundryResource",
    deployment_name="gpt41-prod"
)
# Modify capacity (TPM)
deployment.sku.capacity = 150
client.deployments.begin_create_or_update("myRG", "myFoundryResource", "gpt41-prod", deployment)
```

- **Agent configuration example** (Responses API):

```python
agent = project.agents.create_version(
    agent_name="invoice-agent",
    definition={
        "model": "gpt-4.1",
        "instructions": "Extract invoice fields and validate against policy.",
        "tools": [{"type": "file_search"}, {"type": "function", "function": {"name": "validate_policy"}}],
        "temperature": 0.2
    }
)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/deployments-overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/guardrails/guardrails-overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/architecture

---

## o-1-2-4 Integrate Foundry projects with CI/CD pipelines

- The **Azure Developer CLI (`azd`)** with the **Foundry extensions** (`azd ext install microsoft.foundry`) is the recommended tool for automating Foundry agent deployments.
- `azd pipeline config` auto-detects the Git provider (GitHub or Azure DevOps), creates a service principal, configures repository secrets/variables, and generates a workflow file (`.github/workflows/azure-dev.yml` or Azure Pipelines YAML).
- Standard CI/CD pipeline steps:
  1. `azd provision` — creates/updates Azure infrastructure from Bicep templates in `infra/`.
  2. `azd deploy` — builds the agent container, pushes to Azure Container Registry, creates a new hosted agent version.
- **GitHub Actions** setup uses OpenID Connect (OIDC) with a federated Entra credential (no stored secrets). Required repository variables: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `FOUNDRY_PROJECT_ENDPOINT`, etc.
- **Required RBAC for pipeline identity**:
  - **Foundry User** role on the target Foundry project.
  - **Contributor** role on the Foundry project (for code deployment mode).
  - Additional ACR permissions for container deployment mode.
- Model-only pipelines (not agent containers) can use the Azure REST API or Azure CLI within GitHub Actions / Azure Pipelines YAML steps to create or update model deployments.
- **Azure Machine Learning** pipelines (ML Studio SDK v2) can also automate fine-tuning and evaluation runs within Hub-based Foundry projects.

```yaml
# .github/workflows/azure-dev.yml (generated by azd pipeline config)
name: Deploy Foundry Agent
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install azd
        uses: Azure/setup-azd@v1
      - name: Install Foundry extensions
        run: azd ext install microsoft.foundry
      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - name: Provision infrastructure
        run: azd provision --no-prompt
      - name: Deploy agent
        run: azd deploy --no-prompt
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/architecture
- https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-ai-foundry

---

## o-1-3-1 Manage quotas, scaling, rate limits (TPM/PTU), and cost footprints

- **TPM (Tokens per Minute)** is the primary unit of quota for Azure OpenAI in Foundry Models. Quota is assigned per subscription, per region, per model, per deployment type (Global, Data Zone, Regional each have separate pools).
- When you create a deployment, you assign TPM to it; this directly sets the **TPM rate limit** and a proportional **RPM (Requests per Minute)** limit. Example ratio for o4-mini: 1 RPM per 1,000 TPM; older chat models: 6 RPM per 1,000 TPM.
- Total quota across all deployments of the same model in a region cannot exceed the subscription's regional quota for that model.
- **PTUs** are the unit for provisioned throughput. PTU quota is a policy limit (no cost); **capacity** is the actual compute that must be available at deployment time. Having PTU quota does NOT guarantee available capacity.
- Three provisioned deployment types with separate quota pools: **Global Provisioned** (`GlobalProvisionedManaged`), **Data Zone Provisioned** (`DataZoneProvisionedManaged`), **Regional Provisioned** (`ProvisionedManaged`).
- **PTU sizing**: determined by target RPM × average prompt tokens + average completion tokens, adjusted for output-to-input ratio and prompt cache rate. Use the Foundry portal capacity calculator at `https://ai.azure.com/resource/calculator`.
- **Requesting quota increases**: submit the form at `https://aka.ms/oai/stuquotarequest` (also accessible from Foundry portal → Quota page). Quota increases for partner/community models are not supported.
- **Viewing quota**: Foundry portal → **Management → Quota**; shows deployment-level allocation and subscription-level limit. The **Cognitive Services Usages Reader** role provides minimum permissions to view quota across subscriptions (must be assigned at subscription scope).
- **Cost management**: PTU deployments bill hourly regardless of token consumption; track via Microsoft Cost Management. **Azure Reservations** (1-month or 1-year) discount the hourly PTU meter.
- **Spillover** prevents hard failures when a provisioned deployment is saturated — overflow routes to a linked standard deployment.
- **`model-router`** deployment reduces costs by automatically routing simple queries to cheaper models (nano/mini) and complex queries to full models.
- Maximum resources per region: 30 Azure OpenAI resources; no limit on deployments of the same model per resource (removed with the new quota system).

```azurecli
# View current quota usage for a region
az cognitiveservices usage list \
  --location eastus \
  --query "[?name.value contains 'gpt-4']" \
  --output table
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/quota
- https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/provisioned-throughput
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/architecture

---

## o-1-3-2 Monitor model performance, drift, safety events, and grounding quality

- **Agent Monitoring Dashboard** in the Foundry portal (Monitor tab per agent) shows: token usage, latency, run success rate, evaluation metric scores, and red-teaming results — backed by Azure Monitor Application Insights.
- **Key metrics**:
  - **Token usage** — high values may indicate verbose prompts; optimize prompt engineering.
  - **Latency** — >10 s may indicate model throttling, complex tool chains, or network issues.
  - **Run success rate** — below 95% warrants investigation into failed runs.
  - **Evaluation scores** — vary by evaluator; scores reflect sampled production traffic via continuous evaluation rules.
- **Continuous evaluation**: a rule that automatically triggers a configured evaluator on each agent response (or on a sample). Configure via Foundry portal Monitor → Settings, or programmatically using the `azure-ai-projects` SDK. The rule specifies: eval object ID, max hourly runs (default 100), event type (`RESPONSE_COMPLETED`), and agent name filter.
- **Scheduled evaluations** (preview): run evaluation templates on a schedule to compare performance against baselines over time.
- **Red team scans** (preview): scheduled adversarial tests to detect risks like data leakage, prohibited actions, or jailbreak vulnerabilities.
- **Drift detection**: model monitoring ensures outputs align with Responsible AI principles over time. Drift occurs due to changing user behaviors or data distribution shifts; continuous evaluation metrics surface this.
- **Grounding quality** is measured by the **Groundedness** evaluator (1–5 model-based score) or **Groundedness Pro** (binary pass/fail via Azure AI Content Safety; no model deployment required). The **Relevance** evaluator measures whether retrieved context is pertinent to the query.
- Alerts (preview) can be configured for latency, token usage, evaluation score thresholds, and red team findings.
- Requires: Foundry project connected to Azure Application Insights; **Log Analytics Reader** role for log-based views; **Privileged Monitoring Data Reader** if log tables are protected.
- For custom/external agents: instrument with OpenTelemetry using Foundry semantic conventions, send to the same Application Insights instance, then register the agent in Foundry Control Plane.

```python
# Create continuous evaluation rule (Python SDK)
from azure.ai.projects.models import (EvaluationRule, ContinuousEvaluationRuleAction,
                                       EvaluationRuleFilter, EvaluationRuleEventType)

eval_object = openai_client.evals.create(
    name="Prod Groundedness Eval",
    data_source_config={"type": "azure_ai_source", "scenario": "responses"},
    testing_criteria=[{"type": "azure_ai_evaluator", "name": "groundedness",
                        "evaluator_name": "builtin.groundedness"}],
)
project_client.evaluation_rules.create_or_update(
    id="groundedness-prod-rule",
    evaluation_rule=EvaluationRule(
        display_name="Groundedness Rule",
        action=ContinuousEvaluationRuleAction(eval_id=eval_object.id, max_hourly_runs=100),
        event_type=EvaluationRuleEventType.RESPONSE_COMPLETED,
        filter=EvaluationRuleFilter(agent_name="my-rag-agent"),
        enabled=True,
    ),
)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/how-to-monitor-agents-dashboard
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/built-in-evaluators
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/concepts/trace-agent-concept

---

## o-1-3-3 Monitor data ingestion quality, search index health, and relevance performance

- **Azure AI Search monitoring** is available through Azure Monitor integration: enable diagnostic settings on the search service to route logs to Log Analytics workspace, Storage, or Event Hubs.
- **Key search service metrics** (via Azure Monitor): query latency, queries per second (QPS), throttled queries %, document count, storage size, indexer run success/failure.
- **Indexer run monitoring**: each indexer run reports success, partial success, or failure. Failure details include item-level errors and warnings. Check via the Azure portal (Search service → Indexers → run history) or via REST API (`GET /indexers/{name}/status`).
- **Relevance signals and tuning**:
  - **BM25 score** (`@search.score`): lexical relevance — statistical overlap of query terms and document tokens.
  - **Semantic ranking score** (`@search.rerankerScore`): cross-encoder re-ranker model that scores documents for intent-level relevance (0–4 scale); top 50 BM25 candidates are re-ranked.
  - **Vector search score**: cosine similarity (or dot product / Euclidean, configurable) between query embedding and document embedding.
- **Hybrid search** combines BM25 + vector scores via Reciprocal Rank Fusion (RRF) — provides better recall than either alone.
- **Relevance performance tuning**: use boosting profiles, scoring profiles, and synonyms; test with the Search Explorer in Azure portal; use the Semantic Configuration to specify title, content, and keyword fields.
- **Index health checks**: verify document count matches expected source count; check for indexer throttling (common when Azure OpenAI embedding quota is exhausted during integrated vectorization); retry policies are built in to the indexer.
- **Foundry Agent Service metrics** (Azure Monitor): number of files indexed for File Search tool, number of agent runs per time period — available since April 2025 via the metrics reference.
- **Agentic retrieval quality**: query the knowledge base knowledge source and inspect the `activity` log returned with results — it shows sub-queries generated, sources retrieved, and re-ranking steps.

```azurecli
# Check indexer run status
az search indexer show --service-name mySearchSvc --resource-group myRG --name my-indexer
az search indexer get-status --service-name mySearchSvc --resource-group myRG --name my-indexer
```

Sources:
- https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search
- https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/how-to-monitor-agents-dashboard

---

## o-1-3-4 Configure security: managed identity, private networking/private endpoints, keyless credentials (Entra ID), RBAC role policies

- **Keyless authentication (Entra ID)**: preferred over API keys. Use `DefaultAzureCredential` (from `azure-identity`) to automatically select the credential (managed identity in production, developer credential locally). Only **Standard/Foundry-resource deployments** support keyless auth; serverless API endpoints do not.
- **Managed identity**: assign a system-assigned or user-assigned managed identity to the Foundry resource or project. Grant this identity required roles on connected resources (e.g., **Storage Blob Data Contributor** on Azure Storage, **Search Index Data Contributor** on Azure AI Search, **Key Vault Crypto User** for CMK).
- **Foundry RBAC roles** (recently renamed from Azure AI roles):

  | Role | Scope | Permissions |
  |---|---|---|
  | **Foundry Account Owner** | Resource | Full management + data plane access |
  | **Foundry Owner** | Resource or Project | Management + data plane |
  | **Foundry User** | Resource or Project | Data plane: build agents, run evals, upload files |
  | **Foundry Project Manager** | Project | Create/manage projects |
  | **Cognitive Services Usages Reader** | Subscription | Read quota usage across subscription |

- Control plane actions (create deployments, projects) are distinct from data plane actions (build agents, evaluate, upload files) — enables least-privilege scoping.
- **Private networking**:
  - Create a **private endpoint** for the Foundry resource or Azure AI Search service to block all public internet traffic.
  - Two VNet models for agents: **Customer-managed VNet** (BYO subnet delegated to `Microsoft.App/environments`) or **Managed VNet** (platform-managed, simpler setup).
  - When fully private, portal cannot manage certain settings — use Azure CLI or SDK.
  - Use **shared private link** connections from Azure AI Search to reach vectorizers/embedding models privately within Azure.
- **Azure Policy**: use built-in and custom Azure Policy definitions to enforce governance (e.g., require private endpoints, require CMK encryption, restrict allowed model deployments) via `Microsoft.CognitiveServices` resource provider.
- **Microsoft Purview** integration: apply DLP policies and sensitivity labels to data accessed by agents via Foundry.
- **Network security best practices**: create Foundry hubs with managed VNet isolation; block public access for production; use private DNS zones for private endpoint name resolution.

```python
# Keyless authentication pattern (production code)
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

credential = DefaultAzureCredential()  # uses managed identity in Azure, dev credential locally
project = AIProjectClient(
    endpoint="https://<resource>.ai.azure.com/api/projects/<project>",
    credential=credential,
)
```

```azurecli
# Assign Foundry User role to a managed identity
az role assignment create \
  --role "Foundry User" \
  --assignee-object-id <managed-identity-object-id> \
  --assignee-principal-type ServicePrincipal \
  --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<resource>
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/architecture
- https://learn.microsoft.com/en-us/azure/ai-foundry/guardrails/guardrails-overview

---

## o-1-4-1 Configure safety filters, guardrails, risk detection, content moderation (Azure AI Content Safety, content filters)

- **Guardrails** in Foundry are named collections of **controls** that define: (1) the risk to detect, (2) the intervention point to scan, (3) the action to take.
- **Four intervention points**:
  - **User input** — the prompt sent to the model or agent (both models and agents).
  - **Tool call** (Preview) — the action/data the agent proposes to send to a tool (agents only).
  - **Tool response** (Preview) — content returned from a tool to the agent (agents only).
  - **Output** — the final completion returned to the user (both models and agents).
- **Risk categories** and applicable targets:
  - Hate, Sexual, Self-harm, Violence — apply to both models and agents.
  - User prompt attacks (jailbreak) — both.
  - Indirect attacks (XPIA) — both.
  - Protected material for text/code — both.
  - Groundedness (Preview), Spotlighting (Preview) — models only.
  - PII (Preview), Task Adherence (Preview), Prohibited Actions — agents.
  - Sensitive Data Leakage — agents.
- **Severity levels** for content risks: **Off** (approved customers only), **Low** (flags at low+), **Medium**, **High** (most restrictive, flags only severe content).
- **Actions when risk detected**: **Annotate** (log only, models only) or **Annotate and block** (returns error to caller).
- **Default guardrail**: all models are assigned `Microsoft.DefaultV2` by default. Agents inherit the model's guardrail unless a custom guardrail is explicitly assigned to the agent.
- **Guardrail override for agents**: the agent's guardrail fully overrides the model's guardrail — tool call and tool response risks are governed by the agent's guardrail, not the model's.
- **Modifying guardrails**: requires **Foundry Account Owner** role. To turn off content filters entirely, submit the **Limited Access Review** form; for Azure Government, a separate form exists.
- **Azure AI Content Safety service** (a Foundry Tool): standalone service for analyzing text and images for harmful content — used by Groundedness Pro evaluator and by the guardrail classification models. Supports hate, sexual, violence, self-harm detection with severity levels 0–7.
- **Applies to**: all Foundry Models sold by Azure except audio models (Whisper). Applies to agents in Foundry Agent Service only (not to externally registered agents).

```python
# Configure a custom guardrail (conceptual, via REST)
import requests, json
from azure.identity import DefaultAzureCredential

token = DefaultAzureCredential().get_token("https://management.azure.com/.default").token
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

guardrail_body = {
    "name": "strict-safety",
    "controls": [
        {"risk": "Hate", "interventionPoint": "UserInput", "severity": "Low", "action": "AnnotateAndBlock"},
        {"risk": "Violence", "interventionPoint": "Output", "severity": "Medium", "action": "AnnotateAndBlock"},
        {"risk": "IndirectAttacks", "interventionPoint": "UserInput", "severity": "Low", "action": "AnnotateAndBlock"},
    ]
}
# POST to Foundry guardrails API (project scope)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/guardrails/guardrails-overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/built-in-evaluators

---

## o-1-4-2 Responsible AI instrumentation: evaluators, safety evaluations, explanation tooling (Foundry evaluations)

- **Foundry built-in evaluators** are organized into categories: General Purpose, Textual Similarity, RAG, Risk & Safety, Agent, Rubric, and Azure OpenAI Graders.
- **General purpose**: `Coherence` (logical flow), `Fluency` (natural language quality).
- **Textual similarity**: `F1 Score`, `BLEU`, `GLEU`, `ROUGE`, `METEOR` — all measure n-gram overlaps between response and ground truth; useful for translation/summarization.
- **RAG evaluators**:
  - `Groundedness` — 1–5 model-based score: is the response grounded in retrieved context?
  - `Groundedness Pro` (preview) — binary pass/fail using Azure AI Content Safety (no model deployment needed).
  - `Relevance` — is the response relevant to the query?
  - `Retrieval` — how effectively does the system retrieve relevant information?
  - `Response Completeness` (preview) — does the response cover all critical information from ground truth?
- **Risk and safety evaluators** (used in safety evaluations and red-teaming):
  - `Hate and Unfairness`, `Sexual`, `Violence`, `Self-Harm`, `Protected Materials`.
  - `Indirect Attack (XPIA)` — did the response fall for an indirect jailbreak via retrieved context?
  - `Code Vulnerability`, `Ungrounded Attributes`, `Prohibited Actions`, `Sensitive Data Leakage`.
- **Agent evaluators**:
  - `Task Adherence` — did the agent follow system instruction tasks?
  - `Task Completion` — did the agent successfully complete the end-to-end task?
  - `Tool Call Accuracy` — selection + parameter correctness + efficiency.
  - `Tool Selection`, `Tool Input Accuracy`, `Tool Output Utilization`, `Tool Call Success`.
  - `Intent Resolution` — how accurately did the agent identify user intent?
  - `Customer Satisfaction` (preview) — 6-dimension score: helpfulness, completeness, clarity, tone, resolution, adaptability.
  - `Quality Grader` (preview) — bundles relevance, abstention, completeness, groundedness, context coverage in one evaluator.
- **Evaluation levels**: `turn` (individual response, default) or `conversation` (entire multi-turn interaction). All evaluators in a run must use the same level.
- **RAG recommended combination**: Retrieval + Groundedness + Relevance + Content Safety evaluators.
- **Agent recommended combination**: Tool Call Accuracy + Task Adherence + Intent Resolution + Rubric + Content Safety.
- **Custom evaluators** (preview): define your own scoring logic, validation rules, and quality metrics for business-specific criteria.
- **Rubric evaluator** (preview): scores against custom weighted criteria using an LLM as judge; returns a weighted average 0–1 with per-dimension reasoning.
- **Safety evaluations** can be run on fine-tuned models pre-deployment to detect harmful content risks introduced during fine-tuning.
- The **Discover → Protect → Govern** framework (Microsoft RAI Standard) structures responsible AI: discover risks (red-team, evaluate), protect (guardrails, content filters), govern (tracing, continuous monitoring, compliance).

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/built-in-evaluators
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/how-to-monitor-agents-dashboard
- https://learn.microsoft.com/en-us/azure/ai-foundry/guardrails/guardrails-overview

---

## o-1-4-3 Auditing: trace logging, provenance metadata, approval workflows

- **Foundry Tracing** is built on **OpenTelemetry (OTel)** — traces are stored in **Azure Monitor Application Insights** connected to the Foundry project.
- **Trace structure**:
  - **Traces** — capture the full journey of a request: inputs, outputs, tool calls, retries, latency, token costs.
  - **Spans** — individual operations within a trace; can be nested (parent/child) to show hierarchical call stacks.
  - **Attributes** — key-value pairs on spans: function parameters, return values, custom annotations.
  - **Semantic conventions** — Foundry follows OTel semantic conventions for generative AI (`gen-ai.*` namespaces), standardized with Cisco Outshift collaboration for multi-agent systems.
- **What tracing captures per agent run**: user inputs, agent outputs, tool invocations + results, token consumption, durations and latency, model call spans (llm_spans).
- **Multi-agent tracing spans**: `execute_task` (task planning), `agent_to_agent_interaction` (A2A calls), `agent_planning`, `agent_state.management`, tool `call.arguments` / `call.results`, Evaluation events with name, error.type, label.
- **Setup**: connect Azure Application Insights to the Foundry project → enable tracing → assign **Log Analytics Reader** role (+ **Privileged Monitoring Data Reader** if tables are protected).
- **Data retention**: follows Application Insights configuration — review retention settings to meet compliance requirements.
- **Approval workflows**: Foundry's "Ask AI" feature uses an **approval flow** for actions that modify Azure resources — the agent proposes the action, the user reviews and approves before execution. Pre-approval scopes (System access vs. none) can be configured per session.
- **Provenance**: trace data links responses to the exact tool calls, retrieved documents, and model calls that produced them — enabling lineage tracking for each output.
- **Security for trace data**: redact PII, credentials, and sensitive content from prompts/tool arguments before they reach telemetry. Apply same access controls to trace data as production logs. Don't store secrets in span attributes.
- **Integrations**: Foundry tracing integrates with LangChain, LangGraph, OpenAI Agents SDK, and Microsoft Agent Framework via the standardized OTel multi-agent semantic conventions.
- **W3C Trace Context** (`traceparent` header) propagates trace correlation across distributed agent calls.

```python
# Enable tracing via azure-ai-projects SDK
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.telemetry import enable_telemetry

project = AIProjectClient(endpoint="...", credential=DefaultAzureCredential())
# Connect Application Insights (set env var APPLICATIONINSIGHTS_CONNECTION_STRING)
enable_telemetry(project, connection_string=os.environ["APPINSIGHTS_CONNECTION_STRING"])
# All subsequent agent runs are traced automatically
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/concepts/trace-agent-concept
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/how-to-monitor-agents-dashboard

---

## o-1-4-4 Govern agent behavior: oversight modes, constraints, tool-access controls

- **Microsoft RAI framework for agents** follows three stages: **Discover** (red-team before deployment, test adversarially), **Protect** (guardrails, content filters, tool-access restrictions), **Govern** (trace logging, continuous monitoring, compliance integrations).
- **Tool-access controls (least-privilege)**:
  - Grant agents access only to the specific data sources required for their function — not broad organizational data access.
  - When an agent accesses data on behalf of a user, it should inherit that user's permissions (pass the user's identity/token to downstream systems).
  - Use **Microsoft Entra Agent ID** to create a separate managed identity for each agent — enables RBAC-scoped tool access and audit trail per agent identity.
  - Apply **Microsoft Purview DLP policies** and sensitivity labels to data sources accessed by agents.
- **Oversight and human approval**:
  - For high-risk actions, build in human-in-the-loop approval steps — either via Azure Logic Apps triggers, custom function tools that pause execution, or the Foundry "Ask AI" approval flow (proposes action, user reviews, then executes).
  - **Transparency requirement**: disclose AI involvement clearly in agent interfaces; notify users when agent is acting on their behalf.
- **Azure Policy for infrastructure governance**:
  - Use `Microsoft.CognitiveServices` Azure Policy aliases to enforce network isolation (require private endpoints), CMK encryption, or allowlisted model deployments.
  - Create custom policy definitions to block specific model deployment SKUs or regions.
- **Fairness and accountability**:
  - Assign clear human ownership for AI outcomes and Responsible AI compliance.
  - Use Foundry evaluations (bias evaluators, fairness checks) during development and periodically in production.
  - Designate a human role accountable for approving deployments and monitoring ongoing compliance.
- **Constraint mechanisms**:
  - **System prompt / instructions**: constrain agent behavior, persona, scope, and output format via the agent's `instructions` field.
  - **Guardrail assignment**: apply guardrails to agents that specifically include tool call and tool response intervention points (preview) — scan what the agent proposes to do AND what tools return.
  - **Tool catalog access**: configure which tools are available to each agent; don't expose broad tool catalogs unless required.
  - **Connected agents scope**: use connected sub-agents with narrowly scoped tool sets for specific subtasks — reduces blast radius of any single agent.
- **Agentic guardrail override**: agent's guardrail overrides model's guardrail — explicitly configure `Tool call` and `Tool response` intervention points in the agent guardrail to scan agentic behavior.
- **Audit trail**: all agent runs generate trace data in Application Insights; combined with continuous evaluation rules, this provides a complete record of agent behavior, tool use, and safety events.

```python
# System prompt constraining agent scope
agent = project.agents.create_version(
    agent_name="hr-policy-agent",
    definition={
        "model": "gpt-4.1",
        "instructions": (
            "You are an HR policy assistant. "
            "Only answer questions about company HR policies. "
            "Never take actions on HR systems; only retrieve and explain policies. "
            "If asked to perform any action, respond that you are not authorized to do so."
        ),
        "tools": [{"type": "file_search"}],  # read-only knowledge tool only
    }
)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/guardrails/guardrails-overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/concepts/trace-agent-concept
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/architecture
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/built-in-evaluators
