# Dev Agent CLI

Dev Agent CLI 是一個輕量、可控的 AI developer agent CLI。
這個專案的目標不是做成聊天機器人，而是以最小可行架構實作一個 developer agent harness。

`CLI -> Orchestrator -> Tools -> LLM -> Output`

## 為什麼做這個專案

這個專案的出發點，不是單純包一層 LLM API，而是想用一個小而清楚的實作，驗證 AI developer tooling 在實務上應該如何被設計。

很多 AI CLI 範例本質上只是把檔案內容直接丟進 prompt，再把模型輸出原樣回傳。這種方式雖然能快速做出 demo，但通常很難演進成可維護、可觀測、可逐步擴充的工程工具。

Dev Agent CLI 的目標，是在不過度設計的前提下，實作一個具備基本 agent harness 特徵的開發者工具：有明確的 command abstraction、有 orchestrator 控制流程、有受限的 tools、有 prompt layer，也保留 trace / telemetry 與後續擴充空間。

## 核心設計理念

- **MVP-first**
  先做出可執行、可驗證、可說明的最小版本，而不是一開始就引入複雜框架。

- **可控性優先於魔法感**
  比起讓模型自由發揮，這個專案更重視 command、prompt、tool、trace 之間的邊界與流程控制。

- **工程可讀性優先**
  模組切分維持輕量，讓人能快速理解 CLI、Orchestrator、Tools、LLM 之間的責任分工。

- **逐步演進成 developer agent harness**
  目前先從單步、受控、低風險的工作流開始，未來再視需要往更多工具能力與更完整的 agent loop 演進。

## 這個專案是什麼 / 不是什麼

### 這個專案是什麼

- 一個輕量、可控的 CLI-based AI developer agent MVP
- 一個以 developer tooling 為方向的 agent harness 實作
- 一個能展示 prompt abstraction、tool usage、trace visibility 的作品集專案
- 一個可持續增量演進的 AI application engineering 練習場

### 這個專案不是什麼

- 不是單純的聊天機器人包裝
- 不是大型 framework 或多代理系統
- 不是具備 shell execution、patch apply、autonomous loop 的完整 agent 平台
- 不是以炫技為主的架構展示，而是偏向實作可讀、可驗證、可說明的工程作品

## 專案亮點摘要

- **清楚的模組化架構**
  採用 `CLI -> Orchestrator -> Tools -> LLM -> Output` 流程，責任分工清楚，便於說明與擴充。

- **Command abstraction**
  目前支援 `explain`、`fix`、`gen-api`，每個 command 都有對應的 prompt 設計與用途定位。

- **Lightweight tool layer**
  工具層以安全的檔案操作與目錄摘要為主，避免過早加入高風險能力。

- **Structured output + telemetry**
  `fix` 已具備較穩定的結構化輸出，同時保留 trace / telemetry，讓執行流程更容易觀察與 debug。

- **作品集導向的工程實作**
  專案不只追求功能能跑，也重視 README、測試、手動測試案例、報告整理等可展示性。

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
