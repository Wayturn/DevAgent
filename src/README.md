# src 說明

這個資料夾存放 Dev Agent CLI 的核心程式碼。

## 結構

```text
src/dev_agent_cli/
  cli.py
  config.py
  llm.py
  main.py
  models.py
  orchestrator.py
  prompts.py
  tools.py
```

## 模組職責

- `main.py`
  CLI 入口，組裝 `FileTool`、`PromptRegistry`、`OpenAILlmClient`、`AgentOrchestrator`

- `cli.py`
  命令列參數解析

- `config.py`
  讀取 `.env` 或環境變數設定

- `models.py`
  共享資料模型，例如 `CommandRequest`、`PromptPackage`、`TraceStep`

- `tools.py`
  目前的安全工具能力，包含：
  - 讀檔
  - 寫檔
  - 列出目錄檔案
  - 產生目錄摘要

- `prompts.py`
  command-specific prompt template

- `orchestrator.py`
  控制執行流程與 trace / telemetry

- `llm.py`
  OpenAI Responses API 封裝

## 目前進度

### 已完成

- 單檔 explain / fix / gen-api 工作流
- `fix` 的穩定結構輸出
- prompt template naming
- trace details
- repo-aware directory summary
- `.env` 支援

### 尚未做

- patch apply
- shell execution
- 多步 tool loop
- 目錄層級的正式 agent 規劃

## 設計原則

- MVP-first
- 可讀性優先
- 可觀測性優先
- 不引入不必要 abstraction
