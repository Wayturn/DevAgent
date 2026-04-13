param(
    [string]$Target = ".\test_cases\inputs\sample_service.py",
    [string]$Goal = "",
    [switch]$Trace
)

$command = @("python", "-m", "dev_agent_cli.main", "explain", $Target)

if ($Goal) {
    $command += @("--goal", $Goal)
}

if ($Trace) {
    $command += "--trace"
}

Write-Host "Running explain on $Target"
& $command[0] $command[1..($command.Length - 1)]
