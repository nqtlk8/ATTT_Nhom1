# Script để kích hoạt virtual environment trên Windows PowerShell
# Cách sử dụng: .\activate_venv.ps1

Write-Host "=== Kích hoạt Virtual Environment ===" -ForegroundColor Green

# Kiểm tra venv đã tồn tại chưa
if (-Not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment chưa được tạo!" -ForegroundColor Red
    Write-Host "Đang tạo virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Bypass Execution Policy cho session hiện tại
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Kích hoạt venv
Write-Host "Đang kích hoạt virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

if ($LASTEXITCODE -eq 0 -or $env:VIRTUAL_ENV) {
    Write-Host "✓ Virtual environment đã được kích hoạt!" -ForegroundColor Green
    Write-Host "Python path: $($(Get-Command python).Source)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Để thoát venv, gõ: deactivate" -ForegroundColor Gray
} else {
    Write-Host "✗ Không thể kích hoạt virtual environment!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Thử các cách sau:" -ForegroundColor Yellow
    Write-Host "1. Dùng Command Prompt: venv\Scripts\activate.bat" -ForegroundColor White
    Write-Host "2. Chạy PowerShell với quyền Administrator" -ForegroundColor White
    Write-Host "3. Set Execution Policy: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor White
}

