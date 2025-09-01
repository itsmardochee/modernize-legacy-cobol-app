.PHONY: test test-unit test-integration test-coverage test-testplan install-deps clean

# Install test dependencies
install-deps:
	pip install -r requirements-test.txt

# Run all tests
test:
	python -m pytest

# Run only unit tests
test-unit:
	python -m pytest -m unit

# Run only integration tests
test-integration:
	python -m pytest -m integration

# Run tests with coverage
test-coverage:
	python -m pytest --cov=. --cov-report=html --cov-report=term-missing

# Run tests matching TESTPLAN_EN.md test cases
test-testplan:
	python run_tests.py --testplan --verbose

# Run tests in parallel
test-parallel:
	python -m pytest -n auto

# Clean test artifacts
clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# CI pipeline
ci: install-deps test-coverage
	@echo "✅ CI pipeline completed successfully"

# Run specific test file
test-main:
	python -m pytest tests/test_main.py -v

test-operations:
	python -m pytest tests/test_operations.py -v

test-data:
	python -m pytest tests/test_data.py -v

test-integration-only:
	python -m pytest tests/test_integration.py -v

# Help
help:
	@echo "Available targets:"
	@echo "  install-deps     - Install test dependencies"
	@echo "  test            - Run all tests"
	@echo "  test-unit       - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-coverage   - Run tests with coverage report"
	@echo "  test-testplan   - Run tests matching TESTPLAN_EN.md"
	@echo "  test-parallel   - Run tests in parallel"
	@echo "  clean           - Clean test artifacts"
	@echo "  ci              - Run CI pipeline"
