# Spec-Driven Test Cases

This repository explores two different approaches to **spec-driven development** — a workflow where you define expected behavior _before_ writing code, so requirements, tests, and implementation stay in sync.

Each approach is demonstrated with a working Todo app and lives in its own sub-folder.

---

## Approaches

### 1. Kiro — [`kiro/`](./kiro)

Kiro is an AI-powered IDE that formalizes spec-driven development through a built-in spec workflow. A feature spec lives in `.kiro/specs/<feature>/` and is made up of three cascading documents:

| Document | Purpose |
|---|---|
| `requirements.md` | User stories and acceptance criteria in plain language |
| `design.md` | Architecture, data models, API contracts, and formal correctness properties |
| `tasks.md` | Ordered, checkable implementation steps that reference requirements |

**How it works:**
1. Write requirements as numbered user stories.
2. Kiro (or you) produces a design doc that turns requirements into verifiable properties.
3. Those properties map 1-to-1 to tests.
4. Tasks break the design into an implementation checklist.

Kiro also uses **steering files** (`.kiro/steering/`) — always-on context files that keep the AI grounded in your stack choices, project structure, and product goals across every interaction.

The result is full traceability: **user story → design property → test → code**.

---

### 2. OpenSpec — [`openspec/`](./openspec)

OpenSpec is a lightweight, tool-agnostic approach where you write a plain-language spec first, derive tests from it manually, and then implement only what the tests require.

**How it works:**
1. **Spec first** — describe features in `specs/` using Given/When/Then scenarios.
2. **Tests from spec** — write tests that map directly to each scenario before (or alongside) writing code.
3. **Minimal implementation** — implement only what is needed to make the tests pass.
4. **Edge cases at every layer** — cover both domain logic and UI/HTTP behavior.
5. **Validate frequently** — run the test suite continuously as you iterate.

The key idea: **spec defines intent, tests enforce intent, code fulfills intent**.

---

## Comparison

| | Kiro | OpenSpec |
|---|---|---|
| **Tooling** | Kiro IDE (AI-assisted) | Any editor / framework |
| **Spec format** | Structured markdown (requirements → design → tasks) | Free-form Given/When/Then scenarios |
| **Test generation** | Guided by formal correctness properties in the design doc | Manual mapping from spec scenarios |
| **AI involvement** | Built-in — Kiro generates and refines the spec | Optional |
| **Traceability** | Explicit requirement IDs tracked across all documents | Scenario names mirrored in test names |
| **Best for** | Teams wanting structured, AI-assisted spec workflows | Teams preferring a simple, lightweight spec-first habit |

Both approaches share the same core value: **write down what the system should do before writing the code that does it**, making requirements reviewable, tests meaningful, and regressions easy to catch.
