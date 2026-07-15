# GH-300 Domain 3 — Research Pack (Understand GitHub Copilot data and architecture)

Clean-room notes paraphrased from **public Microsoft Learn** only. Every objective lists verified
facts + a **Sources:** list of REAL learn.microsoft.com URLs. No docs.github.com, blogs, or decks used.
Grounded via fetch_webpage against learn.microsoft.com training modules and the GH-300 study guide.

Primary grounding modules:
- Introduction to prompt engineering with GitHub Copilot (units 3 process flow, 4 data, 5 LLMs)
- Introduction to GitHub Copilot (unit 2 pair programmer / plans)
- Responsible AI with GitHub Copilot (unit 2 mitigate AI risks)

---

## 3.1 Describe data handling and flow

### 3.1.1 Explain data usage, flow, and sharing (data-usage-flow)
- GitHub Copilot moves data in an **inbound** flow (prompt + context → filters → model) and an **outbound**
  flow (model output → filters → suggestion delivery). It repeats per interaction.
- The user prompt is sent to Copilot's servers over **HTTPS** (secure, confidential transmission).
- A **proxy server hosted in a GitHub-owned Microsoft Azure tenant** sits between the client and the model
  and filters traffic in both directions.
- **Data retention / training:**
  - Copilot **in the code editor does not retain** the prompts (code or other context) used to generate a
    suggestion, and does **not** use them to train the foundational models — prompts are **discarded once a
    suggestion is returned**.
  - **Individual** subscribers can **opt out** of sharing their prompts, which would otherwise be used to
    **fine-tune** GitHub's foundational model.
  - For Copilot **Chat used outside the code editor** (and CLI, Mobile, Chat on GitHub.com), GitHub
    typically **retains prompts, suggestions, and supporting context for 28 days**. Retention for Chat
    *within* the editor may vary.
- **Business / Enterprise** plans are built for organizations and provide enterprise-grade security, safety,
  and privacy (e.g., IP indemnity, public-code filtering, centralized policy). Prompts and suggestions on
  these organizational plans are **not used to train the models**.
- Sources:
  - https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/4-github-copilot-data
  - https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/3-github-copilot-user-prompt-process-flow
  - https://learn.microsoft.com/en-us/training/modules/introduction-to-github-copilot/2-github-copilot-your-ai-pair-programmer

### 3.1.2 Describe input processing and prompt building (input-processing)
- The prompt Copilot sends the model is **not just what you typed** — Copilot assembles a richer prompt from
  the surrounding context. Context it gathers includes:
  - Code **before and after the cursor** position.
  - The **filename and file type** being edited.
  - **Adjacent open tabs** (other open files) so suggestions align with the wider project.
  - **Project structure and file paths**.
  - **Programming languages and frameworks** in use.
- Copilot uses a **Fill-in-the-Middle (FIM)** pre-processing technique that considers both the preceding and
  following code, expanding the model's understanding for more accurate, relevant suggestions.
- These steps translate a high-level natural-language request (a comment or chat message) into a concrete
  coding task before the model ever generates code.
- LLMs consider not just the current file but **other open files and tabs** to produce context-aware
  completions.
- **Context window** is finite: standard Copilot completions typically span **~200–500 lines of code / up to
  a few thousand tokens**; **Copilot Chat operates with about a 4k-token** context window. Break large
  problems into smaller, focused prompts.
- Sources:
  - https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/3-github-copilot-user-prompt-process-flow
  - https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/4-github-copilot-data
  - https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/5-github-copilot-large-language-models

### 3.1.3 Explain proxy filtering and post-processing (proxy-filtering)
- **Inbound proxy filter:** after context is gathered and the prompt is built, it passes securely to the
  proxy server (GitHub-owned Azure tenant). The proxy **filters traffic and blocks attempts to hack the
  prompt** or manipulate the system into revealing how the model generates suggestions (prompt-injection
  defense).
- **Toxicity filtering (inbound):** before intent extraction / code generation, content filtering blocks
  **hate speech, offensive, or inappropriate content** and **filters out personal data** (names, addresses,
  identification numbers) to protect privacy.
- **Code generation:** the filtered, analyzed prompt goes to the **LLM**, which generates suggestions from
  the prompt plus surrounding context.
- **Outbound post-processing / response validation:** once the model responds, the **toxicity filter removes
  harmful generated content**, then the proxy applies a **final layer of checks**:
  - **Code quality** — scans for common bugs / vulnerabilities such as **cross-site scripting (XSS)** or
    **SQL injection**.
  - **Matching public code (optional)** — administrators can enable a filter that **blocks suggestions over
    ~150 characters that closely resemble existing public code on GitHub**, preventing coincidental matches
    from being surfaced as original content.
  - Any part of a response that fails these checks is **truncated or discarded**.
- **Delivery + feedback loop:** only responses that pass all filters are delivered. Copilot then starts a
  feedback loop — learning from **accepted** suggestions and from **modifications / rejections** — and
  repeats the process for later prompts.
- Sources:
  - https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/3-github-copilot-user-prompt-process-flow
  - https://learn.microsoft.com/en-us/training/modules/introduction-to-github-copilot/2-github-copilot-your-ai-pair-programmer

---

## 3.2 Understand lifecycle and limitations

### 3.2.1 Visualize the code suggestion lifecycle (suggestion-lifecycle)
- End-to-end lifecycle of a single suggestion (stitching the inbound/outbound flow):
  1. **Capture** — you write a comment, code, or chat message; Copilot gathers editor context
     (cursor-surrounding code, filename/type, open tabs, project structure, language/framework).
  2. **Transmit** — the assembled prompt is sent over **HTTPS** to Copilot's servers.
  3. **Proxy + safety filters (inbound)** — proxy blocks prompt hacking; toxicity/PII filtering runs before
     generation.
  4. **Generate** — the **LLM** produces candidate suggestion(s) from prompt + context.
  5. **Post-process (outbound)** — toxicity filter + proxy checks (code quality for XSS/SQLi; optional
     public-code matching); failing content is truncated or discarded.
  6. **Deliver** — surviving suggestion is shown inline (ghost text) or in chat.
  7. **Act + feedback** — you **accept, modify, or reject**; that action feeds Copilot's feedback loop and
     the cycle repeats for the next prompt.
- Copilot is not a one-shot autocomplete; it's a **continuous loop** that incorporates cumulative feedback
  and interaction/context data to refine intent understanding over time.
- Sources:
  - https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/3-github-copilot-user-prompt-process-flow
  - https://learn.microsoft.com/en-us/training/modules/introduction-to-github-copilot/2-github-copilot-your-ai-pair-programmer

### 3.2.2 Describe the limitations of LLMs and Copilot (llm-limitations)
- LLMs are **neural networks with millions/billions of parameters** trained on vast, diverse text; they
  **predict** likely text/code — output is **probabilistic**, not guaranteed correct.
- **Context-window limits:** the model can only "see" a bounded amount of code/text at once (standard
  completions ~200–500 lines / a few thousand tokens; Chat ~4k tokens). Anything outside that window is
  invisible to the model, so large or cross-file problems may get incomplete answers.
- **Training-data / knowledge limits:** the model's knowledge reflects the data it was trained on. It can be
  **outdated** relative to newer libraries/APIs and can reproduce **biases** present in training data.
- **Reliability limits (Responsible AI framing):** AI systems can make decisions that are **hard to
  interpret**, leading to reduced transparency/accountability, and can produce **unintended, harmful
  outcomes** such as **biased decision-making or privacy violations**. Suggestions may be plausible-looking
  but wrong (hallucination) or insecure.
- **Mitigations:** always **validate AI output**, keep a **human in the loop / human oversight**, apply
  **governance frameworks and transparency**, and use safeguards (content exclusions, public-code filter).
  Copilot is an assistant, not a replacement for developer judgment.
- Sources:
  - https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/5-github-copilot-large-language-models
  - https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/4-github-copilot-data
  - https://learn.microsoft.com/en-us/training/modules/responsible-ai-with-github-copilot/2-manage-ai-risks

---

## Cross-check
- GH-300 study guide (Domain 3 objectives verified): https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-300
- Module landings: 
  - https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/
  - https://learn.microsoft.com/en-us/training/modules/introduction-to-github-copilot/
  - https://learn.microsoft.com/en-us/training/modules/responsible-ai-with-github-copilot/
