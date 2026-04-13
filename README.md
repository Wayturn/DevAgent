# Dev Agent CLI

Dev Agent CLI 是一個輕量、可控的 AI developer agent CLI。

目前專案的核心定位不是聊天機器人，而是以最小可行架構實作一個 developer agent harness，流程如下：

`CLI -> Orchestrator -> Tools -> LLM -> Output`

## 專案目標

- 用簡單可讀的方式實作 agent-style developer workflow
- 保留 command abstraction，而不是把所有行為都塞進單一 prompt
- 讓 trace / telemetry 可以觀察 agent 執行過程
- 用安全的 file tools 先建立基礎能力
- 保持 MVP-first，避免過度設計

## 目前功能

- `explain`
  解釋目標檔案的用途、流程與風險

- `fix`
  針對目標檔案輸出結構化修正建議

- `gen-api`
  根據需求或文字內容產生 API 初稿

## 目前進度

### 已完成

- CLI 入口與 command parsing
- `AgentOrchestrator`
- `FileTool`
- `PromptRegistry`
- `OpenAILlmClient`
- `fix` 穩定 Markdown 結構輸出
- trace / telemetry
- `.env` 讀取支援
- 基本單元測試
- 手動測試素材與測試報告

### 下一步候選

- 強化 `fix`，更貼近 code review / refactor assistant
- 強化 `gen-api` 的 backend 實戰細節
- 支援 directory-level reasoning
- 之後再評估 patch apply

## 目錄結構

```text
src/
  README.md
  dev_agent_cli/
tests/
  README.md
test_cases/
  README.md
  inputs/
  reports/
  templates/
```

## 設定方式

### 方式 1：使用 `.env`

在專案根目錄建立 `.env`：

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

可以直接參考：

```text
.env.example
```

### 方式 2：使用 PowerShell 環境變數

```powershell
$env:OPENAI_API_KEY="your_openai_api_key_here"
$env:OPENAI_MODEL="gpt-4.1-mini"
```

## 常用指令

```powershell
python -m dev_agent_cli.main explain .\test_cases\inputs\sample_service.py --trace
python -m dev_agent_cli.main fix .\test_cases\inputs\sample_service.py --goal "Reduce duplicated validation logic and improve readability" --trace
python -m dev_agent_cli.main gen-api .\test_cases\inputs\api_requirement.txt --goal "Design a clean RESTful backend API" --trace
```

## 相關說明文件

- `src/README.md`
  核心程式結構與目前模組進度

- `tests/README.md`
  測試範圍與目前測試策略

- `test_cases/README.md`
  手動測試素材、分類與使用方式
