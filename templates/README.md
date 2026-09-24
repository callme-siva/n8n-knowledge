# 📥 Templates & sample files

- **`<lesson>/<Tab>.csv`**: one CSV per Google Sheets tab a workflow uses. In Google Sheets: **File → Import → Upload** → *Insert new sheet(s)*; the tab takes the file's name. Columns are generated from what each workflow actually reads and writes in the [end-to-end tests](../tests/README.md), so they always match.
- **`files/`**: sample PDFs: `invoice-valid.pdf`, `invoice-large.pdf` (needs approval), `invoice-wrong-total.pdf` (fails validation), `resume-sample.pdf`, `hr-policy.pdf`. All names and companies are fictional.

[← Back to the learning path](../README.md)
