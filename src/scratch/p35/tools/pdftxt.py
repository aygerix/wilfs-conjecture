"""Extract text from a PDF (data only) to a .txt file.  Usage: python -I pdftxt.py IN.pdf OUT.txt"""
import sys
import pypdf
r = pypdf.PdfReader(sys.argv[1])
with open(sys.argv[2], 'w') as f:
    for i, p in enumerate(r.pages):
        f.write("\n=== page %d ===\n" % (i + 1)); f.write(p.extract_text() or "")
