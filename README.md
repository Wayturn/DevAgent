# Dev Agent CLI

Dev Agent CLI is a lightweight harness-style AI developer tool.

Its MVP goal is simple:

- Accept a command from CLI
- Read local files as tool inputs
- Build a task-specific prompt
- Let the orchestrator control the flow
- Call the LLM and return a structured result

## Why this structure

This project is intentionally not a direct "prompt in, answer out" chatbot.
It models a controllable agent harness:

`CLI -> Orchestrator -> Tools -> LLM -> Output`

That makes it easier to explain in interviews:

- `CLI` is the entrypoint for developer intent.
- `Orchestrator` controls the execution steps.
- `Tools` provide bounded capabilities like file read/write.
- `Prompt layer` keeps command behavior explicit and maintainable.
- `LLM client` is isolated, so the rest of the app is not coupled to one vendor.

## MVP commands

- `explain`: explain a target file in practical engineering language
- `fix`: suggest a fix plan and code patch direction for a target file
- `gen-api`: generate API design from a requirement or source file

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

Set environment variables:

```bash
set OPENAI_API_KEY=your_key
set OPENAI_MODEL=gpt-4.1-mini
```

`OPENAI_MODEL` is optional. If omitted, the app uses `gpt-4.1-mini`.

## Usage

```bash
dev-agent explain .\sample.py --trace
dev-agent fix .\service.py --goal "Reduce duplicated validation logic"
dev-agent gen-api .\requirements.txt --goal "Design a task management API"
```

Optional output file:

```bash
dev-agent explain .\sample.py --output .\out\explain.md
```

## Project structure

```text
src/dev_agent_cli/
  main.py
  cli.py
  config.py
  models.py
  prompts.py
  tools.py
  llm.py
  orchestrator.py
tests/
```

## Next step ideas

- Add real patch application flow for `fix`
- Add directory-level analysis
- Add tool loop with explicit action selection
- Add JSON output mode for editor integration
