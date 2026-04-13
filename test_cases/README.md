# test_cases 說明

這個資料夾存放 Dev Agent CLI 的手動測試素材與測試紀錄。

目標是讓專案可以重複驗證：

- `explain` 是否真的有幫助理解程式碼
- `fix` 是否能提供穩定且有價值的建議
- `gen-api` 是否能產出有 backend 初稿價值的內容

## 分類方式

```text
test_cases/
  inputs/
  reports/
  templates/
```

- `inputs/`
  手動測試輸入檔案

- `reports/`
  實際測試後整理出的報告

- `templates/`
  測試紀錄模板

## 目前內容

### inputs

- `inputs/sample_service.py`
  用來測 `explain` 與 `fix`

- `inputs/api_requirement.txt`
  用來測 `gen-api`

### reports

- `reports/test_report_2026-04-13.md`
  第一輪實測報告

- `reports/test_report_2026-04-13_v3.md`
  v3 狀態下重新執行的測試報告

### templates

- `templates/test_log_template.md`
  手動測試紀錄模板

## 建議測試順序

1. `fix` on `inputs/sample_service.py`
2. `explain` on `inputs/sample_service.py`
3. `gen-api` on `inputs/api_requirement.txt`

## 範例指令

```powershell
python -m dev_agent_cli.main fix .\test_cases\inputs\sample_service.py --goal "Reduce duplicated validation logic and improve readability" --trace
python -m dev_agent_cli.main explain .\test_cases\inputs\sample_service.py --trace
python -m dev_agent_cli.main gen-api .\test_cases\inputs\api_requirement.txt --goal "Design a clean RESTful backend API" --trace
```

## 輸出到檔案

```powershell
python -m dev_agent_cli.main explain .\test_cases\inputs\sample_service.py --output .\out\sample_service_explain.md --trace
```

## 目前進度

- 已建立基礎手動測試素材
- 已完成第一輪實測報告
- 已完成 v3 重新測試報告
- 後續可以持續累積不同 prompt 版本的比較報告
