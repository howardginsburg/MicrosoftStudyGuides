# Domain 4 — Apply prompt engineering and context crafting — Source pack (clean-room)

All facts below are grounded in the public Microsoft Learn module **"Introduction to prompt
engineering with GitHub Copilot"** (learning path *GitHub Copilot Fundamentals — Part 1 of 2*).
Research notes are organized by objective id. Each objective ends with real learn.microsoft.com URLs.

---

## obj-4-1-1 — 4.1.1 Describe prompt structure and context

- **Prompt engineering** = the process of crafting clear instructions to guide AI systems (like
  GitHub Copilot) to generate context-appropriate code tailored to a project's specific needs. Goal:
  code that is **syntactically, functionally, and contextually correct**.
- A prompt to Copilot is more than the literal text you type — Copilot **assembles** a richer prompt
  by combining your natural-language request (a comment or a Chat message) with surrounding context.
- Effective prompt "structure" in the Learn content maps to giving Copilot: a **clear single goal**
  (what you want), **context/details** (comments, related open files), and optionally **examples** it
  can pattern-match from.
- Best practice "Provide enough clarity": e.g., *"Write a Python function to filter and return even
  numbers from a given list"* is both single-focused and specific.
- Best practice "Provide enough context with details": adding comments at the top of a file gives
  Copilot more context and yields better suggestions; keep detail but stay concise.

Sources:
- https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/
- https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/2-prompt-engineering-foundations-best-practices

---

## obj-4-1-2 — 4.1.2 Understand how context is determined

- When processing a prompt, Copilot simultaneously **collects context details**:
  - **Code before and after the cursor** position (immediate context).
  - **Filename and file type** being edited (tailors suggestions to the file type/language).
  - **Adjacent open tabs** — code in other open tabs so suggestions align with the rest of the project.
  - **Project structure and file paths.**
  - **Programming languages and frameworks** in use.
- Copilot pre-processes with the **Fill-in-the-Middle (FIM)** technique — it considers both the
  **preceding and following** code, expanding the model's understanding for more relevant suggestions.
- Copilot also uses **parallel open tabs** in the editor to gather more context about the requirements
  of your code (the "Surround" principle in practice).
- These steps translate the user's high-level request into a concrete coding task.

Sources:
- https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/3-github-copilot-user-prompt-process-flow
- https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/2-prompt-engineering-foundations-best-practices

---

## obj-4-1-3 — 4.1.3 Use zero-shot and few-shot prompting

Copilot learns from the examples you provide; Learn describes three approaches:
- **Zero-shot learning:** no examples given — Copilot relies solely on its foundational training.
  Ideal for common patterns / standard functionality (e.g., generate a Celsius↔Fahrenheit converter
  from just a comment).
- **One-shot learning:** a **single** example is provided, helping the model generate more
  context-aware responses that follow your specific patterns/conventions (consistent implementations).
- **Few-shot learning:** **several** examples are presented — a balance between zero-shot
  unpredictability and the precision of fine-tuning. Excels at sophisticated implementations that
  handle multiple scenarios / edge cases (e.g., a time-of-day greeting generator from several examples).

Sources:
- https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/2-prompt-engineering-foundations-best-practices

---

## obj-4-1-4 — 4.1.4 Apply best practices for prompt crafting

Advanced best practices (built on the 4 Ss):
- **Provide enough clarity** — be explicit; build on Single + Specific.
- **Provide enough context with details** — follow "Surround"; add descriptive comments, keep related
  files open; more contextual info = more fitting suggestions.
- **Provide examples for learning** — examples clarify requirements/expectations, help Copilot learn
  patterns quickly, fewer revision cycles; great for boilerplate, test templates, repetitive code.
- **Assert and iterate** — first output may not be production-ready; don't restart from scratch.
  Erase the suggestion, enrich the comment with more detail/examples, and prompt again — each
  iteration builds on Copilot's understanding.
- **Role prompting** — instruct Copilot to "Act as a …" (security expert, performance optimization
  expert, testing specialist) to get more targeted, domain-aware code on the first try.

Sources:
- https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/2-prompt-engineering-foundations-best-practices

---

## obj-4-2-1 — 4.2.1 Explain prompt engineering principles

- Core principles summed up as the **4 Ss**:
  - **Single** — focus each prompt on a single, well-defined task or question.
  - **Specific** — make instructions explicit and detailed; specificity → more precise suggestions.
  - **Short** — keep prompts concise; balances clarity without overloading Copilot.
  - **Surround** — use descriptive filenames and keep related files open for richer context.
- These principles are the basis of the advanced best practices (clarity, context, examples, iterate).

Sources:
- https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/2-prompt-engineering-foundations-best-practices

---

## obj-4-2-2 — 4.2.2 Describe prompt process flow and chat history usage

**Prompt process flow** (inbound → outbound):
- Inbound:
  1. **Secure prompt transmission + context gathering** — prompt sent over **HTTPS**; Copilot gathers
     context (code before/after cursor, filename/type, adjacent open tabs, project structure/paths,
     languages/frameworks) and applies **FIM**.
  2. **Proxy filter** — prompt passes to a **proxy server in a GitHub-owned Microsoft Azure tenant**;
     blocks prompt-hacking / attempts to reveal how the model works.
  3. **Toxicity filtering** — content filtering removes hate speech/inappropriate content and personal
     data before intent extraction / code generation.
  4. **Code generation with LLM** — the filtered prompt goes to the LLM, which produces suggestions.
- Outbound:
  5. **Post-processing and response validation** — toxicity filter + proxy apply final checks: code
     quality (e.g., XSS, SQL injection), and an **optional matching-public-code filter** (admins can
     block suggestions over ~150 characters that closely match public code). Failing content is
     truncated or discarded.
  6. **Suggestion delivery + feedback loop** — only responses passing all filters are delivered;
     Copilot learns from acceptances, modifications, and rejections.
  7. **Repeat** for subsequent prompts.

**Chat history usage:**
- In extended Chat conversations, each turn builds on prior context (e.g., create function → add error
  handling → add tests → add docs → optimize). The full history grows longer over time.
- **Cost:** long prompts carrying full conversation history can consume **2–3 PRUs per turn**;
  summarizing context or resetting the conversation can keep it closer to **1 PRU per request**.
- Manage efficiently: **summarize context** when conversations get lengthy; **reset and provide
  focused context** for new features (start fresh); use **concise references** to previous work
  instead of repeating full implementations.

Sources:
- https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/3-github-copilot-user-prompt-process-flow
- https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/2-prompt-engineering-foundations-best-practices
