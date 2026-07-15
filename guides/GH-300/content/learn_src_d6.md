# Domain 6 — Research notes (clean-room, learn.microsoft.com only)

Configure privacy, content exclusions, and safeguards (10–15%). Notes are organized by
objective id. Every fact below is paraphrased from the public Microsoft Learn pages listed
under each objective's **Sources:**.

---

## obj-6-1-1 — Configure content exclusions and editor settings

- Content exclusions let admins prevent specific files, directories, or repositories from
  being used to inform code-completion suggestions. Purpose: protect sensitive information.
- **Where you configure it (settings only — not per-user in the editor):**
  - **Repository level:** repo main page → **Settings** → (Code & automation) **Copilot** →
    **Repositories and paths to exclude** → specify files/directories.
  - **Organization level:** profile photo → **Your organizations** → org **Settings** →
    **Copilot > Content exclusion** → enter files or repositories to exclude.
- You can specify content exclusions **only** in organization or repository settings.
- Exclusions defined in an org/repo within an enterprise apply to all members licensed under
  **GitHub Copilot Business** or **GitHub Copilot Enterprise**. (Content exclusions are a
  Business/Enterprise capability — not available on Free/Pro/Pro+.)
- **What excluding content does:**
  - Code completion is no longer available in the affected files.
  - Content in affected files won't inform code-completion suggestions in **other** files.
  - Content in affected files won't inform GitHub Copilot **Chat** responses.
- Trade-off: excluding files can produce more secure/compliant suggestions but reduces the
  context available to Copilot, which can lower accuracy/usefulness (e.g., excluding a
  critical config file may block relevant dependent snippets). Choose exclusions carefully.
- **Limitations (not always fully effective):**
  - **IDE limitations:** in some IDEs, exclusions may not apply to certain features such as
    Copilot Chat. In VS Code and Visual Studio, exclusions are **not** applied when you use
    the `@github` chat participant.
  - **Semantic information:** Copilot may still use semantic info from an excluded file if the
    IDE surfaces it in a non-excluded file — e.g., type information and hover-over definitions
    for symbols/function calls.
  - **Policy scope:** settings apply only to members of the org where the exclusion is
    configured; anyone else with access to the files can still get completions/Chat responses.
- Editor settings context: Copilot is enabled/disabled in the IDE; the Copilot status-bar icon
  reflects state and shows when an exclusion applies to the current file (see 6.2.2).

Sources:
- https://learn.microsoft.com/en-us/training/modules/github-copilot-management-and-customizations/4-manage-content-exclusions
- https://learn.microsoft.com/en-us/training/modules/github-copilot-management-and-customizations/

---

## obj-6-1-2 — Describe ownership and limitations of outputs

- Copilot is a generative-AI assistant; outputs must be validated. AI can produce
  hard-to-interpret decisions and unintended/harmful outcomes (bias, privacy issues), so
  **human oversight**, transparency, and accountability are essential — the developer remains
  responsible for reviewing and validating what Copilot generates before accepting it.
- **Contractual protections** available to organizations:
  - **IP indemnity** — included with **Business** and **Enterprise** plans. If a Copilot
    suggestion is challenged as infringing third-party IP, GitHub assumes legal
    responsibility. **Condition:** the **Matching public code** setting must be set to
    **Block** for GitHub to assume that responsibility.
  - **Data Protection Agreement (DPA)** — outlines data-protection measures / privacy
    compliance.
  - **GitHub Copilot Trust Center** — details on security, privacy, compliance, and IP
    safeguards.
- Plan-tier notes (management/policy features):
  - Public code filter: available on Free, Pro/Pro+, Business, Enterprise.
  - Content exclusions, IP indemnity, enterprise-grade security, "data excluded from training
    by default," user management, usage metrics, SAML SSO: **Business & Enterprise** only.
  - Individual subscribers can choose whether GitHub collects and retains their prompts and
    Copilot suggestions.
- Takeaway for ownership: you own/are responsible for the code you accept and commit;
  Business/Enterprise add contractual/legal protection (indemnity) but do not remove the need
  to review, test, and validate.

Sources:
- https://learn.microsoft.com/en-us/training/modules/github-copilot-management-and-customizations/3-github-copilot-contractual-protections-disabling-matching-public-code
- https://learn.microsoft.com/en-us/training/modules/github-copilot-management-and-customizations/2-explore-github-copilot-plans-associated-management-customization-features
- https://learn.microsoft.com/en-us/training/modules/responsible-ai-with-github-copilot/2-manage-ai-risks

---

## obj-6-2-1 — Enable suggestions matching public code filtering

- The "suggestions matching public code" (duplication-detection) filter identifies and filters
  out code suggestions that match publicly available code on GitHub. Goal: maintain
  originality/security of the codebase and reduce risk of nonsecure/noncompliant code.
- Two options: **Allow** or **Block** matching suggestions. The proxy's duplication filter
  targets longer look-alikes — suggestions of roughly **150+ characters** that closely match
  public code (well-known product behavior; the filter blocks/truncates such matches).
- **Who controls it (key distinctions):**
  - **Organization (Business/Enterprise):** org admins can block suggestions matching public
    code for **all members**. Blocking is **required to activate IP indemnity**.
  - **Personal account (Free/Pro/Pro+), individually paid:** the user fully controls the
    Allow/Block toggle in their account under **Copilot → Features → Privacy**.
  - **Personal account, org-provided seat:** the toggle may be **locked** and reflects the
    organization's policy.
- **Org admin steps:** profile → **Your enterprises/Your organizations** → **Settings** →
  (Code, planning, and automation) **Copilot** → **Features** → **Privacy** section →
  **Suggestions matching public code** → choose **Block** → **Save**.
- **Personal steps:** profile → **Settings** → **Copilot** → **Features** → **Privacy** →
  **Suggestions matching public code** → toggle **Allow**/**Block** (takes effect immediately
  in your personal environment).

Sources:
- https://learn.microsoft.com/en-us/training/modules/github-copilot-management-and-customizations/3-github-copilot-contractual-protections-disabling-matching-public-code
- https://learn.microsoft.com/en-us/training/modules/github-copilot-management-and-customizations/2-explore-github-copilot-plans-associated-management-customization-features

---

## obj-6-2-2 — Resolve issues with suggestions and content exclusions

- **Code suggestions are missing** — troubleshooting actions:
  - Check your **internet connection** (Copilot needs an active connection).
  - **Update the Copilot extension** to the latest version (older versions may not
    communicate with Copilot servers).
  - **Verify IDE compatibility** (some IDEs need specific config/updates).
  - **Review content exclusions** — excluded files won't show suggestions; confirm settings.
- **Content exclusions aren't working as expected:**
  - **Delayed application:** after adding/changing exclusions, changes can take **up to 30
    minutes** to take effect in IDEs where settings are already loaded; **reload** the content
    exclusion settings in the IDE to apply immediately.
  - **Inadequate scope:** exclusions apply only to members of the org where configured —
    ensure all relevant team members have the settings. Check the **Copilot status-bar icon**:
    if an exclusion applies to the file, the icon has a **diagonal line** through it; hover to
    see whether an org or the parent repository disabled Copilot for that file.
  - **IDE-specific limitations:** in some IDEs, exclusions don't apply to certain features such
    as Copilot Chat — adjust workflow accordingly.
- **Code suggestions are unsatisfactory** — improve quality by: providing clear context
  (descriptive comments, meaningful names), using Copilot commands (e.g., Ctrl+Enter in VS
  Code to trigger Copilot), and adjusting prompt length/detail.

Sources:
- https://learn.microsoft.com/en-us/training/modules/github-copilot-management-and-customizations/5-troubleshoot-common-issues-with-github-copilot
- https://learn.microsoft.com/en-us/training/modules/github-copilot-management-and-customizations/4-manage-content-exclusions
