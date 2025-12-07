@echo off
chcp 65001 > nul
echo.
echo ============================================
echo   🚀 Soul LLM Rules - 一键分发工具
echo ============================================
echo.
echo 📋 此脚本将执行以下操作
echo    2️⃣  分发规则到各个目标 [cursor/claude等]
echo.

echo ────────────────────────────────────────────
echo 📤 [步骤 1/1] 分发规则...
echo ────────────────────────────────────────────
python distribute_rules.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ 规则分发失败
    exit /b 1
)

echo.
echo ============================================
echo   ✅ 所有操作完成！规则已更新!
echo ============================================

@echo on
pause
