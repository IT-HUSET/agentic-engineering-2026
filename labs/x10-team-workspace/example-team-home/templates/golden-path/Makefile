TEST_CMD ?= echo "Replace TEST_CMD with the repo's test command" >&2; false

.PHONY: check setup
check:
	gitleaks dir --redact --no-banner .
	$(TEST_CMD)

setup:
	claude plugin marketplace add betala/team-home
	claude plugin install team-tools@betala-team --scope project
