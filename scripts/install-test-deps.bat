@echo off
REM Install Test Dependencies for AI Film Studio (Windows Batch)
echo === AI Film Studio - Installing Test Dependencies ===
echo.

echo 📦 Installing from requirements-test.txt...
pip install -r tests\requirements-test.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Test dependencies installed successfully!
    echo.
    echo Next steps:
    echo   pytest tests/unit/ -v
    echo   pytest tests/ --cov=src --cov-report=html
) else (
    echo.
    echo ❌ Installation failed. Please check errors above.
    exit /b 1
)

pause
