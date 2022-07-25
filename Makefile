
test: 
	maturin develop
	pytest

typecheck:
	mypy 

tidy/fix:
	isort --profile black python tests
	black python tests

tidy/check:
	isort --profile black --check python tests
	black --check python tests

check: tidy/check typecheck test
	