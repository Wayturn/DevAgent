param(
    [string]$Target = ".\test_cases\inputs\api_requirement.txt",
    [string]$Goal = "Design a clean RESTful backend API",
    [switch]$Trace
)

$command = @("python", "-m", "dev_agent_cli.main", "gen-api", $Target)

if ($Goal) {
    $command += @("--goal", $Goal)
}

if ($Trace) {
    $command += "--trace"
}

Write-Host "Running gen-api on $Target"
& $command[0] $command[1..($command.Length - 1)]
