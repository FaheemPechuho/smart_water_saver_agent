#!/bin/bash
# Compile LaTeX report to PDF (Linux/Mac)

echo "Compiling Smart Water Saver Agent Report..."
echo ""

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "ERROR: pdflatex not found!"
    echo ""
    echo "Please install a LaTeX distribution:"
    echo "  Ubuntu/Debian: sudo apt install texlive-full"
    echo "  macOS: brew install --cask mactex"
    echo ""
    exit 1
fi

# Compile (run twice for TOC and references)
echo "First compilation pass..."
pdflatex -interaction=nonstopmode project_report.tex

echo ""
echo "Second compilation pass (for TOC)..."
pdflatex -interaction=nonstopmode project_report.tex

# Clean up auxiliary files
echo ""
echo "Cleaning up auxiliary files..."
rm -f project_report.aux project_report.log project_report.out project_report.toc

echo ""
echo "========================================"
echo "Compilation complete!"
echo "Output: project_report.pdf"
echo "========================================"
echo ""

# Open PDF if it exists
if [ -f "project_report.pdf" ]; then
    echo "Opening PDF..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open project_report.pdf
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open project_report.pdf 2>/dev/null || echo "Please open project_report.pdf manually"
    fi
else
    echo "ERROR: PDF was not generated. Check for LaTeX errors above."
fi

