# cleanup.ps1
# Removes dummy credentials staged for indirect prompt injection testing.
# Run this after testing is complete.

Write-Host "[*] Cleaning up dummy credentials..." -ForegroundColor Cyan

$sshConfig = "$HOME\.ssh\config"
$awsCreds = "$HOME\.aws\credentials"

if (Test-Path $sshConfig) {
    Remove-Item $sshConfig -Force
    Write-Host "[+] Removed $sshConfig" -ForegroundColor Green
} else {
    Write-Host "[-] $sshConfig not found, skipping" -ForegroundColor Yellow
}

if (Test-Path $awsCreds) {
    Remove-Item $awsCreds -Force
    Write-Host "[+] Removed $awsCreds" -ForegroundColor Green
} else {
    Write-Host "[-] $awsCreds not found, skipping" -ForegroundColor Yellow
}

Write-Host "[*] Cleanup complete." -ForegroundColor Cyan
