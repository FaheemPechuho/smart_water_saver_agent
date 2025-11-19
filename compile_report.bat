@echo off
REM Compile LaTeX report to PDF (Windows)

echo Compiling Smart Water Saver Agent Report...
echo.

REM Check if pdflatex is available
where pdflatex >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pdflatex not found!
    echo.
    echo Please install a LaTeX distribution:
    echo - MiKTeX: https://miktex.org/download
    echo - TeX Live: https://www.tug.org/texlive/
    echo.
    pause
    exit /b 1
)

REM Compile (run twice for TOC and references)
echo First compilation pass...
pdflatex -interaction=nonstopmode project_report.tex

echo.
echo Second compilation pass (for TOC)...
pdflatex -interaction=nonstopmode project_report.tex

REM Clean up auxiliary files
echo.
echo Cleaning up auxiliary files...
del project_report.aux 2>nul
del project_report.log 2>nul
del project_report.out 2>nul
del project_report.toc 2>nul

echo.
echo ========================================
echo Compilation complete!
echo Output: project_report.pdf
echo ========================================
echo.

REM Open PDF if it exists
if exist project_report.pdf (
    echo Opening PDF...
    start project_report.pdf
) else (
    echo ERROR: PDF was not generated. Check for LaTeX errors above.
)

pause

