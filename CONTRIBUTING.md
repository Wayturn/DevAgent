# Contributing

感謝你對 Dev Agent CLI 有興趣。

這個專案目前是 learning-oriented、portfolio-oriented 的開源專案，重點在於：

- 研究 lightweight developer agent harness 的設計方式
- 驗證 explain / fix / gen-api 這類 AI developer tooling 的實用性
- 用小步演進方式累積 prompt、tooling、trace、repo-awareness 的經驗

## 目前歡迎的貢獻方向

- 改善 README 與使用說明
- 改善 `fix` / `gen-api` prompt 穩定性
- 補充測試案例與測試報告
- 優化 trace / telemetry 可讀性
- 改善 CLI 使用體驗
- 補充安全、輕量的 tool 能力

## 目前不考慮的方向

為了維持專案聚焦，以下方向目前不優先接受：

- shell execution
- unsafe code execution
- autonomous multi-step loop
- vector DB / RAG
- heavy framework refactor
- enterprise-grade abstraction

## 開發方式

### 1. 安裝

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

### 2. 設定

建立 `.env`：

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

### 3. 執行測試

```powershell
python -m unittest discover -s tests -v
```

## 提交建議

如果你要提 PR，建議描述：

- 你改了什麼
- 為什麼要改
- 有沒有影響既有 CLI / trace / prompt 行為
- 有沒有補測試

## 設計原則

這個專案希望維持以下原則：

- MVP-first
- readable over clever
- safe over powerful
- incremental over over-engineered

## 討論方式

如果你對方向有不同想法，歡迎先提 issue 或討論。

這個專案本來就偏向學習型與交流型，所以清楚的設計理由，通常比一次丟很大的改動更有價值。
