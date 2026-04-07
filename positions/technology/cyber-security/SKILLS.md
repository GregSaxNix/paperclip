# SKILLS — CyberSecurity (Sentry)

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync CyberSecurity`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control, access to all Paperclip API tools
- skill-discovery — Identify and request new capabilities

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills._

- [x] `pdf` — Read CVE reports, security advisories, compliance documents
- [x] `webapp-testing` — Security-focused application and API testing

## Security Skills (installed from community)
_Installed from vetted community repos._

- [x] `bug-hunt-swarm` (dimillian/skills) — Coordinated multi-agent vulnerability discovery
- [x] `qa-patrol` (tahseen137/qa-patrol) — Security-aware QA and code review
- [x] `github` (dimillian/skills) — Code review, dependency scanning, commit history analysis

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only. Pending configuration._

- [ ] **GitHub MCP (claude_local only)** — Deep code scanning, PR security review, repository access
- [ ] **Sequential Thinking MCP (claude_local only)** — Structured threat modelling across complex attack trees

## Custom Build Skills (pending)
_These skills do not exist publicly in the right form. Build progressively as needed._

- [ ] `owasp-llm-security-guide` — OWASP LLM Top 10 checklist, prompt injection patterns, jailbreak taxonomy, mitigation strategies specific to LLM agent systems
- [ ] `paperclip-security-audit` — Audit framework specific to Paperclip: agent permission checks, secret hygiene validation, plugin manifest review, adapter config scanning
- [ ] `dependency-cve-checker` — Structured workflow for npm/pnpm/pip dependency audits against CVE databases, with severity classification and fix recommendations
