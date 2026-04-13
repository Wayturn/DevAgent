# Dev Agent CLI

## 中文說明

Dev Agent CLI 是一個輕量、可控的 AI 開發者工具，採用 harness-style agent 設計，而不是單純的聊天機器人。

這個專案的 MVP 目標很明確：

- 從 CLI 接收開發者指令
- 讀取本地檔案作為工具輸入
- 依照不同命令組裝 prompt
- 由 orchestrator 控制整體執行流程
- 呼叫 LLM 並輸出結構化結果

## 為什麼要用這種結構

這個專案刻意避免做成「prompt 丟進去，答案吐出來」的直接式工具，而是建成一個可控的 agent harness：

`CLI -> Orchestrator -> Tools -> LLM -> Output`

這種設計的好處，是比較接近真實 AI 應用工程場景，也更容易在面試或作品集裡解釋：

- `CLI`：接收使用者意圖，是系統入口
- `Orchestrator`：控制執行步驟與流程
- `Tools`：提供受控能力，例如檔案讀寫
- `Prompt layer`：將不同命令的行為明確抽象化
- `LLM client`：封裝模型 API，避免其他模組直接耦合供應商 SDK

## MVP 命令

- `explain`：用工程語言解釋目標檔案的用途與流程
- `fix`：分析問題並提供修正方向與範例
- `gen-api`：根據需求或既有內容產生 API 設計

## 安裝方式

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

設定環境變數：

```bash
set OPENAI_API_KEY=your_key
set OPENAI_MODEL=gpt-4.1-mini
```

`OPENAI_MODEL` 是選填，若未設定，預設使用 `gpt-4.1-mini`。

## 使用方式

```bash
dev-agent explain .\sample.py --trace
dev-agent fix .\service.py --goal "Reduce duplicated validation logic"
dev-agent gen-api .\requirements.txt --goal "Design a task management API"
```

也可以將結果輸出到檔案：

```bash
dev-agent explain .\sample.py --output .\out\explain.md
```

## 專案結構

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

## 下一步可擴充方向

- 為 `fix` 加入真正的 patch apply 流程
- 支援目錄層級分析，而不只是單檔
- 增加更明確的 tool loop 與 action selection
- 支援 JSON 輸出，方便未來整合 editor 或其他工具

---

## English Version

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
