# Install AI Coding Assistants Script
# Installs Codeium, GitHub Copilot, and related extensions

Write-Host "=== Installing AI Coding Assistants ===" -ForegroundColor Cyan
Write-Host ""

# Check if VS Code/Cursor is installed
$codeCommand = Get-Command code -ErrorAction SilentlyContinue
if (-not $codeCommand) {
    Write-Host "❌ VS Code/Cursor 'code' command not found" -ForegroundColor Red
    Write-Host "Please install VS Code or Cursor and add to PATH" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ VS Code/Cursor found" -ForegroundColor Green
Write-Host ""

# Extensions to install
$extensions = @(
    "Codeium.codeium",
    "GitHub.copilot",
    "GitHub.copilot-chat"
)

Write-Host "Installing extensions..." -ForegroundColor Yellow
Write-Host ""

foreach ($extension in $extensions) {
    Write-Host "Installing: $extension" -ForegroundColor Cyan
    $result = code --install-extension $extension 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $extension installed successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠️  $extension installation had issues" -ForegroundColor Yellow
        Write-Host $result
    }
    Write-Host ""
}

Write-Host "=== Installation Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart VS Code/Cursor" -ForegroundColor White
Write-Host "2. Sign in to Codeium (free account)" -ForegroundColor White
Write-Host "3. Sign in to GitHub Copilot (if you have subscription)" -ForegroundColor White
Write-Host "4. Start using AI assistants!" -ForegroundColor White
Write-Host ""
Write-Host "Shortcuts:" -ForegroundColor Yellow
Write-Host "- Codeium Chat: Ctrl+Shift+L" -ForegroundColor White
Write-Host "- Copilot Chat: Ctrl+Shift+L" -ForegroundColor White
Write-Host "- Accept suggestion: Tab" -ForegroundColor White
Write-Host "- Reject suggestion: Esc" -ForegroundColor White
Write-Host ""
