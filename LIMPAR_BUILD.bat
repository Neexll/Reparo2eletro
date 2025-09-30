@echo off
echo ============================================================
echo      LIMPAR ARQUIVOS DE BUILD
echo ============================================================
echo.
echo Este script remove todas as pastas de build anteriores.
echo Use caso BUILD_EXECUTAVEL.bat de erro de "acesso negado".
echo.
pause

cd /d "%~dp0"

echo.
echo Limpando pastas...
echo.

if exist build (
    echo Removendo build\...
    rmdir /s /q build 2>nul
    if exist build (
        echo [AVISO] build\ nao pode ser removida ^(em uso^)
    ) else (
        echo [OK] build\ removida
    )
)

if exist dist (
    echo Removendo dist\...
    rmdir /s /q dist 2>nul
    if exist dist (
        echo [AVISO] dist\ nao pode ser removida ^(em uso^)
    ) else (
        echo [OK] dist\ removida
    )
)

if exist dist_servidor (
    echo Removendo dist_servidor\...
    rmdir /s /q dist_servidor 2>nul
    if exist dist_servidor (
        echo [AVISO] dist_servidor\ nao pode ser removida ^(em uso^)
        echo.
        echo DICA: Feche o Windows Explorer e tente novamente
    ) else (
        echo [OK] dist_servidor\ removida
    )
)

echo.
echo ============================================================
echo              LIMPEZA CONCLUIDA!
echo ============================================================
echo.
echo Agora voce pode executar: BUILD_EXECUTAVEL.bat
echo.
pause
