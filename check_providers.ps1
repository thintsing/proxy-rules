function Invoke-MihomoApi($method, $path) {
    $pipe = New-Object System.IO.Pipes.NamedPipeClientStream('.', 'verge-mihomo', [System.IO.Pipes.PipeDirection]::InOut)
    $pipe.Connect(5000)
    $request = "$method $path HTTP/1.1`r`nHost: localhost`r`nAuthorization: Bearer set-your-secret`r`nConnection: close`r`n`r`n"
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($request)
    $pipe.Write($bytes, 0, $bytes.Length)
    $pipe.Flush()
    $reader = New-Object System.IO.StreamReader($pipe)
    $response = $reader.ReadToEnd()
    $pipe.Close()
    return $response
}

$resp = Invoke-MihomoApi "GET" "/providers/rules"

if ($resp.Contains("`r`n`r`n")) {
    $body = ($resp -split "`r`n`r`n", 2)[1]
    $body = $body -replace "(?s)^\r?\n?[0-9a-fA-F]+\r?\n", ""
    $body = $body -replace "\r?\n0\r?\n?$", ""
    $body = $body.Trim()
    try {
        $json = $body | ConvertFrom-Json
        Write-Output "=== Rule-Provider Load Status ==="
        foreach ($name in ($json.providers.PSObject.Properties.Name | Sort-Object)) {
            $info = $json.providers.$name
            $icon = if ($info.ruleCount -gt 0) { "[OK]" } else { "[X]" }
            Write-Output ("{0} {1,-15} behavior={2,-8} rules={3}" -f $icon, $name, $info.behavior, $info.ruleCount)
        }
    } catch {
        Write-Output "JSON parse failed: $($_.Exception.Message)"
    }
} else {
    Write-Output "Malformed response"
}