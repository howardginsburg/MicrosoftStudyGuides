# AI-103 Domain 5 — Source pack (public Microsoft Learn only)

> **Scope:** Domain 5 "Implement information extraction solutions" (10–15%).  
> All content paraphrased from public Microsoft Learn documentation. No exam dumps or third-party sources.

---

## o-5-1-1 Ingest and index content: documents, images, audio, video (indexers, data sources)

- An **indexer** in Azure AI Search is a crawler that uses a *pull model* to extract content from a connected data source and populate a search index without custom ingestion code. Each indexer targets exactly one data source and one destination index.
- Indexers progress through four stages: **document cracking** (opening files and extracting text/images), **field mappings** (source → destination field routing), **skillset execution** (optional AI enrichment), and **output field mappings** (enriched document tree → index fields).
- Supported built-in data sources include Azure Blob Storage, Azure Data Lake Storage Gen2, Azure SQL Database, Azure Cosmos DB (SQL, MongoDB, Gremlin), Azure Table Storage, Azure SQL Managed Instance, SQL Server on Azure VMs, Microsoft OneLake, and SharePoint Online (preview).
- Image extraction during document cracking is **disabled by default**; enable it via the `imageAction` property in indexer configuration. PDFs can yield both embedded text and inline images when cracked.
- Indexers can be run on demand or scheduled as often as every five minutes. One indexer job runs per search unit; concurrent processing requires sufficient replicas.
- **Multimodal search** pipelines extend indexers with skills for extracting page text and inline images, verbalizing images with a GenAI Prompt skill (produces natural-language captions for RAG grounding), generating embeddings, and storing extracted images in a knowledge store.
- Two extraction skill paths exist: the **Document Extraction skill** (fast, PDF bounding-box positions, no table cross-page support) and the **Azure Content Understanding skill** (supports semantic chunking, cross-page tables, AI-generated image descriptions, and multiple file types including DOCX, XLSX, PPTX).

```json
// Minimal indexer definition (REST)
{
  "name": "blob-indexer",
  "dataSourceName": "my-blob-source",
  "targetIndexName": "my-index",
  "parameters": {
    "configuration": {
      "imageAction": "generateNormalizedImages"
    }
  },
  "schedule": { "interval": "PT5M" }
}
```

Sources:
- https://learn.microsoft.com/azure/search/search-indexer-overview
- https://learn.microsoft.com/azure/search/search-how-to-create-indexers
- https://learn.microsoft.com/azure/search/multimodal-search-overview

---

## o-5-1-2 Configure semantic search, hybrid search, and vector search for grounding

- **Vector search** converts content and queries into numeric embeddings and ranks results by mathematical similarity (cosine, dot product, Euclidean). It supports similarity search, multilingual content, multimodal content, and filtered vector search; vector fields coexist with text fields in the same index.
- Two nearest-neighbor algorithms are available: **HNSW** (approximate, fast at query time) and **exhaustive KNN** (exact, useful for small result sets or when precision is critical).
- **Hybrid search** runs a full-text BM25 query and one or more vector queries **in parallel** in a single request, then merges ranked lists using **Reciprocal Rank Fusion (RRF)**. A single response set is returned; no separate calls are required.
- Adding `queryType=semantic` to a hybrid or text query invokes the **semantic ranker**, an L2 reranker that applies Microsoft's deep-learning language models (from Bing research) to reorder the top-50 initial results by semantic relevance. It also returns verbatim *captions* and optional *answers*.
- Semantic ranker scores results on a **0–4 scale** (`@search.rerankerScore`). It requires a semantic configuration that names the title, keywords, and content fields to summarize (up to 2,048 tokens per document as of November 2024).
- **Query rewrite** (semantic ranker feature) generates up to 10 reformulated variants of the query to widen recall before reranking.
- For optimal RAG grounding, combine all three: hybrid search (BM25 + vectors) + semantic ranking; benchmark testing confirms this combination delivers the best search relevance.

```http
POST /indexes/hotels/docs/search?api-version=2026-04-01
{
  "search": "historic hotel near restaurants",
  "vectorQueries": [{ "kind": "vector", "vector": [ ... ], "k": 50, "fields": "descriptionVector" }],
  "queryType": "semantic",
  "semanticConfiguration": "my-semantic-config",
  "select": "hotelName, description"
}
```

Sources:
- https://learn.microsoft.com/azure/search/vector-search-overview
- https://learn.microsoft.com/azure/search/hybrid-search-overview
- https://learn.microsoft.com/azure/search/semantic-search-overview
- https://learn.microsoft.com/azure/search/hybrid-search-how-to-query

---

## o-5-1-3 Enrichment using custom or built-in skills for text, images, and layout (skillsets)

- A **skillset** is a collection of skills attached to an indexer; it acts as a "pipeline within the pipeline" that transforms raw content into enriched, searchable output. Skillsets operate on an *enriched document* tree that accumulates transformations through the pipeline.
- **Built-in (cognitive) skills** connect to Foundry Tools (Azure AI Services) and cover: OCR (printed and handwritten text from binary files), image analysis (facial detection, landmark recognition, image description), entity recognition, key phrase extraction, sentiment and opinion mining, language detection, text translation, and PII detection.
- **Image processing scenario**: The OCR skill extracts text from images; the Image Analysis skill describes image content in natural language. Both produce text fields that flow into the search index and are mapped via *output field mappings*.
- The **Document Layout skill** (now superseded for new workloads by the Azure Content Understanding skill) and the **Azure Content Understanding skill** both support richer layout extraction including tables and sections.
- **Custom skills** wrap external REST endpoints; any code that adds value—classification models, domain-specific NLP, embedding calls to non-Azure models—can be integrated using the custom skill web API interface.
- Skillset outputs can be written to a **search index** (required), an optional **knowledge store** (blobs or tables in Azure Storage for data science/Power BI), or an **enrichment cache** to avoid reprocessing unchanged content (useful when OCR or image analysis is expensive).
- A billable Foundry resource (Azure AI Services multi-service account) must be attached to a skillset for workloads that use Foundry-backed built-in skills beyond free-tier limits.

```json
// OCR skill snippet in a skillset definition
{
  "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
  "name": "ocr-skill",
  "inputs": [{ "name": "image", "source": "/document/normalized_images/*" }],
  "outputs": [{ "name": "text", "targetName": "ocrText" }],
  "detectOrientation": true
}
```

Sources:
- https://learn.microsoft.com/azure/search/cognitive-search-concept-intro
- https://learn.microsoft.com/azure/search/cognitive-search-concept-image-scenarios
- https://learn.microsoft.com/azure/search/cognitive-search-predefined-skills

---

## o-5-1-4 Configure RAG ingestion flow: documents, chunking, embeddings, OCR

- **Integrated vectorization** is an extension of the indexer pipeline that handles both chunking (via the Text Split or Azure Content Understanding skill) and embedding generation (via embedding skills) without requiring custom orchestration code.
- The **Text Split skill** offers two modes: `pages` (multi-sentence fixed-size chunks, controlled by `maximumPageLength` in characters or tokens and `pageOverlapLength`) and `sentences` (single-sentence chunks). Starting defaults of `maximumPageLength=2000` and `pageOverlapLength=500` characters are recommended.
- Chunking is required because embedding models impose input token limits (e.g., Azure OpenAI `text-embedding-3-small` accepts up to 8,191 tokens). Overlap (10–25% of chunk size) preserves cross-boundary context.
- Supported embedding skills for integrated vectorization: **AzureOpenAIEmbedding** (text-embedding-ada-002, -3-small, -3-large), **Azure Vision multimodal embeddings** (text + images), **AML skill** (Foundry model catalog), and **custom skill** (any external endpoint).
- At query time, a **vectorizer** defined in the index schema automatically converts a text query string to a vector using the same model used during indexing—enabling end-to-end vector search without client-side embedding calls.
- **OCR in RAG**: Use the OCR skill to extract text from scanned PDFs or image-only documents before chunking and embedding. The Document Intelligence Layout model can produce Markdown output that preserves tables and headings—ideal as a chunking boundary for semantic splits.
- **Secondary indexes** (index projections) allow chunked content to populate a child index while a parent index holds document-level metadata; RAG apps query the chunk index for precision and the parent for richer context.

```python
# LangChain + Azure Document Intelligence for semantic chunking in RAG
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter

loader = AzureAIDocumentIntelligenceLoader(
    file_path="contract.pdf",
    api_key="<key>",
    api_endpoint="https://<endpoint>.cognitiveservices.azure.com/",
    api_model="prebuilt-layout"  # produces Markdown output
)
docs = loader.load()

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
    ("#", "H1"), ("##", "H2"), ("###", "H3")
])
chunks = splitter.split_text(docs[0].page_content)
```

Sources:
- https://learn.microsoft.com/azure/search/vector-search-integrated-vectorization
- https://learn.microsoft.com/azure/search/vector-search-how-to-chunk-documents
- https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview
- https://learn.microsoft.com/azure/ai-services/document-intelligence/concept/retrieval-augmented-generation

---

## o-5-1-5 Connect retrieval pipelines directly to workflows and agent tools (agentic retrieval)

- **Agentic retrieval** is a multi-query pipeline built into Azure AI Search for complex, agent-to-agent and conversational RAG scenarios. It decomposes a complex query (including chat history) into focused **subqueries** using an LLM, runs them in parallel, applies semantic reranking to each, and returns a unified grounding payload.
- The pipeline has two core objects: a **knowledge base** (orchestrates the pipeline, holds query parameters and LLM configuration) and one or more **knowledge sources** (indexed = backed by an Azure AI Search index; remote = external platform content retrieved at query time).
- Three **retrieval reasoning effort** levels control LLM involvement: `minimal` (no LLM, queries issued directly), `low` (default, LLM generates subqueries), and `medium` (LLM generates subqueries plus iterative search expansion). Higher effort increases latency and cost but handles more complex questions.
- Agentic retrieval powers **Foundry IQ** in the Microsoft Foundry portal—the managed knowledge layer that exposes permission-aware knowledge bases to Foundry Agent Service. Agents reference knowledge bases as a tool during reasoning.
- Billing is **token-based** (not per-query): Azure AI Search bills for retrieval tokens used in subquery execution and semantic reranking; Azure OpenAI bills for query planning (input/output tokens). A monthly free allowance applies.
- For custom integrations, call the knowledge base `retrieve` action or connect via the **MCP endpoint** exposed by agentic retrieval. The response includes merged content, optional source references (citations), and an activity log.
- A search index used with agentic retrieval should include a **semantic configuration** (required for internal reranking) and vector fields (for hybrid subquery execution).

```python
# Pseudocode: calling agentic retrieval retrieve action
response = search_client.knowledge_bases.retrieve(
    knowledge_base_name="my-kb",
    query="What are the refund policies for premium accounts?",
    conversation_history=[{"role": "user", "content": "I have a premium account."}],
    reasoning_effort="low"
)
grounding_content = response["content"]  # pass to LLM for answer generation
```

Sources:
- https://learn.microsoft.com/azure/search/agentic-retrieval-overview
- https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-knowledge-base
- https://learn.microsoft.com/azure/search/search-what-is-azure-search#what-is-agentic-retrieval
- https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-pipeline

---

## o-5-2-1 Extract information via multimodal pipelines combining OCR, layout analysis, field extraction (Document Intelligence)

- Azure AI Document Intelligence's **layout model** (`prebuilt-layout`, GA v4.0 / 2024-11-30) is a machine-learning API that performs OCR and document structure analysis in a single call, extracting text, tables, selection marks, figures, headings, and logical roles (title, footer).
- Document structure analysis distinguishes **geometric roles** (text blocks, tables, figures, selection marks) from **logical roles** (titles, headings, footers), enabling structure-aware downstream processing.
- Supported input formats: PDF, JPEG/JPG, PNG, BMP, TIFF, HEIF, and Office formats (DOCX, XLSX, PPTX, HTML). Files up to 500 MB (paid tier); up to 2,000 pages per PDF/TIFF document.
- The layout model can output results as **Markdown**, preserving table structure, heading hierarchy, and paragraph boundaries—making it directly consumable by LLMs for RAG without additional parsing.
- **Query field extraction** allows callers to specify fields to extract from a document at inference time without training a custom model—useful for ad-hoc structured extraction scenarios.
- The **prebuilt model portfolio** covers over 100 domain-specific document types including invoices, receipts, ID documents, tax forms (1040, W-2, 1099 variants), mortgage forms (1003, 1004), contracts, and pay stubs, each with tailored field schemas.
- Language support spans 309 printed languages and 12 handwritten languages for the layout model, enabling multilingual OCR across global enterprise document sets.

```python
# Extract layout as Markdown using Document Intelligence SDK
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentContentFormat

client = DocumentIntelligenceClient(endpoint, credential)
poller = client.begin_analyze_document(
    "prebuilt-layout",
    AnalyzeDocumentRequest(url_source="https://example.com/doc.pdf"),
    output_content_format=DocumentContentFormat.MARKDOWN
)
result = poller.result()
markdown_content = result.content  # tables and headings preserved
```

Sources:
- https://learn.microsoft.com/azure/ai-services/document-intelligence/prebuilt/layout?view=doc-intel-4.0.0
- https://learn.microsoft.com/azure/ai-services/document-intelligence/model-overview?view=doc-intel-4.0.0
- https://learn.microsoft.com/azure/ai-services/document-intelligence/concept/retrieval-augmented-generation?view=doc-intel-4.0.0
- https://learn.microsoft.com/azure/ai-services/document-intelligence/concept/query-fields?view=doc-intel-4.0.0

---

## o-5-2-2 Produce clean, grounded representations for agents and RAG by using Content Understanding

- **Azure AI Content Understanding** (a Foundry Tool) processes documents, images, audio, and video into user-defined structured output using generative AI, streamlining ingestion into RAG and agentic pipelines.
- For RAG and agentic use cases, Content Understanding delivers **clean Markdown representations** with layout context preserved (paragraphs, tables, figures), plus AI-generated figure descriptions for charts and diagrams that are normally invisible to text-only extractors.
- **Grounding** is a first-class capability: every extracted or generated field value is accompanied by a source region reference (bounding box or timestamp) enabling citations and human-in-the-loop verification in automation workflows.
- **Confidence scores** (0–1 range) accompany each extracted field value; high-confidence values can flow through automation without human review, while low-confidence values are flagged for manual inspection—enabling straight-through processing.
- The `prebuilt-documentSearch` RAG analyzer extracts paragraphs, tables, figures (with AI-generated textual descriptions for charts/diagrams as chart.js or mermaid.js syntax), hand-written annotations, and a document-level summary. Recommended for document ingestion in RAG workflows.
- Content Understanding supports classification at ingestion time—a document can be categorized first (e.g., invoice vs. contract), then routed to the appropriate domain-specific analyzer, enabling multi-document-type pipelines.
- Output is configurable: **Markdown** for search/retrieval or **structured JSON** matching a user-defined field schema for automation and analytics—both produced by the same analyzer invocation.

```http
POST /analyzers/prebuilt-documentSearch:analyze
Content-Type: application/json

{
  "url": "https://storage.example.com/report.pdf"
}
```

Sources:
- https://learn.microsoft.com/azure/ai-services/content-understanding/overview
- https://learn.microsoft.com/azure/ai-services/content-understanding/concepts/prebuilt-analyzers
- https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview

---

## o-5-2-3 Implement analyzers generating structured or markdown outputs for downstream reasoning (Content Understanding)

- An **analyzer** in Content Understanding is a versioned, reusable configuration that specifies: content type (document, image, audio, video), extraction settings, field schema, output format, and which Foundry AI models to invoke. Analyzers are the core unit of work in the service.
- **Four analyzer categories**: *content extraction* (OCR + layout, no LLM required: `prebuilt-read`, `prebuilt-layout`, `prebuilt-digitalParse`), *base analyzers* (per-modality processing foundations), *RAG analyzers* (semantic Markdown + figure description: `prebuilt-documentSearch`, `prebuilt-imageSearch`, `prebuilt-audioSearch`, `prebuilt-videoSearch`), and *domain-specific* (preconfigured schemas for invoices, IDs, tax forms, mortgages, contracts).
- The **field schema** within an analyzer definition drives three extraction modes: `Extract` (pull verbatim values from the document), `Classify` (label content from a fixed category set), or `Generate` (use an LLM to produce a value such as a summary or description). These can be mixed in one analyzer.
- RAG analyzers produce **Markdown output** that preserves document structure for LLM reasoning. `prebuilt-documentSearch` additionally outputs chart analysis as `chart.js` syntax and diagram analysis as `mermaid.js` syntax.
- Custom analyzers are created by providing a `baseAnalyzerId` (one of the four base analyzers), then adding or overriding fields. Prebuilt analyzer definitions can be retrieved with a `GET`, modified, and published as a new named analyzer. Use the `copy` operation to freeze a prebuilt's definition against future API-version changes.
- The analyze endpoint accepts a document URL or binary payload and returns a response that includes extracted content, field values with confidence scores, grounding regions, and (for RAG analyzers) full Markdown output.
- **Audio and video RAG analyzers** (`prebuilt-audioSearch`, `prebuilt-videoSearch`) transcribe speech, auto-segment video by topic/scene change, and generate per-segment summaries with people/places/actions, all in a RAG-ready format for indexing.

```json
// Custom analyzer definition (excerpt)
{
  "analyzerId": "myInvoiceAnalyzer",
  "baseAnalyzerId": "prebuilt-document",
  "config": { "enableOcr": true },
  "fieldSchema": {
    "fields": {
      "vendorName": { "type": "string", "method": "extract" },
      "invoiceSentiment": {
        "type": "string",
        "method": "classify",
        "enum": ["positive", "neutral", "disputed"]
      },
      "executiveSummary": { "type": "string", "method": "generate" }
    }
  },
  "models": { "completion": "gpt-5.2" }
}
```

Sources:
- https://learn.microsoft.com/azure/ai-services/content-understanding/concepts/analyzer-reference
- https://learn.microsoft.com/azure/ai-services/content-understanding/concepts/prebuilt-analyzers
- https://learn.microsoft.com/azure/ai-services/content-understanding/overview
- https://learn.microsoft.com/azure/ai-services/document-intelligence/concept/markdown-elements?view=doc-intel-4.0.0
