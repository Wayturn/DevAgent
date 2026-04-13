# tests 說明

這個資料夾存放 Dev Agent CLI 的自動化測試。

## 目前測試範圍

- CLI 參數解析
- 缺少 API key 時的友善錯誤訊息
- `.env` 載入設定
- 環境變數覆蓋 `.env`
- orchestrator 基本流程
- `fix` prompt 結構
- directory summary 工具能力

## 測試檔案

- `test_cli.py`
  測試 CLI parsing、設定載入與錯誤處理

- `test_orchestrator.py`
  測試 orchestrator、prompt 結構與 file tool 行為

## 執行方式

```powershell
python -m unittest discover -s tests -v
```

## 目前測試策略

- 優先驗證 MVP 的核心流程
- 優先驗證可預期的輸出結構
- 不過早加入大量 integration test

## 後續可補

- 更完整的 trace snapshot 驗證
- `gen-api` prompt 的格式驗證
- output file 寫入行為的更多 edge case
