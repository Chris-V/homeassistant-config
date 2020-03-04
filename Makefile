ifneq (,)
.error This Makefile requires GNU Make.
endif

.PHONY: lint _lint-cr _lint-crlf _lint-trailing-single-newline _lint-trailing-space _lint-utf8 _lint-utf8-bom

CURRENT_DIR = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

FL_VERSION      = latest
FL_IGNORE_PATHS = .git/,.github/,.vscode/

lint: _lint-files _lint-yaml

_lint-files: _pull-fl
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint file-cr --text --ignore '$(FL_IGNORE_PATHS)' --path .
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint file-crlf --text --ignore '$(FL_IGNORE_PATHS)' --path .
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint file-trailing-single-newline --text --ignore '$(FL_IGNORE_PATHS)' --path .
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint file-trailing-space --text --ignore '$(FL_IGNORE_PATHS)' --path .
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint file-utf8 --text --ignore '$(FL_IGNORE_PATHS)' --path .
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint file-utf8-bom --text --ignore '$(FL_IGNORE_PATHS)' --path .

_lint-yaml:
	@docker run --rm $$(tty -s && echo "-it" || echo) -v $(CURRENT_DIR):/data cytopia/yamllint:latest . -s

_pull-fl:
	docker pull cytopia/file-lint:$(FL_VERSION)
