# DevAgent 架構導讀

這份文件的目標不是解釋每一行程式碼，而是幫你建立這個專案的整體理解。

重點是先回答：

- 這個專案整體怎麼運作？
- 每個模組分別負責什麼？
- 為什麼它不是單純的 prompt wrapper？
- 之後如果要自己改功能，該先從哪裡理解？

---

## 1. 專案一句話定位

DevAgent 是一個 **analysis-first、lightweight developer agent CLI**。

它的核心流程是：

`CLI -> Orchestrator -> Tools -> LLM -> Output`

這代表它不是單純把 prompt 丟進模型，而是先透過 CLI 接收命令，再由 orchestrator 控制流程，透過 tool layer 提供受控能力，最後才呼叫 LLM 並輸出結果。

---

## 2. 整體架構圖

```mermaid
flowchart LR
    U["使用者輸入指令"] --> CLI["cli.py\n解析命令列參數"]
    CLI --> REQ["CommandRequest\n結構化請求物件"]

    REQ --> MAIN["main.py\n組裝系統元件"]
    MAIN --> ORCH["orchestrator.py\n流程控制器"]

    ORCH --> TOOLS["tools.py\nFileTool"]
    ORCH --> PROMPTS["prompts.py\nPromptRegistry"]
    ORCH --> LLM["llm.py\nOpenAILlmClient"]

    TOOLS --> ORCH
    PROMPTS --> ORCH
    LLM --> ORCH

    ORCH --> RESULT["AgentResult\n內容 + trace"]
    RESULT --> OUT["終端輸出 / 寫入檔案"]
```

---

## 3. 執行流程圖

假設執行這條指令：

```powershell
python -m dev_agent_cli.main fix .\test_cases\inputs\sample_service.py --trace
```

實際流程如下：

```mermaid
sequenceDiagram
    participant User as 使用者
    participant CLI as cli.py
    participant Main as main.py
    participant Orch as orchestrator.py
    participant Tool as FileTool
    participant Prompt as PromptRegistry
    participant LLM as OpenAILlmClient

    User->>CLI: 輸入 fix + target + trace
    CLI->>Main: 回傳 CommandRequest
    Main->>Main: 讀取設定 AppConfig
    Main->>Orch: 建立 AgentOrchestrator
    Orch->>Tool: read_text(target file)
    Tool-->>Orch: file_content
    Orch->>Tool: read_directory_summary(parent dir)
    Tool-->>Orch: directory_summary
    Orch->>Prompt: build(request, file_content)
    Prompt-->>Orch: PromptPackage
    Orch->>LLM: generate(prompt)
    LLM-->>Orch: model output
    Orch-->>Main: AgentResult
    Main-->>User: 印出內容與 trace
```

---

## 4. 每個模組的責任

| 模組 | 主要責任 | 不該做的事 |
|---|---|---|
| `cli.py` | 解析命令列輸入 | 不該讀檔或打模型 |
| `main.py` | 組裝系統與啟動流程 | 不該承擔業務邏輯 |
| `orchestrator.py` | 控制整個 AI workflow | 不該自己硬寫 prompt 細節 |
| `tools.py` | 提供受控工具能力 | 不該變成萬能 shell |
| `prompts.py` | 產生 command-specific prompt | 不該控制流程 |
| `llm.py` | 呼叫模型 API | 不該知道業務邏輯 |
| `models.py` | 定義共享資料結構 | 不該承擔流程邏輯 |

---

## 5. `main.py` 的角色

`main.py` 的角色很像應用程式的啟動點或 composition root。

它主要做這幾件事：

1. 呼叫 `parse_request()`，把 CLI 輸入轉成 `CommandRequest`
2. 讀取 `.env` 或環境變數設定
3. 建立 `FileTool`、`PromptRegistry`、`OpenAILlmClient`
4. 組裝 `AgentOrchestrator`
5. 執行 `orchestrator.run(request)`
6. 印出結果與 trace

它的重點不是做業務邏輯，而是把整個系統「接起來」。

---

## 6. `cli.py` 的角色

`cli.py` 的責任是把命令列輸入轉成乾淨的 request model。

目前它支援三個 command：

- `explain`
- `fix`
- `gen-api`

並且把這些參數：

- `target`
- `goal`
- `output`
- `trace`

整理成 `CommandRequest`。

這樣後面的 orchestrator 就不用知道 argparse 細節，只需要處理一個穩定的 request 物件。

---

## 7. `orchestrator.py` 的角色

`orchestrator.py` 是這個專案的流程控制器。

一句話：

> 它決定先做什麼、再做什麼、結果怎麼整理。

目前 `run()` 的流程是：

1. 讀取目標檔案內容
2. 讀取目標目錄摘要
3. 根據 command 建 prompt
4. 呼叫 LLM
5. 必要時寫入輸出檔案
6. 收集 trace / telemetry
7. 回傳 `AgentResult`

這是目前整個專案最核心的地方。

---

## 8. `prompts.py` 的角色

`PromptRegistry` 的價值不是單純存放 prompt 字串，而是把不同 command 的 AI 行為明確化。

目前的 mapping 很清楚：

- `explain` -> explain prompt
- `fix` -> fix prompt
- `gen-api` -> gen-api prompt

這就是 command abstraction。

### 為什麼它重要？

因為這樣：

- prompt 不會散在各處
- 每個 command 的行為規格更清楚
- prompt 可以版本化，例如 `fix_v3_structured_markdown`
- 更容易測試與調整

### `fix` 為什麼最像工具？

因為它不是自由回答，而是要求模型固定輸出：

- `Problem Summary`
- `Root Cause`
- `Recommended Fix`
- `Revised Code`
- `Follow-up Checks`

這讓它更像工具輸出，而不是一篇很會寫的 AI 建議文。

---

## 9. `tools.py` 的角色

`FileTool` 是這個專案目前的 tool layer。

它的設計重點不是很強，而是：

- 受控
- 可預測
- 有邊界

目前提供的能力有：

- `read_text()`
- `write_text()`
- `list_files()`
- `read_directory_summary()`

### 為什麼 tool layer 很重要？

如果沒有 tool layer，整個專案會退化成：

- 直接把檔案內容塞進 prompt
- 讓模型自己猜更多 context

有了 tool layer 之後，AI 的上下文來源就變成工程上可控制的資料，而不是純 prompt 猜測。

### 為什麼目前不直接加 shell execution？

因為這個專案目前是 MVP，而且是學習型、作品集導向。

先從 bounded file tools 開始比較合理，因為：

- 安全性高
- 可觀測性高
- 容易說明設計理由
- 風險比 shell execution 低很多

---

## 10. `llm.py` 的角色

`llm.py` 負責封裝模型呼叫。

它做的事情很單純：

- 接收 `PromptPackage`
- 呼叫 OpenAI Responses API
- 回傳模型輸出文字

它不負責：

- 決定流程
- 讀檔
- 組 prompt
- 理解業務邏輯

它只是模型呼叫的 adapter。

---

## 11. `models.py` 的角色

`models.py` 提供整個專案共享的資料結構，例如：

- `CommandRequest`
- `PromptPackage`
- `TraceStep`
- `AgentResult`

你可以把它想成：

> 讓不同模組之間講同一種語言。

這樣 CLI、orchestrator、prompt registry、LLM client 就不用彼此直接吃很原始的資料格式。

---

## 12. 為什麼這個專案不是單純 prompt wrapper？

如果是一般 prompt wrapper，流程通常是：

```text
讀檔 -> 拼 prompt -> 丟模型 -> 拿回答
```

但 DevAgent 目前已經多了這些關鍵元素：

- command abstraction
- orchestrator-controlled workflow
- tool layer
- repo-aware context
- structured output
- trace / telemetry

所以更準確的說法是：

> 這是一個 analysis-first、lightweight developer agent harness，而不是只有 prompt in / answer out 的小工具。

---

## 13. 用餐廳比喻來理解

如果你覺得模組之間很抽象，可以用餐廳來想：

```mermaid
flowchart LR
    A["客人點餐"] --> B["cli.py\n接單"]
    B --> C["CommandRequest\n訂單內容"]
    C --> D["main.py\n把人員叫齊"]
    D --> E["orchestrator.py\n店長安排流程"]
    E --> F["tools.py\n備料/拿資料"]
    E --> G["prompts.py\n決定料理說明"]
    E --> H["llm.py\n請廚師做菜"]
    H --> E
    E --> I["AgentResult\n成品 + 過程紀錄"]
    I --> J["輸出給客人"]
```

對應關係：

- `cli.py` = 櫃檯
- `main.py` = 開店 / 接線
- `orchestrator.py` = 店長
- `tools.py` = 備料區
- `prompts.py` = 菜單規格
- `llm.py` = 廚師
- `trace` = 廚房作業紀錄

---

## 14. 你目前最該會講的 5 句話

1. 這個專案是 analysis-first 的 developer agent CLI。
2. 它的核心流程是 `CLI -> Orchestrator -> Tools -> LLM -> Output`。
3. `Orchestrator` 的責任是控制流程，不是做所有事情。
4. `PromptRegistry` 讓不同 command 有明確的 prompt abstraction。
5. `FileTool` 目前刻意保持安全，只提供 bounded file operations。

如果這 5 句你能自然講出來，代表你對整個專案已經有不錯的理解。

---

## 15. 建議學習順序

如果你要持續把這個專案真正內化，建議順序是：

### 第一輪：先懂流程

- `main.py`
- `cli.py`
- `orchestrator.py`

### 第二輪：再懂 agent 核心

- `prompts.py`
- `tools.py`

### 第三輪：補工程化支撐

- `models.py`
- `config.py`
- `tests/`

### 第四輪：自己改一個小功能

例如：

- 增加一個 trace 欄位
- 修改 `fix` prompt
- 調整 `list_files()` 的行為

---

## 16. 目前理解自己的檢查題

你可以用下面 3 題檢查自己：

1. 如果拿掉 `orchestrator.py`，整個專案會變成什麼樣子？
2. 如果拿掉 `tools.py`，這個專案會退化成什麼？
3. `PromptRegistry` 和 `llm.py` 最大差別是什麼？

如果你能用自己的話回答出來，而且答案越來越穩，代表你開始真的理解這個專案，而不是只會看檔名。
