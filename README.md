# Dev Agent CLI

## 中文說明

Dev Agent CLI 是一個輕量、可控的 AI 開發者工具，定位是 developer agent harness，而不是單純的 prompt wrapper 或聊天機器人。

這個專案的目標，不是做一個「把程式碼貼進去，讓模型隨便回答」的小工具，而是用最小可行架構，展示一個可解釋、可擴充、可觀測的 AI developer workflow。

### 專案亮點

- 使用明確的 command abstraction：`explain`、`fix`、`gen-api`
- 採用可控流程：`CLI -> Orchestrator -> Tools -> LLM -> Output`
- 保留 trace / telemetry，能看到 agent 在做什麼
- `fix` 輸出使用穩定 Markdown 結構，方便後續 parsing 或 UI 整合
- 支援安全的 repo-aware 能力，例如目錄摘要，而不是只看單一檔案

### 這個專案想解決什麼問題

很多 AI CLI demo 本質上只是：

`input file -> prompt -> model -> output`

這樣雖然能動，但很難稱作 agent harness，因為：

- 流程控制不明確
- 工具能力沒有被清楚邊界化
- 不容易觀察模型決策上下文
- 後續要加 tool loop 或 structured output 時容易越改越亂

Dev Agent CLI 的做法是保留 MVP 的簡潔度，但先把骨架立好，讓它更像真實 AI 應用系統。

### 架構流程

`CLI -> Orchestrator -> Tools -> LLM -> Output`

- `CLI`
  接收使用者命令與參數，是整個系統的入口。

- `Orchestrator`
  控制執行步驟，決定要先觀察什麼、用哪個 prompt、最後如何輸出結果。

- `Tools`
  提供受控能力，目前以檔案讀寫與目錄摘要為主，避免過早加入危險能力。

- `Prompt Layer`
  將不同 command 的行為抽象成明確模板，降低 prompt 分散在各處的問題。

- `LLM Client`
  封裝模型呼叫，讓 orchestrator 不直接依賴特定 API 細節。

### 目前支援的命令

- `explain`
  用工程語言解釋目標檔案的用途、流程與風險。

- `fix`
  針對目標檔案提出修正建議，並使用穩定結構輸出：
  - Problem Summary
  - Root Cause
  - Recommended Fix
  - Revised Code
  - Trade-offs / Notes

- `gen-api`
  根據需求或既有內容產生 API 設計。

### 為什麼這個專案比較像 agent harness

這一版雖然仍然是 MVP，但已經有幾個很重要的 agent 特徵：

- 有 orchestrator，而不是 CLI 直接呼叫模型
- 有工具層，而不是所有上下文都手動拼進 prompt
- 有 command-specific prompt template
- 有 trace / telemetry，可觀察執行過程
- 有輕量 repo context，不再只是單檔 prompt wrapper

這讓它很適合作為：

- AI Application Engineer 作品集專案
- agent harness 入門實作
- 未來往 patch apply、tool loop、editor integration 擴充的基礎

### 安裝方式

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

`OPENAI_MODEL` 是選填，若未設定則預設使用 `gpt-4.1-mini`。

### 使用方式

```bash
dev-agent explain .\sample_input.py --trace
dev-agent fix .\sample_input.py --goal "Reduce duplicated validation logic"
dev-agent gen-api .\requirements.txt --goal "Design a task management API"
```

輸出到檔案：

```bash
dev-agent explain .\sample_input.py --output .\out\explain.md
```

### Trace / Telemetry 範例

開啟 `--trace` 後，可以看到類似以下資訊：

- 讀取了哪個檔案
- 使用了哪個 command template
- 檔案副檔名與目錄摘要
- 使用了哪個 model
- input / prompt / output 大小
- 是否有 write-back

這些資訊的目的不是炫技，而是讓 agent workflow 更可觀測、更容易 debug。

### 專案結構

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

### 適合展示的技術重點

如果你要把這個專案放進履歷或面試說明，這幾點最值得講：

- 如何把 LLM 應用拆成 CLI / orchestrator / tools / prompts / client
- 為什麼 structured output 對 developer tooling 很重要
- 為什麼 trace / telemetry 能提升 agent 系統可維護性
- 為什麼先做安全的 file tools，而不是直接加 shell execution
- 如何用 MVP 方式逐步把 prompt wrapper 升級成 agent harness

### 下一步方向

- 為 `fix` 加入安全的 patch apply 流程
- 支援 directory-level explain / fix
- 加入更明確的 tool loop 與 action selection
- 增加 JSON output mode，方便整合 editor 或其他工具

---

## English Version

Dev Agent CLI is a lightweight and controllable AI developer tool designed as a developer agent harness, not just a prompt wrapper or chatbot.

The goal of this project is not to build a simple "paste code into a prompt" utility, but to demonstrate a minimal, explainable, extensible, and observable AI developer workflow.

### Highlights

- Clear command abstraction: `explain`, `fix`, `gen-api`
- Controlled flow: `CLI -> Orchestrator -> Tools -> LLM -> Output`
- Built-in trace / telemetry for visibility
- Stable structured markdown output for `fix`
- Safe repo-aware capability through directory summary

### What problem this project solves

Many AI CLI demos are essentially:

`input file -> prompt -> model -> output`

They can work, but they are hard to describe as an agent harness because:

- flow control is unclear
- tool capability boundaries are vague
- model context is not observable
- future extension becomes messy

Dev Agent CLI keeps the MVP lightweight while establishing a practical agent-oriented foundation.

### Architecture Flow

`CLI -> Orchestrator -> Tools -> LLM -> Output`

- `CLI`
  Accepts user commands and arguments.

- `Orchestrator`
  Controls execution steps and decides how the workflow runs.

- `Tools`
  Provide bounded capabilities such as file read/write and directory summary.

- `Prompt Layer`
  Encapsulates command-specific behavior as explicit templates.

- `LLM Client`
  Wraps model API calls so the rest of the app is not tightly coupled to one vendor SDK.

### Supported Commands

- `explain`
  Explains the purpose, flow, and risks of a target file.

- `fix`
  Produces a structured fix response with stable sections:
  - Problem Summary
  - Root Cause
  - Recommended Fix
  - Revised Code
  - Trade-offs / Notes

- `gen-api`
  Generates API design from requirements or existing content.

### Why this feels more like an agent harness

Even though this is still an MVP, it already includes important agent-like properties:

- an orchestrator instead of direct CLI-to-model calls
- a tool layer instead of dumping everything into a prompt
- command-specific prompt templates
- trace / telemetry for observability
- lightweight repo context instead of pure single-file prompting

### Setup

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

### Usage

```bash
dev-agent explain .\sample_input.py --trace
dev-agent fix .\sample_input.py --goal "Reduce duplicated validation logic"
dev-agent gen-api .\requirements.txt --goal "Design a task management API"
```

Write output to a file:

```bash
dev-agent explain .\sample_input.py --output .\out\explain.md
```

### Project Structure

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

### Next Steps

- Add a safe patch-apply flow for `fix`
- Support directory-level explain / fix
- Add a clearer tool loop and action selection
- Add JSON output mode for editor integration
