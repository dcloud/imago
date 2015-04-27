echo "Testing against: ${DATABASE_TEST_URL:?"Must export to set a DATABASE_TEST_URL env variable to test against."}"

py.test --reuse-db --cov imago --cov-config=.coveragerc