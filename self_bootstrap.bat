@echo off
chcp 65001 >NUL 2>&1
echo.
echo ============================================
echo   🔄 Self-Bootstrap - 自举分发工具
echo ============================================
echo.
echo 📋 此脚本将 skills 分发到本项目
echo    目标: .claude/skills/
echo.
echo ────────────────────────────────────────────
echo 📤 执行自举分发...
echo ────────────────────────────────────────────
python run_distribute.py configs\self_bootstrap.json
if %errorlevel% neq 0 (
    echo.
    echo ❌ 自举分发失败
    exit /b 1
)

echo.
echo ============================================
echo   ✅ 自举分发完成！
echo ============================================
echo.
pause
