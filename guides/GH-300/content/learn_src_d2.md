# Domain 2 — Use GitHub Copilot features — CLEAN-ROOM SOURCE PACK

All facts below are paraphrased from **public Microsoft Learn** training (learn.microsoft.com).
Every citation URL is a learn.microsoft.com URL. No docs.github.com, blogs, or decks were used.

## Source modules (learn.microsoft.com)
- Introduction to GitHub Copilot — `/training/modules/introduction-to-github-copilot/`
- GitHub Copilot Across Environments — `/training/modules/github-copilot-across-environments/`
- Management and customization considerations — `/training/modules/github-copilot-management-and-customizations/`
- Building applications with GitHub Copilot agent mode — `/training/modules/github-copilot-agent-mode/`
- Accelerate development with GitHub Copilot Cloud Agent — `/training/modules/github-copilot-code-agent/`
- Introduction to MCP Server — `/training/modules/mcp-server/`
- Leveling up code reviews and pull requests with GitHub Copilot — `/training/modules/code-reviews-pull-requests-github-copilot/`
- Introduction to Copilot Spaces — `/training/modules/introduction-copilot-spaces/`
- Using advanced GitHub Copilot features — `/training/modules/advanced-github-copilot/`

---

## 2.1.1 Enable Copilot in the IDE
- Sign in with a GitHub account that has Copilot access. On GitHub: profile > **Settings**; Copilot is under
  **Code, planning, and automation**.
- Supported environments: **GitHub.com (no extension needed)**, **VS Code**, **Visual Studio**, **JetBrains IDEs**,
  **Neovim**.
- VS Code: install the **GitHub Copilot** extension from the Marketplace, then **Sign in to GitHub**.
- Enable/disable via the **status icon** in the bottom pane; can disable **globally** or **per language**.
- Inline suggestions: **Settings > Extensions > GitHub Copilot > Editor: Enable Auto Completions** (per language too).
- Free tier: **2,000 code completions + 50 chat messages / month**. Educators, students, select OSS maintainers can get
  **Copilot Pro** free.
- Troubleshoot in VS Code: **Developer: Open Log File** / **Open Extensions Logs Folder**; **GitHub Copilot: Collect
  Diagnostics**; **Help > Toggle Developer Tools** for Electron logs. Firewalls/proxies can block Copilot.
- Surfaces (diagram copilot-surfaces): IDE, GitHub.com, CLI, GitHub Mobile.
- Cite: introduction-to-github-copilot/4-setup-configure-troubleshoot; across-environments/2-code-completion.

## 2.1.2 Trigger modes: inline, chat, CLI, agent mode
- **Inline suggestions**: ghost text; accept **Tab** or **→**; reject **Esc** or keep typing.
- **Multiple suggestions**: light bulb / **Alt+]** (next), **Alt+[** (prev) (Option on macOS).
- **Command palette**: Ctrl+Shift+P / Cmd+Shift+P — e.g., **Explain This**, **Generate Unit Tests**.
- **Copilot Chat**: dedicated panel, natural language, project-aware.
- **Inline chat**: **Ctrl+I / Cmd+I**; slash commands `/explain`, `/suggest`, `/tests`, `/comment`.
- **Comments to code**: describe intent in a comment; Enter generates code.
- **Copilot Edits**: multi-file changes toward a goal.
- **Agent Mode**: autonomous, iterative; determines files/deps, runs terminal commands, self-heals.
- **Copilot CLI**: brings Copilot to the terminal.
- Diagram: interaction-modes.
- Cite: introduction-to-github-copilot/3-interacting-with-copilot; agent-mode/2-what-is-agent-mode.

## 2.1.3 Content exclusions
- Configured at **repository** (repo Settings > Copilot > *Repositories and paths to exclude*) and **organization**
  (org Settings > Copilot > *Content exclusion*).
- Effects: no **code completion** in excluded files; excluded content won't inform **completions elsewhere** or
  **Chat responses**.
- **Only** on **Business/Enterprise** (Free/Pro have no content exclusions). Settings apply to Business/Enterprise members.
- Limitations: **IDE limits** — not applied to the **@github** chat participant in VS Code/Visual Studio; **semantic
  info** (type info, hover defs) may still surface from non-excluded files; **policy scope** only covers org members.
- Cite: management-and-customizations/4-manage-content-exclusions.

## 2.2.1 Define CLI / benefits
- GitHub Copilot CLI brings Copilot to the **terminal**: explain commands, **suggest** shell commands from natural
  language, work interactively/safely with files. Uses **GitHub authentication**; runs **independently from GitHub CLI**
  but reuses existing credentials. Reduces guesswork, speeds everyday workflows.
- Cite: across-environments/5-git-hub-copilot-for-the-command-line.

## 2.2.2 Install steps
- Homebrew (macOS/Linux): `brew install copilot-cli`. Or script: `curl -fsSL https://gh.io/copilot-install | bash`.
- Launch interactive: `copilot`. First launch **asks to trust the files** in the current folder (Copilot may read/modify/
  execute files there).
- One-shot: `copilot -i "explain brew install git"`.
- Cite: across-environments/5-git-hub-copilot-for-the-command-line.

## 2.2.3 Features & commands
- Slash commands (explicit session control, **cannot** be replaced by natural language): `/help`, `/explain <cmd>`,
  `/suggest <task>`, `/revise`, `/feedback`, `/exit`, `/model <model>`, `/theme`, `/skills`, `/mcp`, `/list-dirs`,
  `/reset-allowed-tools`, `/sandbox`.
- Natural language works for explain/suggest/revise.
- Cite: across-environments/5-git-hub-copilot-for-the-command-line.

## 2.2.4 Interactive & sessions
- Interactive mode (`copilot`) vs one-shot (`copilot -i "…"`). Use `@` to select a file as context.
- **Local sandboxing**: `/sandbox enable` — restricts filesystem/network/OS access on your machine.
- **Cloud sandboxing**: `copilot --cloud` — fully isolated GitHub-hosted Linux env (built on **Azure Container Apps
  Sandboxes**). Sessions: **Active / Stopped / Deleted**; stopped sessions snapshot state; **resume across devices**.
  Org/enterprise admins must enable the **Cloud Sandbox** policy.
- Diagram: copilot-cli-flow.
- Cite: across-environments/5-git-hub-copilot-for-the-command-line.

## 2.2.5 Scripts & file management
- Config via permission prompts, flags, local config files: **trusted directories**, **tool permissions**
  (`--allow-tool` / `--deny-tool`), **path permissions**, **URL permissions**.
- Suggests commands from NL, revise with follow-ups; combine with **gh** CLI; **always review before execution**.
- Cite: across-environments/5-git-hub-copilot-for-the-command-line.

## 2.3.1 Agent Mode, Copilot Edits, MCP, Agent Sessions & Sub-Agents
- Engagement ladder: inline suggestions → Chat → **Copilot Edits** (multi-file) → **Agent Mode** (autonomous, iterative).
- Agent Mode: analyzes the whole workspace, determines relevant files/dependencies, executes edits, runs terminal
  commands (build/install/test), **self-heals** (detects errors, corrects, re-runs), keeps the developer in control
  (review/revert). Limits: specialized domain logic, missing/poorly documented context.
- PRUs: each handoff ≈ 1 PRU; premium reasoning ≈ doubles consumption (~4+ vs ~2).
- **MCP** (Model Context Protocol): open standard, "USB-C for AI tools"; connects models to external tools/data.
  **GitHub MCP Server** hosted at `https://api.githubcopilot.com/mcp/`; add via **MCP: Add server > HTTP > URL > OAuth**;
  **PAT** alternative (repo + read:packages); optional local Docker `ghcr.io/github/github-mcp-server`. 30+ tools.
  Combining MCP + Agent mode → agentic loops (explore, adapt, refine).
- **Copilot Cloud Agent** (Agent Sessions / delegating to background "sub-agents"): autonomous teammate inside GitHub.
  Assign an issue → **👀** reaction → `copilot/` branch → **draft PR** → **agent session** in a GitHub Actions env →
  commits → **"Copilot finished work"** → requests review. Track from the **Agents** page / **session logs**; iterate
  by mentioning **@copilot** in a PR comment (write permission required). Draft PRs need **human approval**; the author
  can't approve their own; Actions need **Approve and run workflows**; sessions time out after **1 hour**.
  Plans: **Pro/Pro+/Business/Enterprise**. Uses **Actions minutes + PRUs**. Customize env via
  `.github/workflows/copilot-setup-steps.yml`; extend with **MCP tools only** (no remote OAuth); defaults include
  **GitHub MCP** + **Playwright MCP**.
- Distinction: **Cloud agent** (runs in GitHub Actions) vs **Agent mode / Copilot Edits** (local IDE edits).
- Diagrams: agent-mode-loop, mcp-architecture.
- Cite: agent-mode/3-explore-the-power; mcp-server/3-configure-connect; code-agent/3-assign-track; code-agent/1-understand-enable.

## 2.3.2 Code review & coding assistance
- Copilot review features: **PR summaries**, **security fixes** (integrates with **Code Scanning**), line-by-line
  **explanations**, drafting **review comments**, reviews **in the IDE** before opening a PR.
- On GitHub.com: add **Copilot** in the **Reviewers** menu; review typically **< 30s**; comments land on lines.
  **Advisory only** — doesn't approve/reject and **doesn't count toward required approvals**.
- Customize with **.github/copilot-instructions.md** (repo-wide) and path-specific **.github/instructions/*.instructions.md**
  with an **applyTo** glob frontmatter.
- Automate at scale: **rulesets** (*Request pull request review from Copilot*) at repo/org; pair with **status checks**;
  account-level **Automatic Copilot code review** (Pro/Pro+); *Require conversation resolution before merging*.
- **PRUs** power deep, context-rich reviews of large diffs; budget/optimize them.
- Diagram: code-review-flow.
- Cite: code-reviews-pull-requests/2-github-copilot-review-process; /3-copilot-reviewer-github; /4-issues-early-automated-reviews-copilot.

## 2.3.3 Spaces, Spark, PR summaries, instructions files
- **Copilot Spaces**: reusable, scoped workspace. Create at **github.com/copilot/spaces**; owned by **you or an org**;
  add **Instructions** (free text) + **Attachments** (files/folders, linked issues/PRs, uploads, text). Always reference
  the **latest main branch**. **Inherit GitHub permissions** — a Space grants **no new access**. Governance: "one job per
  Space", assign an owner, naming conventions, review cadence.
- **PR summaries**: generate from the PR description editor via the **Copilot** icon (draft summary/outline); consume PRUs.
- **Instructions files**: repo-wide **.github/copilot-instructions.md**; path-specific **.instructions.md** with `applyTo`.
- **GitHub Spark**: build and deploy apps from natural-language descriptions (kept high-level; no non-Learn citation).
- Cite: introduction-copilot-spaces/2-create-first-space; /3-share-discover-govern; code-reviews-pull-requests/2.

## 2.3.4 Chat limits, options, feedback, commands, prompt files
- Surfaces: Chat panel + **inline chat** (Ctrl+I).
- **Scope references**: `#file:<name>`; participants **@terminal**, **@vscode**, **@github**.
- **Slash commands**: `/doc`, `/explain`, `/fix`, `/generate`, `/optimize`, `/tests`, `/new`.
- **Model selection**: standard (GPT-4o, ~1 PRU) vs premium reasoning (o1-preview/o1-mini, ~2 PRU).
- **Feedback**: thumbs up / thumbs down on suggestions.
- **Limits**: Free tier = 50 chat messages/month; content exclusions are **not** applied to the **@github** participant.
- **Prompt files / instructions**: custom prompt files guide behavior (e.g., with specific MCP servers) for consistency.
- Cite: across-environments/3-git-hub-copilot-chat; advanced-github-copilot module.

## 2.4.1 Org policy management + Code Review policies
- Plans: **Free**, **Pro/Pro+**, **Business**, **Enterprise**. Management policy features (✅ = Business/Enterprise):
  Public code filter (all), User management, Data excluded from training by default, Enterprise-grade security,
  IP indemnity, Content exclusions, SAML SSO, Usage metrics; **Require GitHub Enterprise Cloud** = Enterprise only.
- **Matching public code**: org admins (Business/Ent) at **Settings > Copilot > Features > Privacy > Suggestions matching
  public code > Block**; **required for IP indemnity**. Personal (Free/Pro/Pro+) can toggle Allow/Block; an org-provided
  seat may be **locked** to the org policy.
- **Code Review policies**: rulesets → *Request pull request review from Copilot* at repo/org, *Require a pull request
  before merging*, optional *Require conversation resolution*.
- **Policy layers** (diagram org-policy-layers): enterprise → organization → repository → personal. Diagram: copilot-plans.
- Cite: management-and-customizations/2-explore-github-copilot-plans; /3-contractual-protections; code-reviews-pull-requests/4.

## 2.4.2 Audit log events
- **Usage metrics** and audit/visibility are **Business/Enterprise** capabilities used for governance/compliance.
- Cloud Agent work is auditable: **session logs** + PR history give traceability of every commit/action.
- Frame audit log as monitoring Copilot activity (who used it, policy changes) for oversight. Keep to Learn-supported
  facts; don't invent event names.
- Cite: management-and-customizations/2-explore-github-copilot-plans; code-agent/3-assign-track.

## 2.4.3 Manage subscriptions using the REST API
- Seat/subscription management is a **Business/Enterprise admin** function (**User management** ✅ Business/Ent) in
  org Copilot settings.
- Programmatic management/automation: Learn demonstrates the GitHub **API/CLI** for Copilot workflows — assign issues to
  Copilot via **GraphQL** (`suggestedActors` with `CAN_BE_ASSIGNED`, `createIssue`, `replaceActorsForAssignable`) and the
  **gh** CLI (`gh issue edit`). Same API-driven approach underpins automating Copilot administration.
- Keep REST specifics general (don't fabricate endpoints); emphasize automation + admin scope.
- Cite: code-agent/3-assign-track-troubleshoot-copilot-code-agent-tasks; management-and-customizations/2-explore-github-copilot-plans.
