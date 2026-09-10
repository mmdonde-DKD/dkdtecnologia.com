@echo off
setlocal EnableDelayedExpansion
title DKD Tecnologia - Apresentacao
cd /d "%~dp0"

echo.
echo   ============================================================
echo    DKD TECNOLOGIA E INOVACAO - apresentacao
echo    Tecnologia que impulsiona na busca pelo novo
echo   ============================================================
echo.

rem ---- acha um Python para servir a pasta -------------------------------
set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY ( where python >nul 2>&1 && set "PY=python" )
if not defined PY ( where python3 >nul 2>&1 && set "PY=python3" )

if not defined PY (
  echo   Nao achei o Python nesta maquina.
  echo.
  echo   Sem ele, abra o arquivo abaixo com dois cliques - funciona igual,
  echo   so os portais Asset e Portal Integrado e que precisam do servidor:
  echo.
  echo       DKD_Site_Institucional_previa.html
  echo.
  pause
  exit /b 1
)

rem ---- procura uma porta livre -----------------------------------------
set "PORTA="
for %%P in (8321 8322 8323 8324 8325) do (
  if not defined PORTA (
    netstat -ano ^| findstr /r /c:":%%P .*LISTENING" >nul 2>&1
    if errorlevel 1 set "PORTA=%%P"
  )
)
if not defined PORTA set "PORTA=8321"

echo   Servindo esta pasta em http://localhost:%PORTA%
echo.
echo   O navegador abre sozinho em alguns segundos.
echo   Para encerrar a apresentacao, feche esta janela preta.
echo.

start "" "http://localhost:%PORTA%/DKD_Site_Institucional_previa.html"
%PY% -m http.server %PORTA% --bind 127.0.0.1

endlocal
