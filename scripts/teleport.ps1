function tp {
    param(
        [Parameter(ValueFromRemainingArguments=$true)]
        $args
    )
    
    $cmd = $args[0]
    
    # Check if user wants a known command or help
    if ($cmd -in @("add", "save", "list", "--help", "update", "--update")) {
        python -m teleport.cli $args
        return
    }

    $tmp_file = [System.IO.Path]::GetTempFileName()
    
    try {
        # Default behavior: Jump
        if (-not $cmd) {
            python -m teleport.cli jump --interactive --output-file $tmp_file
        } else {
            python -m teleport.cli jump $args --output-file $tmp_file
        }

        if ($LASTEXITCODE -eq 0 -and (Test-Path $tmp_file)) {
            $result = Get-Content $tmp_file -Raw
            if ($result -match "^CD:(.*)") {
                $target = $matches[1].Trim()
                if (Test-Path $target -PathType Container) {
                    Set-Location $target
                }
            } elseif ($result -match "^CMD:(.*)") {
                $command = $matches[1].Trim()
                Invoke-Expression $command
            }
        }
    } finally {
        if (Test-Path $tmp_file) {
            Remove-Item $tmp_file -ErrorAction SilentlyContinue
        }
    }
}
