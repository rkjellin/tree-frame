
test: 
	maturin develop
	pytest

tidy/fix:
	isort --profile black python tests
	black python tests

tidy/check:
	isort --profile black --check python tests
	black --check python tests