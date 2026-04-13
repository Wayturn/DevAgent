# Dev Agent CLI 測試報告

## 基本資訊

- 測試日期：2026-04-13
- 測試環境：本機 PowerShell + `.env`
- 使用模型：`gpt-4.1-mini`
- 測試範圍：`explain`、`fix`、`gen-api`
- 測試目的：驗證目前 MVP 是否已具備實用性，而不只是 prompt wrapper

## 測試摘要

這次測試重點不是單純確認「能不能跑」，而是檢查這個專案是否已經有 developer tooling 的實際價值。

整體結論：

- `fix` 是目前最有價值的命令
- `gen-api` 已具備 backend 初稿產出能力
- `explain` 可用，但目前偏向整理與摘要，驚喜感較少
- trace / telemetry 有實際價值，能幫助觀察 agent 執行過程

整體評價：

- `explain`：3.5 / 5
- `fix`：4.5 / 5
- `gen-api`：4 / 5

## 測試項目 1

- 指令：
  `python -m dev_agent_cli.main explain .\test_cases\sample_service.py --trace`
- 目標檔案：
  `test_cases/sample_service.py`

### 結果摘要

輸出清楚解釋了 `TaskService` 的用途、`create_task()` 與 `update_task_status()` 的流程，以及一些實務上可能的改進點，例如：

- 目前只操作 in-memory dict，沒有 persistence layer
- `completed_at` 使用 `"now"` 字串而不是真正時間
- status validation 可以改成 enum 或常數集合
- dict 結構缺乏型別保護

### 觀察

- 優點：
  - 回答穩定、好讀
  - 能抓到幾個合理的 backend 風險點
  - 不會完全停留在逐行翻譯

- 不足：
  - 比較像「整理與說明」，而不是更深層的設計理解
  - 對這類小檔案來說，幫助有，但還沒到會讓人覺得明顯省時間
  - repo-aware context 有帶進去，但目前對回答品質的影響不算明顯

### Trace / Telemetry

這次 trace 顯示：

- target path：`test_cases\sample_service.py`
- target extension：`.py`
- prompt template：`explain_v1`
- model：`gpt-4.1-mini`
- input chars：1152
- output chars：3154
- 有帶入 directory summary

### 實用性評分

3.5 / 5

### 結論

`explain` 已經合格，但目前比較像「穩定的說明助手」，還沒有強烈展現出 agent 工具的獨特價值。

## 測試項目 2

- 指令：
  `python -m dev_agent_cli.main fix .\test_cases\sample_service.py --goal "Reduce duplicated validation logic and improve readability" --trace`
- 目標檔案：
  `test_cases/sample_service.py`

### 結果摘要

這個命令輸出結構非常穩定，確實包含了預期的五個區塊：

- `## Problem Summary`
- `## Root Cause`
- `## Recommended Fix`
- `## Revised Code`
- `## Trade-offs / Notes`

建議內容也符合實務：

- 抽出 `_validate_user_id(user_id)`
- 抽出 `_validate_title(title)`
- 用 `set` 取代多重 `or` 狀態判斷
- 保持既有行為不變，優先改善可讀性與維護性

### 觀察

- 優點：
  - 最像真正 developer tool 的輸出
  - revised code 可以直接當重構參考
  - 結構穩定，後續很容易做簡單 parsing 或 UI 呈現
  - 建議偏保守，符合 MVP 與 maintainability 導向

- 不足：
  - 還沒有特別強調 minimal diff 或 preserve behavior
  - revised code 雖然可用，但還沒有完全貼合更大專案的風格約束
  - 還沒有進入 patch apply，因此目前仍是「建議型工具」

### Trace / Telemetry

這次 trace 顯示：

- prompt template：`fix_v2_structured_markdown`
- model：`gpt-4.1-mini`
- input chars：1152
- prompt chars：2225
- output chars：2342
- write_back_requested：`false`

### 實用性評分

4.5 / 5

### 結論

`fix` 是目前整個專案最有展示價值的功能。它已經不像只是包一層 prompt，而是開始有「agent-style developer assistant」的味道。

## 測試項目 3

- 指令：
  `python -m dev_agent_cli.main gen-api .\test_cases\api_requirement.txt --goal "Design a clean RESTful backend API" --trace`
- 目標檔案：
  `test_cases/api_requirement.txt`

### 結果摘要

輸出提供了完整的 API 初稿，包括：

- API purpose
- endpoint design
- request / response models
- validation rules
- service / repository responsibilities

內容上有提到：

- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `title` 必填
- `status` 限制為 `todo`, `doing`, `done`
- `completed_at` 在狀態切換時處理
- ownership check

### 觀察

- 優點：
  - 已經有實際 backend 初稿價值
  - 不只是列 endpoint，還有 model 與 validation
  - service / repository 的切分也合理

- 不足：
  - 整體仍偏 generic
  - 還沒很貼近真實專案會關注的細節，例如：
    - pagination
    - error response contract
    - idempotency
    - auth context 實作方式
  - 若目標是面試展示，還可以再更強調實務設計決策

### Trace / Telemetry

這次 trace 顯示：

- prompt template：`gen_api_v1`
- model：`gpt-4.1-mini`
- input chars：573
- prompt chars：1567
- output chars：4205
- write_back_requested：`false`

### 實用性評分

4 / 5

### 結論

`gen-api` 已具備明顯可用性，可以當成 API 設計初稿工具，但還需要更多 backend 實戰約束，才能更貼近真實工作流。

## 綜合分析

### 目前最有價值的地方

- `fix` 的 structured output 已經有工具感
- trace / telemetry 不是裝飾，而是真的能幫助理解 agent flow
- prompt template abstraction 清楚，利於後續持續調整

### 目前還偏 MVP 的地方

- `explain` 偏摘要型，缺少更深的設計洞察
- `gen-api` 還不夠貼近真實 backend 團隊慣例
- repo-aware context 有加分，但影響力還不夠大

### 這個專案目前比較像什麼

目前它已經不是單純的 prompt wrapper，但還在「輕量 developer agent harness」的早期階段。

比較準確的描述是：

- 有可控流程
- 有工具邊界
- 有可觀測性
- 有 command abstraction
- 但還沒有進入真正多步工具操作或 patch apply

## 下一步建議

### 第一優先

強化 `fix` 的 prompt，讓它更像 code review / refactor assistant：

- 強調 minimal diff
- 強調 preserve behavior
- 避免不必要抽象
- 更貼近真實開發風格

### 第二優先

強化 `gen-api` 的 backend 實戰性：

- pagination
- error response format
- auth assumptions
- ownership enforcement flow
- transaction / consistency thinking

### 第三優先

之後再評估 patch apply：

- 現在先把建議品質做好，比直接進 patch apply 更划算
- patch apply 一旦加入，就要開始處理安全性與使用者信任問題

## 結論

這次測試結果是正面的。

Dev Agent CLI 已經具備：

- 真正可用的 `fix`
- 可展示的 trace / telemetry
- 可作為 API 初稿工具的 `gen-api`

它現在最大的價值，不是「功能很多」，而是：

在很小的架構下，已經能展示出 agent harness 的核心元素，而且輸出開始有實務價值。
