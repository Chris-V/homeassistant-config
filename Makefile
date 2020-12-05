ifneq (,)
.error This Makefile requires GNU Make.
endif

.PHONY: lint _pull-file-lint _pull-yaml-lint _lint-files _lint-yaml

CURRENT_DIR       = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

FILE_LINT_VERSION = 0.4
YAML_LINT_VERSION = 1.25
LINT_IGNORE_PATHS = .git/,.github/,.vscode/

lint: _lint-files _lint-yaml

_pull-file-lint:
	docker pull cytopia/file-lint:$(FILE_LINT_VERSION)

_pull-yaml-lint:
	docker pull cytopia/yamllint:$(YAML_LINT_VERSION)

_lint-files: _pull-file-lint
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint:$(FILE_LINT_VERSION) file-cr --text --ignore '$(LINT_IGNORE_PATHS)' --path .
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint:$(FILE_LINT_VERSION) file-crlf --text --ignore '$(LINT_IGNORE_PATHS)' --path .
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint:$(FILE_LINT_VERSION) file-trailing-single-newline --text --ignore '$(LINT_IGNORE_PATHS)' --path .
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint:$(FILE_LINT_VERSION) file-trailing-space --text --ignore '$(LINT_IGNORE_PATHS)' --path .
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint:$(FILE_LINT_VERSION) file-utf8 --text --ignore '$(LINT_IGNORE_PATHS)' --path .
	@docker run --rm -v $(CURRENT_DIR):/data cytopia/file-lint:$(FILE_LINT_VERSION) file-utf8-bom --text --ignore '$(LINT_IGNORE_PATHS)' --path .

_lint-yaml: _pull-yaml-lint
	@docker run --rm $$(tty -s && echo "-it" || echo) -v $(CURRENT_DIR):/data cytopia/yamllint:$(YAML_LINT_VERSION) . -s
