# Minimal LaTeX Makefile (single pass) with live filtered logs
# Usage:
#   make           # build once; see filtered warnings/errors
#   make clean     # remove aux files
#   make distclean # remove aux + PDF

SHELL := /bin/bash

# ---- Config ----
MAIN      ?= presentation
BUILD     ?= build
ENGINE    ?= pdflatex
TEXFLAGS  ?= -interaction=nonstopmode -file-line-error -recorder -synctex=1 -output-directory=$(BUILD)
LOGFILTER ?= texlogfilter
TF_OPTS   ?= --filename --no-info --box

# ---- Files ----
PDF  := $(BUILD)/$(MAIN).pdf
LOG  := $(BUILD)/$(MAIN).log
RERUN_SENT := $(BUILD)/.rerun_required

SRC      := $(MAIN).tex
SECTIONS := $(wildcard sections/*.tex)
IMAGES   := $(wildcard img/*.png) $(wildcard img/*.jpg) $(wildcard img/*.jpeg) $(wildcard img/*.pdf) $(wildcard img/*.eps) $(wildcard img/*.svg)

.PHONY: all pdf clean distclean
all: pdf
pdf: $(PDF)

# Rebuild when sources change OR when the sentinel exists/newer
$(PDF): $(SRC) $(SECTIONS) $(IMAGES) $(wildcard $(RERUN_SENT)) | $(BUILD)
	$(ENGINE) $(TEXFLAGS) $(MAIN).tex </dev/null |& $(LOGFILTER) $(TF_OPTS)
	@if grep -Eq 'Rerun to get cross-references right|Label\(s\) may have changed|There were undefined citations|Please \(re\)run (Biber|BibTeX)|Rerun BibTeX' "$(LOG)"; then \
	  echo "----"; \
	  echo "Note: LaTeX suggests another run (refs/citations changed). Run 'make' again."; \
	  touch "$(RERUN_SENT)"; \
	else \
	  rm -f "$(RERUN_SENT)"; \
	fi
	@test -f "$(PDF)"

$(BUILD):
	mkdir -p "$(BUILD)"

clean:
	@rm -f $(BUILD)/$(MAIN).{aux,bbl,bcf,blg,idx,ilg,ind,lof,log,lot,out,toc,fdb_latexmk,fls,synctex.gz,nav,snm,vrb,run.xml} || true
	@rm -f "$(RERUN_SENT)" || true

distclean: clean
	@rm -f "$(PDF)" || true

