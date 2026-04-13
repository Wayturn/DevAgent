# scripts 說明

這個資料夾提供 Windows / PowerShell 使用者的便利啟動腳本。

## 定位

這些腳本是本地開發與 demo 用的 convenience scripts，不是專案唯一入口。

正式入口仍然是：

```powershell
python -m dev_agent_cli.main <command> ...
```

## 目前提供的腳本

- `run_explain.ps1`
  快速執行 `explain`

- `run_fix.ps1`
  快速執行 `fix`

- `run_gen_api.ps1`
  快速執行 `gen-api`

## 使用方式

### explain

```powershell
.\scripts\run_explain.ps1 -Trace
.\scripts\run_explain.ps1 -Target ".\src\dev_agent_cli\orchestrator.py" -Trace
```

### fix

```powershell
.\scripts\run_fix.ps1 -Trace
.\scripts\run_fix.ps1 -Target ".\src\dev_agent_cli\prompts.py" -Goal "Make the logic easier to maintain" -Trace
```

### gen-api

```powershell
.\scripts\run_gen_api.ps1 -Trace
.\scripts\run_gen_api.ps1 -Target ".\test_cases\inputs\api_requirement.txt" -Goal "Design a clean RESTful backend API" -Trace
```

## 設計原則

- 不重寫既有邏輯
- 只包裝現有 CLI
- 保持低耦合
- 方便本地測試與 demo
