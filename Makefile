.PHONY: all html text pdf expand validate validate-examples check-draft archive-draft idnits clean help

DRAFT=$(shell sed -n 's/.*docName="\([^"]*\)".*/\1/p' draft.xml | head -n1)
XML=draft.xml
EXPANDED=draft-expanded.xml
HTML=$(DRAFT).html
TEXT=$(DRAFT).txt
PDF=$(DRAFT).pdf
LEGACY_HTML=draft-singla-aip-00.html draft.html
LEGACY_TEXT=draft-singla-aip-00.txt draft.txt
LEGACY_PDF=draft.pdf

SECTIONS := $(wildcard sections/*.xml)
REFS := $(wildcard references/*.xml)

all: html text

expand: $(EXPANDED)

$(EXPANDED): $(XML) $(SECTIONS) $(REFS) build_draft.py
	python3 build_draft.py --input $(XML) --output $(EXPANDED) --validate

html: $(HTML)

text: $(TEXT)

pdf: $(PDF)

$(HTML): $(EXPANDED)
	xml2rfc $(EXPANDED) --html -o $(HTML)
	@echo "✓ Generated $(HTML)"

$(TEXT): $(EXPANDED)
	xml2rfc $(EXPANDED) --text -o $(TEXT)
	@echo "✓ Generated $(TEXT)"

$(PDF): $(EXPANDED)
	xml2rfc $(EXPANDED) --pdf -o $(PDF)
	@echo "✓ Generated $(PDF)"

validate: $(EXPANDED)
	@xmllint --noout $(EXPANDED) && echo "✓ XML is well-formed"

validate-examples:
	python3 scripts/validate_examples.py

check-draft:
	python3 scripts/check_draft_consistency.py

archive-draft: $(EXPANDED) $(HTML) $(TEXT)
	python3 scripts/archive_current_draft.py

idnits: $(TEXT)
	@if ! command -v idnits >/dev/null 2>&1; then \
		echo "idnits not installed."; \
		echo "  Install: https://github.com/ietf-tools/idnits"; \
		echo "  Or use online: https://tools.ietf.org/tools/idnits/"; \
		exit 1; \
	fi
	idnits --mode submission $(TEXT)

clean:
	rm -f $(EXPANDED) $(HTML) $(TEXT) $(PDF) $(LEGACY_HTML) $(LEGACY_TEXT) $(LEGACY_PDF)
	@echo "✓ Cleaned build artifacts"

help:
	@echo "AIP RFC Build Targets:"
	@echo "  make all       - Build HTML and TEXT (default)"
	@echo "  make expand    - Resolve XIncludes into $(EXPANDED)"
	@echo "  make html      - Build HTML output"
	@echo "  make text      - Build TEXT output"
	@echo "  make pdf       - Build PDF output"
	@echo "  make validate  - Validate expanded XML with xmllint"
	@echo "  make validate-examples - Validate example JSON against schemas/"
	@echo "  make check-draft - Check draft numbering and archive consistency"
	@echo "  make archive-draft - Archive current draft into drafts/"
	@echo "  make idnits    - Run idnits IETF compliance check on $(TEXT)"
	@echo "  make clean     - Remove build artifacts"
	@echo ""
	@echo "Pipeline: $(XML) --[build_draft.py]--> $(EXPANDED) --[xml2rfc]--> output"
	@echo ""
	@echo "Requirements:"
	@echo "  - Python 3 with lxml (pip install lxml)"
	@echo "  - xml2rfc (pip install xml2rfc)"
	@echo "  - jsonschema (pip install jsonschema)"
	@echo "  - For PDF: weasyprint (pip install weasyprint)"
	@echo "  - For idnits: https://github.com/ietf-tools/idnits"
