@echo off
REM ============================
REM LIMPIAR BUILDS ANTERIORES
REM ============================
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM ============================
REM CREAR scores.json VACIO SI NO EXISTE
REM ============================
if not exist resources\scores.json (
    echo { "scores": [] } > resources\scores.json
    echo ✅ Archivo resources\scores.json creado
)

REM ============================
REM COMPILAR CON PYINSTALLER
REM ============================
pyinstaller --noconfirm --clean main.spec

REM ============================
REM RESULTADO
REM ============================
if exist dist\SnakeGame\SnakeGame.exe (
    echo ✅ Build completado correctamente.
    echo El juego se encuentra en: dist\SnakeGame
    echo Comprime manualmente esa carpeta para distribuir el juego.
) else (
    echo ❌ Error: no se encontro SnakeGame.exe en dist\SnakeGame
)

pause
