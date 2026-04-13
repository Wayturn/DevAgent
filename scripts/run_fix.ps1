param(
    [string]$Target = ".\test_cases\inputs\sample_service.py",
    [string]$Goal = "Reduce duplicated validation logic and improve readability",
    [switch]$Trace
)

$command = @("python", "-m", "dev_agent_cli.main", "fix", $Target)

if ($Goal) {
    $command += @("--goal", $Goal)
}

if ($Trace) {
    $command += "--trace"
}

Write-Host "Running fix on $Target"
& $command[0] $command[1..($command.Length - 1)]
