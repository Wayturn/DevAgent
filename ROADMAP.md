# Roadmap

這份 roadmap 用來說明 Dev Agent CLI 目前做到哪裡、接下來想往哪裡走，以及哪些方向暫時不做。

## 現在已完成

### Core architecture

- CLI entrypoint
- `AgentOrchestrator`
- `FileTool`
- `PromptRegistry`
- `OpenAILlmClient`
- basic data models

### Commands

- `explain`
- `fix`
- `gen-api`

### Current developer-agent features

- command abstraction
- structured `fix` output
- basic trace / telemetry
- lightweight repo-aware file tools
- `.env` support
- unit tests
- test cases and test reports
- PowerShell convenience scripts

## 近期想做

### 1. Improve `fix`

- 更貼近 code review / refactor assistant
- 強化 minimal diff / preserve behavior 導向
- 提高建議品質與穩定性

### 2. Improve `gen-api`

- 補更多 backend 實戰細節
- 加入更合理的 validation / ownership / error response thinking

### 3. Improve README / Quick Start

- 持續優化開源體驗
- 讓第一次進 repo 的使用者更容易快速體驗

## 中期候選方向

### 1. Safer code-output workflow

- 先考慮 output-to-file
- 再考慮更安全的 patch-like workflow

### 2. Better repo awareness

- 更好的 directory-level reasoning
- 但仍保持 bounded / safe

### 3. More test scenarios

- 擴充 `test_cases`
- 加入不同 prompt 版本比較

## 目前明確不做

以下方向目前不是這個專案的重點：

- shell execution
- unsafe code execution
- autonomous multi-step agent loop
- patch apply engine
- vector DB / RAG
- editor integration
- enterprise architecture refactor

## 專案定位

Dev Agent CLI 目前的定位是：

**a lightweight, inspectable AI-assisted developer workflow / agent harness experiment**

這是學習與作品集專案，不是 production-ready 工具。它把 command、orchestration、tool、prompt 與 model call 的責任邊界攤開；trace 讓執行流程可檢視，測試與手動案例驗證目前涵蓋的行為。這些描述不代表完整的檔案路徑安全隔離。

這代表它現在的核心價值是：

- 清楚的 command、orchestration、tool、prompt 與 model call 邊界
- 可檢視的執行流程與 trace / telemetry
- 由測試與手動案例驗證目前涵蓋的行為
- 以 AI application / developer tooling 為主題的學習與作品集實作
