# LaTeX Report Compilation Guide

This guide helps you compile the `project_report.tex` file into a professional PDF document.

## Prerequisites

You need a LaTeX distribution installed on your system.

### Windows

**Option 1: MiKTeX (Recommended)**
1. Download from: https://miktex.org/download
2. Run the installer
3. During installation, select "Always install missing packages on-the-fly"

**Option 2: TeX Live**
1. Download from: https://www.tug.org/texlive/acquire-netinstall.html
2. Run the installer (this is large, ~4GB)

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install texlive-full
```

For minimal installation (faster):
```bash
sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

### macOS

**Option 1: MacTeX**
```bash
brew install --cask mactex
```

**Option 2: BasicTeX (smaller)**
```bash
brew install --cask basictex
```

## Compilation Methods

### Method 1: Using Compilation Scripts (Easiest)

**Windows:**
```cmd
compile_report.bat
```

**Linux/Mac:**
```bash
chmod +x compile_report.sh
./compile_report.sh
```

This will:
- Compile the LaTeX document (twice for proper TOC generation)
- Clean up auxiliary files
- Open the PDF automatically

### Method 2: Manual Compilation

**Command Line:**
```bash
pdflatex project_report.tex
pdflatex project_report.tex  # Run twice for TOC
```

**VS Code with LaTeX Workshop Extension:**
1. Install "LaTeX Workshop" extension
2. Open `project_report.tex`
3. Press `Ctrl+Alt+B` (or `Cmd+Option+B` on Mac)

**TeXstudio / TeXmaker:**
1. Open `project_report.tex`
2. Press F5 or click the "Build & View" button

### Method 3: Online (No Installation Required)

**Overleaf:**
1. Go to https://www.overleaf.com/
2. Create a free account
3. Click "New Project" → "Upload Project"
4. Upload `project_report.tex`
5. Click "Recompile"

## Output

After successful compilation, you'll get:
- **`project_report.pdf`** - Your final report (this is what you submit!)

Auxiliary files (auto-cleaned by scripts):
- `project_report.aux` - Auxiliary file
- `project_report.log` - Compilation log
- `project_report.out` - Hyperref outlines
- `project_report.toc` - Table of Contents

## Troubleshooting

### "pdflatex: command not found"

**Solution:** LaTeX is not installed or not in PATH. Install a LaTeX distribution (see Prerequisites above).

### Missing Packages Error

If you see errors like `! LaTeX Error: File 'xyz.sty' not found`:

**MiKTeX (Windows):**
- If you selected auto-install during setup, MiKTeX will download packages automatically
- Otherwise, open "MiKTeX Console" → "Packages" → Search and install missing package

**TeX Live (Linux/Mac):**
```bash
sudo tlmgr install <package-name>
```

**Common packages needed:**
- tikz (usually in `texlive-pictures` or `texlive-latex-extra`)
- booktabs
- longtable
- hyperref
- listings

### Compilation Errors

1. **Check the log file**: Look at `project_report.log` for detailed errors
2. **Line numbers**: Error messages show line numbers (e.g., `l.123`)
3. **Common issues**:
   - Unescaped special characters: `# $ % & _ { }`
   - Missing `\end{...}` for environments
   - Mismatched braces `{ }`

### PDF Not Generated

1. Check for errors in the console output
2. Look at `project_report.log` for details
3. Try compiling twice (some errors resolve on second pass)

## Customization

### Change Document Information

Edit these lines in `project_report.tex`:

```latex
\author{
    Your Name \\
    Your ID \\
    Software Project Management (SPM)
}
```

### Add Your University Logo

1. Add your logo image to the project folder (e.g., `logo.png`)
2. In the title page section, add:
```latex
\begin{center}
\includegraphics[width=3cm]{logo.png}
\end{center}
```

### Adjust Margins

Change this line:
```latex
\usepackage[margin=1in]{geometry}
```

To:
```latex
\usepackage[top=1in, bottom=1in, left=1.5in, right=1in]{geometry}
```

## Document Structure

The report includes:

1. **Title Page** - Project information and abstract
2. **Table of Contents** - Auto-generated
3. **10 Main Sections**:
   - Introduction
   - Project Management (WBS, Schedule, Risks)
   - System Architecture
   - Memory Strategy
   - API Contract
   - Implementation Details
   - Testing & Validation
   - Deployment
   - Integration with Supervisor
   - Conclusion
4. **References** - Hyperlinked
5. **Appendices** - Code samples and test results

## Features

✅ Professional academic formatting  
✅ Automatic table of contents  
✅ Hyperlinked references and sections  
✅ Syntax-highlighted code blocks  
✅ TikZ diagrams for architecture  
✅ Tables with booktabs styling  
✅ Color-coded status indicators  
✅ 20+ pages of comprehensive documentation  

## PDF Preview

After compilation, the PDF will include:
- Professional title page with abstract
- Clickable table of contents
- Color-coded architecture diagrams
- Formatted code listings (Python & JSON)
- Tables with professional styling
- Complete project documentation

## Quick Reference

| Task | Command |
|------|---------|
| Compile | `pdflatex project_report.tex` |
| View PDF | Open `project_report.pdf` |
| Clean | `rm *.aux *.log *.out *.toc` (Linux/Mac) |
| | `del *.aux *.log *.out *.toc` (Windows) |

## Need Help?

1. **LaTeX Errors**: Check the `.log` file for detailed error messages
2. **Package Issues**: Make sure you have `texlive-full` or equivalent
3. **Online Alternative**: Use Overleaf if local compilation fails

## Submission

For your SPM course submission:
- ✅ Submit: `project_report.pdf`
- ✅ Optionally include: `project_report.tex` (source file)

---

**Estimated Compilation Time**: 10-30 seconds  
**Output Size**: ~200-300 KB (PDF)  
**Pages**: 20+ pages

Good luck with your submission! 📄✨

