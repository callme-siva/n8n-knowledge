"""Generate templates/: Google Sheets CSV templates (columns proven by the e2e harness) and sample PDFs."""
import csv, json, os, zlib

LEAD = ["row_id", "request_id", "invoice_no", "time", "timestamp", "logged_at", "date", "email", "name", "vendor", "company"]


def _order(cols):
    first = [c for c in LEAD if c in cols]
    return first + [c for c in cols if c not in first]


def _cell(v):
    return json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else ("" if v is None else v)


def sheet_templates(root):
    """Returns {slug: [(tab, relative_csv_path, columns)]} and writes the CSV files."""
    res_path = os.path.join(root, "tests", "results.json")
    if not os.path.exists(res_path):
        return {}
    results, out = json.load(open(res_path)), {}
    for slug, r in sorted(results.items()):
        for tab, io in (r.get("sheets") or {}).items():
            cols = []
            for row in io["reads"] + io["writes"]:
                cols += [c for c in row if c not in cols]
            cols = _order(cols)
            rows = (io["reads"] or io["writes"])[:5]
            d = os.path.join(root, "templates", slug)
            os.makedirs(d, exist_ok=True)
            path = os.path.join(d, f"{tab}.csv")
            with open(path, "w", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(cols)
                for row in rows:
                    w.writerow([_cell(row.get(c)) for c in cols])
            out.setdefault(slug, []).append((tab, f"templates/{slug}/{tab}.csv", cols))
    return out


# ---------------------------------------------------------------- tiny PDF writer (text only, Helvetica)
def _pdf(lines, path):
    def esc(t):
        return t.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    body = ["BT", "/F1 11 Tf", "14 TL", "56 790 Td"]
    for i, (text, size) in enumerate(lines):
        body += [f"/F1 {size} Tf", f"({esc(text)}) Tj", "T*"]
    body.append("ET")
    stream = zlib.compress("\n".join(body).encode("latin-1", "replace"))
    objs = ["<< /Type /Catalog /Pages 2 0 R >>", "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
            None, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"]
    out, offs = bytearray(b"%PDF-1.4\n"), []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        if o is None:
            out += f"{i} 0 obj\n<< /Length {len(stream)} /Filter /FlateDecode >>\nstream\n".encode() + stream + b"\nendstream\nendobj\n"
        else:
            out += f"{i} 0 obj\n{o}\nendobj\n".encode()
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode() + b"".join(f"{o:010d} 00000 n \n".encode() for o in offs)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    open(path, "wb").write(out)


def sample_files(root):
    d = os.path.join(root, "templates", "files")
    os.makedirs(d, exist_ok=True)
    inv = lambda no, sub, tax, total, gstin: [
        ("TAX INVOICE", 18), ("", 11), ("Acme Supplies Pvt Ltd", 12), ("12 MG Road, Bengaluru 560001", 10), (f"GSTIN: {gstin}", 10), ("", 11),
        (f"Invoice No: {no}", 11), ("Invoice Date: 01 Sep 2026", 11), ("Due Date: 01 Oct 2026", 11), ("Bill To: Finlytics Pvt Ltd", 11), ("", 11),
        ("Description                               Qty      Rate        Amount", 10),
        ("Laptop stands (aluminium)                 20       350.00      7,000.00", 10),
        ("USB-C docking stations                     2     1,500.00      3,000.00", 10), ("", 11),
        (f"Subtotal: INR {sub}", 11), (f"IGST 18%: INR {tax}", 11), (f"Grand Total: INR {total}", 13), ("", 11), ("Payment: NEFT to HDFC0001234 · A/c 50100123456789", 9)]
    _pdf(inv("INV-4411", "10,000.00", "1,800.00", "11,800.00", "29ABCDE1234F1Z5"), os.path.join(d, "invoice-valid.pdf"))
    _pdf(inv("INV-4412", "10,000.00", "1,800.00", "12,300.00", "29ABCDE1234F1Z5"), os.path.join(d, "invoice-wrong-total.pdf"))
    _pdf(inv("INV-9001", "1,00,000.00", "18,000.00", "1,18,000.00", "27PQRSX5678K1Z2"), os.path.join(d, "invoice-large.pdf"))
    _pdf([("ACME Leave & Remote Work Policy (2026)", 16), ("", 11),
          ("1. Casual leave: 12 days per calendar year, max 3 consecutive days. Unused casual leave lapses on 31 Dec.", 10),
          ("2. Earned leave: 18 days per year, carry forward up to 30 days.", 10),
          ("3. Work from home: up to 2 days per week with manager approval.", 10),
          ("   Broadband reimbursed up to $50/month with bill.", 10),
          ("4. Travel: economy class for flights under 4 hours. Hotel limit $200/night in major cities.", 10),
          ("5. Sick leave beyond 2 days requires a medical certificate.", 10)], os.path.join(d, "hr-policy.pdf"))
    _pdf([("Priya Sharma", 18), ("Scrum Master · Bengaluru · priya@example.com", 10), ("", 11), ("SUMMARY", 12),
          ("Certified Scrum Master (CSM) with 6 years in fintech; coached 4 teams through SAFe adoption.", 10), ("", 11),
          ("EXPERIENCE", 12), ("Finlytics (2022-now) - Scrum Master: cut cycle time 35%, introduced flow metrics in Jira.", 10),
          ("PayWave (2019-2022) - Agile Delivery Lead: ran PI planning for 60 people across 6 teams.", 10), ("", 11),
          ("SKILLS", 12), ("Scrum, Kanban, SAFe 5, Jira, Confluence, facilitation, OKRs, stakeholder management", 10)],
         os.path.join(d, "resume-sample.pdf"))
    return ["invoice-valid.pdf", "invoice-large.pdf", "invoice-wrong-total.pdf", "hr-policy.pdf", "resume-sample.pdf"]
