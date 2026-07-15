# AI-103 Domain 2 — Source pack (public Microsoft Learn only)

> **Domain 2: Implement generative AI and agentic solutions** (30–35% of exam)
> Every source URL below was fetched from learn.microsoft.com during authoring.

---

## o-2-1-1 Deploy and consume LLMs, small models, code models, and multimodal models

- Azure AI Foundry provides a unified **model catalog** covering LLMs, small language models (SLMs), code-generation models (e.g., Codex family), and multimodal models (e.g., GPT-4o with vision and audio).
- Two deployment types exist: **Serverless API** (pay-per-token, no compute to manage) and **Managed Compute** (dedicated container-based endpoint, required for custom fine-tuned models or regulatory isolation).
- After deployment, four SDKs are officially supported for inference: **OpenAI SDK**, **Azure OpenAI SDK**, **Azure AI Inference package** (`azure-ai-inference`), and **Azure AI Projects package** (`azure-ai-projects`).
- The **Azure AI Inference package** (`azure-ai-inference`) is the recommended cross-model abstraction—it targets the Azure AI Model Inference REST API and lets you swap the underlying model without changing application code.
- The project endpoint pattern for inference is `https://<resource-name>.services.ai.azure.com/models`; the OpenAI-compatible endpoint is `https://<resource-name>.openai.azure.com/openai/v1`.
- **Autoscaling** for managed compute deployments is configured through Azure Machine Learning online endpoint scaling rules in the Azure portal.
- Multimodal content (images, audio) is passed via the `content` array in the messages list using `image_url` or `input_audio` typed blocks, supported by models like GPT-4o.
- The portal **Test** tab and **Consume** tab on a model deployment provide ready-to-use code samples and the Target URI for the endpoint.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],  # e.g. https://<resource>.services.ai.azure.com/models
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_KEY"]),
)

response = client.complete(
    model="gpt-4o",          # model name from catalog
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="Explain transformer attention in two sentences."),
    ],
    temperature=0.3,
    max_tokens=256,
)
print(response.choices[0].message.content)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview
- https://learn.microsoft.com/en-us/azure/foundry-classic/foundry-models/supported-languages
- https://learn.microsoft.com/en-us/azure/ai-foundry/model-inference/reference/reference-model-inference-chat-completions
- https://learn.microsoft.com/en-us/azure/foundry-classic/how-to/deploy-models-managed
- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/model-router

---

## o-2-1-2 Implement retrieval-augmented generation (RAG) in an application

- RAG follows a three-step pipeline: **Retrieve** (query an index), **Augment** (combine retrieved chunks with the user query into a grounding prompt), then **Generate** (send the augmented prompt to the LLM).
- Azure AI Foundry integrates with **Azure AI Search** as the primary indexing and retrieval back-end; the index must include searchable text fields and optionally vector (`Collection(Edm.Single)`) fields for semantic similarity.
- Two RAG approaches are available in Azure AI Search: **Agentic retrieval** (preview—LLM-assisted query planning, multi-source, structured response with citations) and **Classic RAG** (hybrid search + semantic ranking, GA-stable, fine-grained control).
- Content preparation matters: Azure AI Search supports automatic **chunking**, 50+ language analyzers, OCR for PDFs and images, and integrated vectorization through Azure OpenAI or Azure Vision.
- **Foundry IQ** is the managed knowledge layer in the Foundry portal that turns enterprise content into permission-aware, reusable knowledge bases for agents, built on Azure AI Search under the hood.
- To implement RAG in code: (1) prepare and chunk data, (2) create and populate an Azure AI Search index, (3) create a project connection from the Foundry project to the search service, (4) retrieve with the search SDK, and (5) pass retrieved context into the LLM prompt.
- Use **hybrid search** (vector + keyword) for the best out-of-box relevance; add **semantic ranking** for query-intent reranking.
- Groundedness of RAG responses can be measured with the built-in **Groundedness** evaluator in the Foundry evaluation service.

```python
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage, SystemMessage
import os

search_client = SearchClient(
    endpoint=os.environ["SEARCH_ENDPOINT"],
    index_name="my-index",
    credential=AzureKeyCredential(os.environ["SEARCH_KEY"]),
)

def rag_answer(question: str) -> str:
    # Retrieve top-3 chunks
    results = search_client.search(search_text=question, top=3)
    context = "\n".join(r["content"] for r in results)

    # Augment + Generate
    chat_client = ChatCompletionsClient(
        endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
        credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_KEY"]),
    )
    resp = chat_client.complete(
        model="gpt-4o",
        messages=[
            SystemMessage(content=f"Answer only from the context below.\n\n{context}"),
            UserMessage(content=question),
        ],
    )
    return resp.choices[0].message.content
```

Sources:
- https://learn.microsoft.com/en-us/azure/foundry/concepts/retrieval-augmented-generation
- https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
- https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-overview
- https://learn.microsoft.com/en-us/training/modules/develop-rag-solution-azure-ai-foundry/
- https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq

---

## o-2-1-3 Design workflows, tool-augmented flows, and multistep reasoning pipelines

- **Prompt flow** was the original Foundry workflow tool; it is now **deprecated** (retirement April 20, 2027) and new development should migrate to the **Microsoft Agent Framework** and the Responses API.
- Tool-augmented flows combine an LLM reasoning step with external tool calls (search, code execution, API calls) in a loop; the model emits a tool-call request, application code executes the tool, and the output is returned to the model to continue reasoning.
- The **Responses API** is the single entry point for Foundry agents and tool orchestration; it supports streaming, multi-turn conversations, and structured tool-call lifecycle management.
- Multistep reasoning pipelines can be built with the **Agent Framework** (hosted code-based agents), **LangGraph**, the **OpenAI Agents SDK**, or the **Semantic Kernel** library—all can call the Responses API on the Foundry project endpoint.
- The **Foundry Toolbox** feature lets teams define a curated set of tools once, version them, and expose them through a single MCP-compatible endpoint consumable by any framework.
- For sequential reasoning, prefer a **single agent** with multiple tool definitions. For parallel or specialized subtask execution, prefer **connected/multi-agent** patterns (see o-2-2-4).
- Built-in platform tools available via the Responses API include: **file search**, **code interpreter**, **web search**, **memory**, **SharePoint**, **WorkIQ**, **Fabric IQ**, and **remote MCP servers**.

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_KEY"],
    api_version="2025-01-01-preview",
)

tools = [{
    "type": "function",
    "function": {
        "name": "get_inventory",
        "description": "Return current stock count for a product SKU.",
        "parameters": {
            "type": "object",
            "properties": {"sku": {"type": "string"}},
            "required": ["sku"],
        },
    },
}]

messages = [{"role": "user", "content": "Is SKU-42 in stock?"}]
response = client.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)
# If finish_reason == "tool_calls", execute the function and loop
```

Sources:
- https://learn.microsoft.com/en-us/azure/foundry-classic/how-to/prompt-flow/develop-prompt-flow
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstarts/responses-api
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/toolbox
- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview

---

## o-2-1-4 Evaluate models and apps: detect fabrications/groundedness, relevance, quality, safety

- The Foundry **Evaluation service** runs model or agent outputs against built-in or custom evaluators; evaluations can be triggered from the portal, SDK, or scheduled runs.
- **Evaluation targets**: Agent (full conversation or individual turn), Model (individual turn), Dataset (pre-computed outputs), or Traces (historical Application Insights traces).
- **Quality evaluators** (AI-assisted, require a judge model such as `gpt-4.1-mini`): Groundedness, Relevance, Coherence, Fluency, Response Completeness, Customer Satisfaction, Task Completion.
- **Groundedness** specifically measures whether a response is supported by the provided context—the primary metric for detecting fabrications in RAG applications.
- **Safety evaluators** (individual turns only): Violence, Sexual, Self-harm, Hate/Unfairness—used to ensure generated content meets content policy requirements before production deployment.
- **Agent evaluators** assess tool usage effectiveness: Intent Resolution, Task Adherence, Tool Call Success, Tool Selection Accuracy, Tool Output Utilization, Tool Input Accuracy.
- For conversation-level evaluation, use **simulated data** (generate synthetic multi-turn conversations from scenario descriptions) or **existing conversations** from production traffic.
- Programmatic evaluation uses the `azure-ai-projects` SDK; poll for run completion, then retrieve the `report_url` to view results in the Foundry portal under the **Evaluations** tab.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Run evaluation with groundedness and relevance evaluators
eval_run = project_client.evals.runs.create(
    evaluation_id="<eval-id>",
    data_source={"type": "dataset", "dataset_id": "<dataset-id>"},
    evaluators=["groundedness", "relevance", "coherence"],
)
print(f"Evaluation run ID: {eval_run.id}")
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/evaluate-generative-ai-app
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/cloud-evaluation
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-metrics-built-in
- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/evaluate-results
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/concepts/observability-overview

---

## o-2-1-5 Integrate generative workflows into applications by using Foundry SDKs and connectors

- The **Foundry SDK** (`azure-ai-projects>=2.0.0`) is the thin-client foundation; it wraps the single project endpoint and is the dependency that higher-level SDKs (Agents, Evaluation, etc.) build on.
- SDK selection guide: **Foundry SDK** for agents/evaluations/Foundry-specific features; **OpenAI SDK** for maximum OpenAI API compatibility or lowest latency; **Agent Framework** (`foundry` package) for hosted code-based multi-agent systems; **Foundry Tools SDKs** for specialized services (Vision, Speech, Content Safety).
- Connections are the mechanism to wire external services (Azure AI Search, Azure Blob Storage, Azure OpenAI, custom APIs) to a Foundry project; they are created via the portal (**Management Center → Connected resources**), Azure CLI (`az ml connection create`), or Python (`azure-ai-ml`).
- The `AIProjectClient` class (from `azure-ai-projects`) exposes sub-clients for agents, evaluations, connections, and inference through a single authenticated session.
- Streaming is supported via the Responses API and the OpenAI SDK `stream=True` parameter; partial message deltas are delivered as server-sent events.
- The Foundry **MCP server** integration lets any MCP-compatible client consume Foundry tools and agents without rewriting application code.
- Connector types supported: Azure AI Search (vector/hybrid), Azure Blob Storage, Azure OpenAI, custom HTTPS (REST), and third-party APIs via OpenAPI tool definitions.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Single client gives access to agents, evaluations, connections, inference
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],  # https://<resource>.services.ai.azure.com/api/projects/<project>
    credential=DefaultAzureCredential(),
)

# List project connections (e.g., Azure AI Search, Blob Storage)
connections = project_client.connections.list()
for conn in connections:
    print(conn.name, conn.type)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/connections-add
- https://learn.microsoft.com/en-us/python/api/overview/azure/ai-projects-readme
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/toolbox
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/migrate

---

## o-2-1-6 Configure an application to connect to a Foundry project (project endpoint, DefaultAzureCredential)

- Every Foundry project exposes a **single project endpoint** in the form `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>`; this endpoint provides access to agents, models, evaluations, and tools.
- **Authentication**: Use `DefaultAzureCredential` (from `azure-identity`) for passwordless, environment-aware auth (picks up Managed Identity in Azure, service principal via env vars, `az login` token locally); API keys can be used for `/openai/v1` routes.
- Required RBAC role for development: **Foundry User** (least-privilege); **Foundry Project Manager** for project administration. The Foundry Owner and Foundry Account Owner roles exist for broader permissions.
- For Entra-authenticated tracing and content recording, set the environment variable `AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED=true`.
- When using the OpenAI SDK directly against the Foundry project endpoint, supply the project endpoint as `azure_endpoint` and set `api_version` to the target API release.
- Environment variables commonly used: `PROJECT_ENDPOINT`, `AZURE_OPENAI_ENDPOINT`, `APPLICATION_INSIGHTS_CONNECTION_STRING`, `MODEL_DEPLOYMENT_NAME`.
- The `azure-ai-projects` package exposes both a **project client** (for Foundry-native ops like listing connections) and an **OpenAI-compatible client** (for agent runs and model calls).

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# DefaultAzureCredential handles local dev (az login), CI (service principal),
# and production (Managed Identity) without code changes
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Obtain an OpenAI-compatible client scoped to the Foundry project
openai_client = project_client.inference.get_azure_openai_client(api_version="2025-01-01-preview")
response = openai_client.chat.completions.create(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-foundry
- https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential
- https://learn.microsoft.com/en-us/python/api/overview/azure/ai-projects-readme
- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/install-cli-sdk

---

## o-2-2-1 Define agent roles, goals, conversation-tracking approach (threads), and tool schemas

- An agent is defined by three components: a **model** (from the Foundry catalog), **instructions** (goal, constraints, behavior), and **tools** (capabilities like search, code, APIs, or custom functions).
- Two agent types: **Prompt agents** (fully managed, authored in portal or code, no runtime code to maintain) and **Hosted agents** (your code packaged as a container, Foundry provides endpoint, scaling, and identity).
- **Threads** represent persistent conversation state; a thread holds the ordered message history between user and agent across multiple turns without the application managing history manually.
- Tool definitions (schemas) follow the **JSON Schema** format with `name`, `description`, and `parameters` (object with typed properties and `required` list); the model uses descriptions to decide when to invoke a tool.
- Agent instructions (`instructions` field) define the agent's persona, response style, scope limits, escalation rules, and which tools to prefer; clear, specific instructions significantly improve tool selection accuracy.
- Agents can be published to a **stable endpoint** (Agent Application), given a dedicated **Microsoft Entra identity** for secure downstream resource access (RBAC without shared keys), and version-controlled.
- The **Agents Playground** in the Foundry portal enables interactive testing of agents, tool connectivity, and prompt variations before publishing.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Create a prompt agent with a defined role and tool schema
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="inventory-agent",
    instructions=(
        "You are an inventory assistant. Answer questions about stock levels. "
        "Use the get_inventory tool when asked about a specific SKU. "
        "Do not make up stock quantities."
    ),
    tools=[{
        "type": "function",
        "function": {
            "name": "get_inventory",
            "description": "Return current stock count for a product SKU.",
            "parameters": {
                "type": "object",
                "properties": {"sku": {"type": "string", "description": "Product SKU identifier"}},
                "required": ["sku"],
            },
        },
    }],
)
print(f"Agent ID: {agent.id}")

# Create a thread to track conversation state
thread = project_client.agents.threads.create()
print(f"Thread ID: {thread.id}")
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/development-lifecycle
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/agent-applications
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/agent-identity
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstarts/get-started-code

---

## o-2-2-2 Build agents that integrate retrieval, function-calling, and conversation memory

- **Function calling** lets an agent emit a structured tool-call request (`tool_calls` in the response) that your application code must execute and return as a `tool` role message; the run enters `requires_action` status until you submit results.
- The function calling lifecycle: (1) define function + schema, (2) create agent with tool, (3) create thread + message, (4) poll run status, (5) detect `requires_action`, (6) execute function in your code, (7) submit `tool_outputs`, (8) poll to completion.
- **Tool outputs expire 10 minutes after run creation**—submit function results before this window closes.
- **Memory** (preview) is a platform tool that stores and retrieves key facts across sessions; it persists user-specific or session-specific state without custom database code.
- **File search** is a built-in tool that indexes uploaded documents, enabling the agent to retrieve and cite content from uploaded PDFs, Word docs, or text files during a conversation.
- Conversation memory across turns is maintained automatically within a thread; no manual message history management is required when using threads.
- For retrieval, attach the **Azure AI Search** tool or **file search** tool to the agent; for live data, use **function calling** with your own backend logic.

```python
import json
from azure.ai.projects.models import MessageRole, RunStatus

# Add a user message to the thread
project_client.agents.messages.create(
    thread_id=thread.id, role=MessageRole.USER, content="Is SKU-42 in stock?"
)

# Start a run
run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)

# Poll until the run needs a function result or completes
while run.status in (RunStatus.QUEUED, RunStatus.IN_PROGRESS, RunStatus.REQUIRES_ACTION):
    import time; time.sleep(1)
    run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)
    if run.status == RunStatus.REQUIRES_ACTION:
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        outputs = []
        for tc in tool_calls:
            args = json.loads(tc.function.arguments)
            result = {"sku": args["sku"], "quantity": 150}   # your real logic here
            outputs.append({"tool_call_id": tc.id, "output": json.dumps(result)})
        run = project_client.agents.runs.submit_tool_outputs(
            thread_id=thread.id, run_id=run.id, tool_outputs=outputs
        )

# Retrieve final response
msg = project_client.agents.messages.get_last_message_by_role(
    thread_id=thread.id, role=MessageRole.AGENT
)
print(msg.text_messages[0].text.value)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/function-calling
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/file-search
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/memory
- https://learn.microsoft.com/en-us/python/api/overview/azure/ai-agents-readme
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/tool-catalog

---

## o-2-2-3 Integrate agent tools: APIs (OpenAPI), knowledge stores, Azure AI Search, content understanding, custom functions

- **OpenAPI tool**: Pass an OpenAPI 3.0/3.1 specification to the agent; the Foundry model can then call external HTTP services without custom code. Supports three auth methods: `anonymous`, `API key`, and `managed identity`.
- **Azure AI Search tool**: Connects an agent to an existing Azure AI Search index for knowledge retrieval. The index must have at least one searchable text field and optionally vector fields; supports Simple, Semantic, Vector, Hybrid, and Hybrid+Semantic search types.
- When using the Azure AI Search tool, the connection name in the Foundry project **must match the index name**; create the connection via CLI (`az ml connection create`), Python `AzureAISearchConnection`, or the portal's **Connected resources** page.
- **Azure AI Search tool limitation**: Only one index per tool instance; use **connected agents** (see o-2-2-4) to fan out queries across multiple indexes.
- **Content Understanding** (via Azure AI Content Understanding in Foundry Tools) enables multimodal RAG by extracting structured metadata from documents, images, audio, and video before indexing.
- **Code Interpreter** is a built-in sandboxed tool that lets agents write and execute Python code for data analysis, chart generation, and file manipulation.
- **Azure Functions** and **MCP servers** can be wired as agent tools; Azure Functions integrate via a queue-based pattern and the `azure-ai-projects` Azure Function tool definition; MCP servers can be added from the Foundry portal tool catalog.

```python
from azure.ai.agents.models import AzureAISearchTool, AzureAISearchQueryType
import os

# Attach Azure AI Search tool to an agent
search_tool = AzureAISearchTool(
    index_connection_id=os.environ["SEARCH_CONNECTION_ID"],  # ARM resource ID of the connection
    index_name="product-index",
    query_type=AzureAISearchQueryType.VECTOR_SEMANTIC_HYBRID,
    top_k=5,
)

agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="knowledge-agent",
    instructions="Answer questions grounded in the product knowledge base.",
    tools=search_tool.definitions,
    tool_resources=search_tool.resources,
)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/azure-ai-search
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/openapi-spec
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/azure-functions
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/code-interpreter
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/tool-catalog

---

## o-2-2-4 Implement orchestrated multi-agent solutions (connected agents / multi-agent)

- **Connected Agents** (classic API `2025-05-15-preview`) implement a primary/subagent hierarchy: the main agent delegates tasks to specialized subagents using natural language routing—no hardcoded routing logic needed.
- The `ConnectedAgentTool` requires an `id` (subagent ID), `name` (machine-readable, letters and underscores only), and `description` (when to invoke); the description guides the main agent's delegation decisions.
- **Maximum depth is 2**: a parent agent can have multiple sibling subagents, but subagents cannot have their own subagents. Violating this produces an `Assistant Tool Call Depth Error`.
- Connected agent responses are returned only to the main agent, not directly to the end user; the main agent synthesizes a final response.
- For production, **publish connected agents and the main agent separately** as Agent Applications; each receives its own stable endpoint and Entra identity.
- The **new recommended approach** for multi-agent orchestration is the Workflows API (`2025-11-15-preview`), which supersedes the classic connected agents pattern.
- For code-based multi-agent systems, use **Agent Framework** with `FoundryChatClient`; LangGraph and OpenAI Agents SDK also integrate with the Foundry Responses API for complex graph-based agent topologies.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ConnectedAgentTool, MessageRole
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Create specialized subagent
stock_agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="stock_price_bot",
    instructions="Return the stock price for a given company ticker symbol.",
)

# Wire subagent into main agent via ConnectedAgentTool
connected_tool = ConnectedAgentTool(
    id=stock_agent.id,
    name="stock_price_bot",
    description="Gets the current stock price of a company.",
)

main_agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="research_agent",
    instructions="You are a financial research assistant. Delegate stock lookups to available tools.",
    tools=connected_tool.definitions,
)

thread = project_client.agents.threads.create()
project_client.agents.messages.create(
    thread_id=thread.id, role=MessageRole.USER, content="What is Microsoft's stock price?"
)
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=main_agent.id)
print(f"Run status: {run.status}")
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/connected-agents
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/workflow
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/agent-applications
- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview

---

## o-2-2-5 Build autonomous or semiautonomous workflows with safeguards and approval flow controls

- **Human-in-the-Loop (HITL)** is implemented with the AG-UI protocol: the agent generates tool calls, the server sends approval requests to the client, the user approves or rejects, and the server proceeds accordingly.
- Tool-level approval modes: `always_require` (every invocation needs approval) and `never_require` (fully autonomous); use `always_require` for irreversible or high-risk actions (deletions, payments, external emails).
- **Task Adherence** (preview guardrail) detects misaligned tool invocations—wrong tool, incorrect inputs, or responses inconsistent with user intent—and provides a signal to block the invocation or escalate to HITL review.
- **Content Safety / Guardrails**: Foundry guardrails apply input/output content filtering (Violence, Sexual, Self-harm, Hate/Unfairness severity levels) and **Spotlighting** to mitigate prompt injection, including cross-prompt injection attacks (XPIA).
- Guardrails are assigned to an agent explicitly; if no guardrail is assigned, the model's default guardrail applies. Verify assignment via SDK or portal when troubleshooting.
- **Role-based access control** (RBAC) restricts who can create, invoke, and modify agents—`Foundry User` for invocation, `Foundry Project Manager` for management operations.
- Private networking (virtual network injection for hosted agents, private endpoints for prompt agents) provides network-level isolation for compliance-sensitive autonomous workflows.

```python
# AG-UI Human-in-the-Loop pattern (conceptual — requires AG-UI server-side library)
from agui import tool, ToolApprovalMode

@tool(approval_mode=ToolApprovalMode.ALWAYS_REQUIRE)
def delete_record(record_id: str) -> str:
    """Delete a customer record by ID. ALWAYS requires human approval."""
    # actual deletion logic here
    return f"Record {record_id} deleted."

@tool(approval_mode=ToolApprovalMode.NEVER_REQUIRE)
def read_record(record_id: str) -> dict:
    """Read a customer record — read-only, no approval needed."""
    return {"id": record_id, "name": "Example Customer"}
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/human-in-the-loop-agui
- https://learn.microsoft.com/en-us/azure/ai-foundry/guardrails/guardrails-overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/agentic-workflows-task-adherence
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview#enterprise-capabilities
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/virtual-networks

---

## o-2-2-6 Integrate monitoring into deployed agents, evaluate agent behavior, perform error analysis

- The **Agent Monitoring Dashboard** (Foundry portal → Build → select agent → Monitor tab) shows operational metrics: run success rate, token usage over time, evaluation scores, and red-teaming signal data.
- Monitoring requires **Application Insights** to be connected to the Foundry project; traces from all agent runs stream to Application Insights and appear in the Foundry **Tracing** UI and Azure Monitor.
- **Continuous evaluation** (preview) automatically evaluates ongoing agent traffic against configured metrics on a schedule; results feed back into the monitoring dashboard.
- Error analysis patterns: check run `status` for `failed`, inspect `last_error.message`, review trace spans in Application Insights to identify which tool call or model step caused the failure.
- The Agent monitoring dashboard groups metrics by: **Summary** (high-level KPIs), **Evaluation scores** (quality metrics over time), **Run success rates**, and **Token usage per model**.
- Key agent evaluators for ongoing monitoring: Intent Resolution, Task Adherence, Tool Call Success, Customer Satisfaction, and Groundedness.
- **AI Red Teaming Agent** (preview) can be scheduled from the monitoring dashboard to periodically probe deployed agents for safety and security vulnerabilities.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Connect to Application Insights for agent monitoring
app_insights_conn_str = project_client.telemetry.get_connection_string()
configure_azure_monitor(connection_string=app_insights_conn_str)

tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("agent-invocation"):
    run = project_client.agents.runs.create_and_process(
        thread_id=os.environ["THREAD_ID"], agent_id=os.environ["AGENT_ID"]
    )
    if run.status == "failed":
        print(f"Agent run failed: {run.last_error}")
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/how-to-monitor-agents-dashboard
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/cloud-evaluation
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/evaluate-agents
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/concepts/trace-agent-concept
- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/run-scans-ai-red-teaming-agent

---

## o-2-3-1 Tune generation behavior: prompt engineering, model parameters (temperature, top_p, max tokens)

- **System message** sets the model's role, persona, and behavioral constraints; it is the most impactful lever for shaping output quality and tone before touching numeric parameters.
- **Temperature** (0–2): controls output randomness. Lower values (e.g., 0.1–0.3) produce more deterministic, focused responses; higher values (0.7–1.0) increase creativity and diversity. Default is 1.
- **top_p** (nucleus sampling, 0–1): restricts generation to the smallest set of tokens whose cumulative probability exceeds `top_p`. Altering `top_p` instead of `temperature` is an alternative randomness control—**avoid adjusting both simultaneously**.
- **max_tokens** (or `max_completion_tokens`): hard upper limit on response length in tokens; one token ≈ 4 characters in English. For GPT-4 class models, the shared prompt + response context window is up to 128,000 tokens.
- **Prompt engineering techniques**: role assignment ("You are a…"), few-shot examples (provide input/output pairs in the prompt), explicit format constraints ("Respond in JSON"), and chain-of-thought triggering ("Think step by step before answering").
- Structured output / JSON mode forces the model to emit valid JSON; activate with `response_format={"type": "json_object"}` (or `json_schema` for strict schema enforcement in newer API versions).
- For code models, include language and style constraints in the system message and use lower temperature (0.0–0.2) for deterministic output.

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a concise financial analyst. Answer in three bullet points."},
        {"role": "user",   "content": "What are the key risks of rising interest rates?"},
    ],
    temperature=0.3,          # low randomness → consistent, factual
    top_p=1.0,                # nucleus sampling at full probability mass
    max_tokens=300,           # cap output length
    response_format={"type": "text"},
)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering
- https://learn.microsoft.com/en-us/azure/ai-services/openai/reference
- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/chatgpt
- https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/json-mode
- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-router

---

## o-2-3-2 Implement model reflection, chain-of-thought evaluations, self-critique loops

- **Chain-of-thought (CoT)** prompting instructs the model to reason through intermediate steps before producing a final answer; commonly triggered with phrases like "Think step by step" or by providing few-shot examples that include reasoning traces.
- **Reasoning models** (e.g., `o1`, `o3`, `o4-mini` series) perform internal multi-step reasoning without explicit CoT prompting; they are best for math, logic, and code tasks requiring complex inference.
- **Self-critique loops** implement a reflection pattern: the model generates an initial response, then is asked to critique or score that response, and finally revises it; this can be implemented as a multi-turn conversation or separate API calls.
- **Agentic reflection**: agents can be instructed to call a validation tool or evaluator function after producing an output, then update their response based on the feedback before returning to the user.
- **Task Adherence** (Foundry guardrail) provides automated reflection at the tool-call level, detecting when tool invocations deviate from user intent and triggering correction or escalation.
- Programmatic self-critique can be implemented by running a second LLM call with a "critique" system prompt on the first output, then feeding that critique back as context for a final generation.
- For RAG, implement a **self-grounding check**: after generating a response, prompt the model to identify which retrieved chunks support each claim; this surfaces hallucinations for correction.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_KEY"]),
)

# Step 1: Initial response with CoT trigger
r1 = client.complete(
    model="gpt-4o",
    messages=[
        SystemMessage("Think step by step, then give a final answer."),
        UserMessage("How many prime numbers are there below 50?"),
    ],
    temperature=0.0,
)
initial = r1.choices[0].message.content

# Step 2: Self-critique
r2 = client.complete(
    model="gpt-4o",
    messages=[
        SystemMessage("You are a meticulous reviewer. Identify any errors in the response below and provide a corrected answer."),
        UserMessage(f"Response to review:\n{initial}"),
    ],
    temperature=0.0,
)
print(r2.choices[0].message.content)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering
- https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/o1-o3-chain-of-thought
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/agentic-workflows-task-adherence
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/agent-optimizer-overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/evaluate-generative-ai-app

---

## o-2-3-3 Observability: tracing (OpenTelemetry), token analytics, safety signals, latency breakdowns

- Foundry observability is built on **OpenTelemetry (OTeL)**; every model call, tool invocation, and agent decision becomes a **span** within a distributed trace, exportable to Application Insights or any OTeL-compatible backend.
- Enable tracing in Python with `opentelemetry-sdk` + `azure-core-tracing-opentelemetry` + `azure-monitor-opentelemetry-exporter` (or `azure-monitor-opentelemetry` for the all-in-one package).
- To export to Application Insights: retrieve the connection string from `project_client.telemetry.get_connection_string()` and pass it to `configure_azure_monitor()`.
- Set `AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED=true` to record actual prompt and response text in traces (note: may capture PII; disabled by default).
- The **Foundry Tracing UI** (portal → project → Tracing) lets you filter, inspect, and step through individual spans: model inputs, outputs, token counts, latencies per span, and tool call results.
- **Token analytics** are available on the Agent Monitoring Dashboard; usage is broken down per model, per run, and over time—essential for cost attribution and quota planning.
- **Safety signals** (content filter hits, guardrail activations, XPIA detections) appear as span attributes in traces and as aggregate counts in the monitoring dashboard.
- **Latency breakdowns**: because each span includes start/end timestamps, you can identify which step (retrieval, model inference, function execution) contributes most to end-to-end latency.

```python
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Configure OTeL → Application Insights
exporter = AzureMonitorTraceExporter(
    connection_string=os.environ["APPLICATION_INSIGHTS_CONNECTION_STRING"]
)
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("my-app")

with tracer.start_as_current_span("rag-pipeline") as span:
    span.set_attribute("query", "What is the refund policy?")
    # ... retrieval and generation calls here
    span.set_attribute("retrieved_chunks", 3)
    span.set_attribute("completion_tokens", 142)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/trace-agents
- https://learn.microsoft.com/en-us/python/api/overview/azure/ai-agents-readme#tracing
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/how-to-monitor-agents-dashboard
- https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview
- https://learn.microsoft.com/en-us/azure/ai-foundry/observability/concepts/observability-overview

---

## o-2-3-4 Orchestrate multiple models, flows, or hybrid LLM and rules engines

- **Model router** is a deployable Foundry model that selects the optimal underlying LLM **per turn** based on query complexity, cost, and capability—exposed as a single deployment endpoint with no routing code required in the application.
- Model router routing modes: **Quality** (frontier models for complex tasks), **Balanced** (mixed capability/cost), **Cost** (fast, cheap models for classification/triage). You can restrict the model subset per deployment.
- Using model router with agents: assign a model router deployment as the agent's model; the router automatically picks cheaper models for simple turns (greetings, confirmations) and frontier models for complex tool-calling chains.
- **Semantic Kernel** and **LangGraph** integrate with the Foundry Responses API; they enable graph-based orchestration where different graph nodes invoke different models, tools, or rule engines.
- **Hybrid LLM + rules engines**: implement deterministic routing guards before LLM calls (e.g., regex or keyword checks to block off-topic queries) and validate LLM outputs against schema or business rules after generation.
- For cost-efficient multi-model pipelines, use a small model (e.g., `gpt-4.1-mini`) for intent classification and routing, then a larger model only for tasks that require deep reasoning or generation.
- The **Foundry Workflows API** (`2025-11-15-preview`) supports declarative multi-agent orchestration definitions, enabling visual composition of model steps, tool calls, and branching logic in the Foundry portal.

```python
import os
from openai import AzureOpenAI

# Model router deployed as "model-router" — single endpoint, auto model selection
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_KEY"],
    api_version="2025-01-01-preview",
)

def smart_complete(user_message: str) -> str:
    """Routes to the best model per turn via model-router deployment."""
    response = client.chat.completions.create(
        model="model-router",          # model router deployment name
        messages=[{"role": "user", "content": user_message}],
    )
    chosen_model = response.model      # which underlying model was selected
    print(f"Routed to: {chosen_model}")
    return response.choices[0].message.content

# Hybrid: rules gate + LLM
def safe_complete(user_message: str) -> str:
    blocked_keywords = ["competitor", "lawsuit"]
    if any(kw in user_message.lower() for kw in blocked_keywords):
        return "I can't assist with that topic."
    return smart_complete(user_message)
```

Sources:
- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-router
- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/model-router
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/use-model-router-with-agents
- https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/workflow
- https://learn.microsoft.com/en-us/semantic-kernel/overview/

---

*Generated from public Microsoft Learn documentation only. All source URLs verified during authoring session (July 2026).*
