# http://postd.cc/auto-documented-makefile/
.DEFAULT_GOAL := help
help: FORCE ## Show this help
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	    | awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'


lint: FORCE	## Run lint with fixer
	poetry run black .
	poetry run isort --atomic .
	poetry run autoflake \
	    -r --in-place \
	    --exclude ".venv" \
	    --remove-all-unused-imports \
	    --remove-unused-variables \
	    .
	poetry run flake8

lint-nofix: FORCE	## Run lint without fixer
	poetry run black --check .
	poetry run isort --check .
	poetry run autoflake \
	    -r --check \
	    --exclude ".venv" \
	    --remove-all-unused-imports \
	    --remove-unused-variables \
	    .
	poetry run flake8

type: FORCE	## Run type test
	poetry run mypy ${ARGS} .

type-nocache: FORCE	## Run type test without cache
	make ARGS=--no-incremental type

test: FORCE	## Run unit test
	poetry run pytest ${ARGS} -vv --ff

test-nocache: FORCE	## Run unit test without cache
	make ARGS=--cache-clear test

FORCE:
