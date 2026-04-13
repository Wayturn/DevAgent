# Dev Agent CLI 測試報告

## 基本資訊

- 測試日期：2026-04-13
- 測試環境：本機 PowerShell + `.env`
- 使用模型：`gpt-4.1-mini`
- 測試範圍：`explain`、`fix`、`gen-api`
- 測試目的：依照 `test_cases` 既有測試流程，重新驗證目前 v3 狀態下的實用性與輸出穩定性

## 測試摘要

這次測試的重點，不只是確認三個 command 能不能執行，而是重新檢查在 v3 調整後：

- repo-aware tool 能力是否真的有被使用
- `fix` 的輸出是否更穩定、更像工具
- trace / telemetry 是否更接近 agent harness 觀察需求

整體結論：

- `fix` 依然是目前最有價值的命令，而且 v3 後更穩定
- `gen-api` 仍然具備 backend 初稿價值
- `explain` 可用，但仍偏向整理型輸出
- trace / telemetry 在 v3 後更清楚，特別是 directory-aware tool 的使用情況已可明確觀察

整體評價：

- `explain`：3.5 / 5
- `fix`：4.6 / 5
- `gen-api`：4 / 5

## 測試項目 1

- 指令：
  `python -m dev_agent_cli.main explain .\test_cases\inputs\sample_service.py --trace`
- 目標檔案：
  `test_cases/inputs/sample_service.py`

### 結果摘要

輸出清楚說明了 `TaskService` 的用途、`create_task()` 與 `update_task_status()` 的流程，以及幾個合理的 backend 風險點，例如：

- 目前只操作 in-memory dict，沒有 persistence layer
- `completed_at` 只是 `"now"` 字串，不是真正時間
- task 使用 dict，缺少型別保護
- 沒有對 `description` 與 `due_date` 做更完整驗證

### 觀察

- 優點：
  - 仍然維持穩定且好讀
  - 能提出實務上合理的風險與改善點
  - 對小型 service 檔案有基本解釋價值

- 不足：
  - 仍比較偏摘要型與整理型
  - 相比 `fix`，工具感沒有那麼強
  - repo-aware context 有帶進去，但對回答品質的影響仍有限

### Trace / Telemetry

這次 trace 顯示：

- command：`explain`
- target path：`test_cases\inputs\sample_service.py`
- target extension：`.py`
- prompt template：`explain_v1`
- model：`gpt-4.1-mini`
- input chars：1152
- output chars：2653
- `directory_tool_used`：先是 `false`，接著在目錄觀察步驟為 `true`
- `directory_files_listed`：2

### 實用性評分

3.5 / 5

### 結論

`explain` 依然是穩定可用的說明工具，但目前最主要價值還是在「快速理解」，而不是提供更強的設計洞察。

## 測試項目 2

- 指令：
  `python -m dev_agent_cli.main fix .\test_cases\inputs\sample_service.py --goal "Reduce duplicated validation logic and improve readability" --trace`
- 目標檔案：
  `test_cases/inputs/sample_service.py`

### 結果摘要

v3 後的 `fix` 輸出結構如下：

- `## Problem Summary`
- `## Root Cause`
- `## Recommended Fix`
- `## Revised Code`
- `## Follow-up Checks`

這次的建議內容仍然務實，重點包括：

- 抽出 `_validate_user_id`
- 抽出 `_validate_status`
- 抽出 `_validate_title`
- 用集合簡化 status 驗證
- 將驗證邏輯集中化，降低重複程式碼

### 觀察

- 優點：
  - 結構非常穩定
  - `Follow-up Checks` 比原本的 `Trade-offs / Notes` 更接近工程實務
  - revised code 可以直接當 refactor 參考
  - trace 能清楚看出這次使用的是 `fix_v3_structured_markdown`

- 不足：
  - 還是屬於建議型工具，尚未進入 patch apply
  - `minimal diff`、`preserve behavior` 雖然有部分體現，但還沒被更強約束
  - 若未來要更像 code review assistant，還可以再更聚焦於 regression risk 與 behavior safety

### Trace / Telemetry

這次 trace 顯示：

- command：`fix`
- prompt template：`fix_v3_structured_markdown`
- model：`gpt-4.1-mini`
- input chars：1152
- prompt chars：2338
- output chars：2622
- `directory_tool_used`：有明確顯示
- `directory_files_listed`：2
- `write_back_requested`：`false`

### 實用性評分

4.6 / 5

### 結論

`fix` 依然是目前整個專案最有作品集價值的 command，而 v3 後因為 `Follow-up Checks` 與更清楚的 trace，整體更像一個輕量 developer tool。

## 測試項目 3

- 指令：
  `python -m dev_agent_cli.main gen-api .\test_cases\inputs\api_requirement.txt --goal "Design a clean RESTful backend API" --trace`
- 目標檔案：
  `test_cases/inputs/api_requirement.txt`

### 結果摘要

輸出仍提供完整的 API 初稿，包括：

- API purpose
- endpoint design
- request / response models
- validation rules
- service / repository responsibilities

這次內容包含：

- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}/status`
- `owner_id` / ownership 限制
- `completed_at` 處理
- 建議用於 Python MVP，例如 FastAPI + SQLAlchemy

### 觀察

- 優點：
  - 仍有實際 backend 初稿價值
  - 結構清楚，對面試展示也夠好理解
  - 有把 ownership 與 validation 放進設計說明

- 不足：
  - 仍偏 generic
  - 尚未強化更多實戰細節，例如：
    - pagination
    - error response contract
    - idempotency
    - transaction 邏輯
  - endpoint 設計仍比較偏一般 REST 初稿，而不是更深入的業務設計

### Trace / Telemetry

這次 trace 顯示：

- command：`gen-api`
- prompt template：`gen_api_v1`
- model：`gpt-4.1-mini`
- input chars：573
- prompt chars：1546
- output chars：4172
- `directory_tool_used`：有明確顯示
- `directory_files_listed`：2
- `write_back_requested`：`false`

### 實用性評分

4 / 5

### 結論

`gen-api` 已具備 API 設計初稿價值，但若未來想更貼近真實 backend workflow，還需要補更多工程約束與設計細節。

## 綜合分析

### v3 帶來的實際提升

這一輪測試中，v3 最明顯的提升有三個：

- `fix` 結構更穩定
  `Follow-up Checks` 比前一版更接近工程實務，也更像真正的工具輸出。

- repo-aware tool 能力更清楚
  目錄摘要仍然輕量，但現在 trace 已能明確看出 directory-aware tool 是否使用、列出了多少檔案。

- telemetry 更像 agent harness
  trace 現在不只是「有步驟」，而是能說明 prompt template、model、輸入輸出大小、directory tool 狀態。

### 目前最有價值的地方

- `fix` 的 structured output
- trace / telemetry 的可觀測性
- 安全且邊界清楚的 repo-aware file tools

### 目前還偏 MVP 的地方

- `explain` 仍偏摘要型
- `gen-api` 還缺更強的 backend 實戰約束
- orchestrator 仍是單步線性流程，尚未進入更完整的多步 agent harness

## 下一步建議

### 第一優先

持續強化 `fix` prompt，使其更像 code review / refactor assistant：

- 明確強調 minimal diff
- 明確強調 preserve behavior
- 更聚焦於 regression risk
- 更貼近真實 review 語境

### 第二優先

強化 `gen-api` 的 backend 實戰性：

- pagination
- error response format
- auth assumptions
- idempotency thinking
- repository / service 邊界更具體

### 第三優先

未來再考慮 patch apply 或更完整的 tool loop：

- 現階段先把「建議品質」做強仍然最划算
- 直接加入 patch apply 會開始碰到安全性與使用者信任問題

## 結論

這次依照 `test_cases` 流程重跑後，可以確認 v3 方向是有效的。

Dev Agent CLI 目前已經具備：

- 可展示的 agent harness 敘事
- 有實用價值的 `fix`
- 可觀測的 trace / telemetry
- 基本安全的 repo-aware tool 能力

它仍然是一個輕量 MVP，但已經不只是 prompt wrapper，而是一個更完整、更可解釋的 developer agent CLI 作品集專案。
