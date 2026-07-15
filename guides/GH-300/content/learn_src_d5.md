# Domain 5 — Improve developer productivity with GitHub Copilot — CLEAN-ROOM SOURCE PACK

All facts below are paraphrased from **public Microsoft Learn** training (learn.microsoft.com).
Every citation URL is a learn.microsoft.com URL. No docs.github.com, blogs, or decks were used.

## Source modules (learn.microsoft.com)
- Developer use cases for AI with GitHub Copilot — `/training/modules/developer-use-cases-for-ai-with-github-copilot/`
- Develop unit tests using GitHub Copilot tools — `/training/modules/develop-unit-tests-using-github-copilot-tools/`

---

## 5.1.1 Use Copilot for code generation, refactoring, and documentation
Source: "Boost developer productivity with AI" and "AI in the SDLC" units.
- **Automating the boring stuff** — Copilot handles routine coding tasks so developers focus on complex/creative
  work: boilerplate code generation (e.g., scaffolding a REST API or class structure), sample data creation for
  testing, writing unit tests, and **code translation and refactoring** (suggesting improved patterns / more efficient
  implementations, and even converting between programming languages).
- **Refactoring** — Copilot assists refactoring by suggesting cleaner patterns, more efficient implementations, and
  cross-language translation. In the SDLC "Maintenance & support" phase it proposes improvements to existing code to
  keep a codebase modern and efficient.
- **Documentation writing** — Copilot improves writing/maintaining docs via: inline comments explaining complex code;
  function descriptions (parameters + return values); README generation (structure/content from the codebase); and
  documentation consistency across a project. It can also keep comments/docs in sync with code changes.
- **Personalized code completion** — Copilot adapts to individual coding style and project context over time; it learns
  from patterns and preferences and tailors suggestions accordingly.
- **SDLC coverage** — Requirement analysis (rapid prototyping, turning user stories into initial function/class defs,
  API design); Design & development (boilerplate, design-pattern implementation, code optimization, cross-language
  translation); Deployment (config files, deploy scripts, doc updates); Maintenance (bug-fix suggestions, refactoring,
  legacy understanding).
- **Always review**: generated code can contain bugs or miss requirements — human review is required.
- Diagram: productivity-sdlc.
- Cite: developer-use-cases-for-ai-with-github-copilot/2-boost-developer-productivity;
  developer-use-cases-for-ai-with-github-copilot/4-ai-software-development-lifecycle.

## 5.1.2 Accelerate learning and reduce context switching
Source: "Boost developer productivity with AI" unit.
- **Accelerate learning new languages/frameworks** — Copilot bridges learning and implementation via: context-aware
  code suggestions that illustrate unfamiliar functions/libraries; broad language support (helps transition between
  languages); documentation integration (inline suggestions on API usage and function parameters reduce trips to
  external docs). Example: working in an unfamiliar language (Golang), Copilot generates the code and the **"Explain
  this"** context-menu option explains what it does.
- **Minimizing context switching** — context switching drains productivity; Copilot keeps focus by giving relevant
  suggestions in the current context: **in-editor assistance** (suggestions in the IDE reduce online searches);
  **quick references** (correct method calls/parameters for APIs & libraries without leaving the editor);
  **code completion** (autocompletes repetitive patterns so you keep your train of thought).
- Net effect: less time on routine tasks, faster learning of new tech, better focus throughout the day.
- Diagram: (reuse productivity-sdlc only if helpful — but per outline, diagrams limited; use none here to avoid reuse).
- Cite: developer-use-cases-for-ai-with-github-copilot/2-boost-developer-productivity.

## 5.1.3 Generate sample data and modernize legacy code
Source: "Boost developer productivity with AI" + "AI in the SDLC" units.
- **Sample data / test data** — under "Automating the boring stuff," Copilot creates realistic **sample data** for
  testing, saving manual data-entry time. In the SDLC "Testing & QA" phase it does **test data generation** (realistic
  test data sets).
- **Modernize legacy code** — in "Maintenance & support," Copilot helps developers **understand and work with
  unfamiliar or legacy code** by providing explanations and **modern equivalents**; it suggests refactoring to keep the
  codebase modern/efficient, and can perform cross-language translation to migrate older code.
- **Boilerplate & scaffolding** for modernization: generate class structures, ORM/DB models, migration files, config
  files for different environments, and project scaffolding from descriptive comments.
- **Always review** generated data and modernized code before use.
- Cite: developer-use-cases-for-ai-with-github-copilot/2-boost-developer-productivity;
  developer-use-cases-for-ai-with-github-copilot/4-ai-software-development-lifecycle.

## 5.2.1 Generate unit and integration tests
Source: "Develop unit tests using GitHub Copilot tools" module (Chat view + Plan/Agent units).
- **Chat view** is the primary place to generate tests in VS Code. Open with **Ctrl+Alt+I** (Win/Linux) /
  **Cmd+Alt+I** (macOS), or the Copilot icon → Toggle Chat. Three per-prompt choices: **Agent Target** (Local),
  **Agent** (Ask / Plan / Agent), **Permission level** (Default Approvals / Bypass Approvals / Autopilot).
  Recommended start for test generation: **Agent** with **Default Approvals** (keeps you confirming each tool call).
- **/setupTests** — recommends and configures a test framework; in Agent mode it can install packages and scaffold the
  test project. Useful for new/onboarding projects.
- **/tests** — generates unit tests for the code active in the editor; Copilot detects the existing framework & style
  and writes tests into an appropriate test file (appends to an existing test file or creates a new one). Works for a
  whole file or a selected method/block. Diff appears in editor; choose **Keep** or **Undo**.
- **Natural-language prompts** work too, e.g. "Generate xUnit tests… add them to the Calculator.Tests project" or
  **"Create integration tests for the data access layer in this module."** You can tell the Agent to **run** the tests
  after writing them so it catches obvious failures.
- **Context matters**: Add Context button; drag-and-drop files/tabs; **#** mentions (`#selection`, `#editor`,
  `#codebase`); attaching external markdown (test conventions) shapes output.
- **Ask / Plan / Agent** agents: Ask = read-only analysis/Q&A (explore cases before writing); Plan = structured
  step-by-step implementation plan you review before code; Agent = autonomous multi-file generate/run/iterate.
- **Custom instructions** — a `*.instructions.md` file with an `applyTo` field (e.g., `applyTo: tests/**`) enforces
  frameworks (xUnit vs NUnit), naming conventions, Arrange-Act-Assert structure, parameterized tests; share in source
  control for team consistency.
- **Important**: generated tests may not cover every scenario — **manual review and code review are still required**.
  Agent runs can consume multiple **premium requests**.
- Diagram: test-generation-flow.
- Cite: develop-unit-tests-using-github-copilot-tools/3-generate-unit-tests-chat-view;
  develop-unit-tests-using-github-copilot-tools/4-plan-automate-tests-using-agents.

## 5.2.2 Identify edge cases and write assertions
Source: "Develop unit tests…" (Chat view + ghost text) and "AI in the SDLC" (Testing & QA).
- **Ask mode** to explore before writing: attach the file/selection (`#selection`) and ask e.g. "What edge cases
  should I cover when testing the CalculateDiscount method? List the scenarios and explain why each matters." Then
  switch to Agent to generate the tests.
- **Prompt for edge cases** directly: "/tests Generate unit tests for the methods in this file. Include success,
  failure, and **edge cases**." or "…including edge cases for **negative values and zero**."
- **Assertion suggestions** — in the SDLC Testing & QA phase Copilot proposes **appropriate assertions** based on the
  expected behavior of the code under test, and suggests test scenarios covering **edge cases** to improve robustness.
- **Ghost text** to extend coverage: with 1–2 existing test cases, put the cursor after the last test and type a new
  method or a descriptive comment (e.g., `// Test that ProcessOrder throws when the order total is negative`); Copilot
  completes the case from existing patterns/imports. **Tab** accepts, **Esc** dismisses. Best when the file already
  shows the pattern (Arrange-Act-Assert / parameterized attribute) and the method is imported.
- **Boundary conditions** — Plan agent prompt example: "Include tests for success, failure, and **boundary
  conditions**." Parameterized tests are good for boundary values.
- **Review**: still confirm the generated assertions actually reflect intended behavior.
- Cite: develop-unit-tests-using-github-copilot-tools/3-generate-unit-tests-chat-view;
  develop-unit-tests-using-github-copilot-tools/5-extend-fix-tests-using-github-copilot.

## 5.2.3 Suggest security improvements and performance optimizations
Source: "Understand limitations and measure impact" + "AI in the SDLC" + "Boost productivity" units.
- **Performance / code optimization** — in Design & development, Copilot offers **more efficient code alternatives**
  ("code optimization") so you write performant code from the start; SDLC Testing & QA can generate **performance
  benchmarks and load-testing scenarios**; refactoring suggestions improve efficiency.
- **Security assistance** — Copilot can be used for **pre-submission quality checks** to identify potential issues and
  suggest improvements before a PR; orchestrated "review agent" patterns identify **security vulnerabilities** and
  **performance optimization** opportunities and check architectural/pattern compliance.
- **Fix failing tests** — Test Explorer **Fix Test Failure** (sparkle icon) attaches the failing test + output and
  proposes a fix (to test, app code, or both); **/fixTestFailure** in Chat does the same with extra context; the Agent
  can monitor test output and auto-fix + rerun until green.
- **Critical limitation** — generated code **may not follow security best practices** and must be reviewed carefully;
  Copilot can suggest buggy code, misread context, vary by language/framework, and reflect training-data bias. Human
  review is essential for security- and performance-sensitive code. Never blindly trust suggestions.
- Cite: developer-use-cases-for-ai-with-github-copilot/5-understand-limitations-measure-impact;
  developer-use-cases-for-ai-with-github-copilot/4-ai-software-development-lifecycle;
  develop-unit-tests-using-github-copilot-tools/5-extend-fix-tests-using-github-copilot.

---

## Real learn.microsoft.com URLs cited in domain5.html
- https://learn.microsoft.com/en-us/training/modules/developer-use-cases-for-ai-with-github-copilot/2-boost-developer-productivity
- https://learn.microsoft.com/en-us/training/modules/developer-use-cases-for-ai-with-github-copilot/4-ai-software-development-lifecycle
- https://learn.microsoft.com/en-us/training/modules/developer-use-cases-for-ai-with-github-copilot/5-understand-limitations-measure-impact
- https://learn.microsoft.com/en-us/training/modules/develop-unit-tests-using-github-copilot-tools/3-generate-unit-tests-chat-view
- https://learn.microsoft.com/en-us/training/modules/develop-unit-tests-using-github-copilot-tools/4-plan-automate-tests-using-agents
- https://learn.microsoft.com/en-us/training/modules/develop-unit-tests-using-github-copilot-tools/5-extend-fix-tests-using-github-copilot
