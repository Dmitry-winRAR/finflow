# FinFlow QA

QA automation project for a fintech REST API.

The project demonstrates API testing, database testing, integration testing and automated test execution in CI.

## Tech Stack

* Python 3.13
* Pytest
* FastAPI
* PostgreSQL 16
* Psycopg
* Docker / Docker Compose
* GitHub Actions

## What is Tested

### API Testing

* API availability
* User creation
* User retrieval
* Non-existent users
* Deposit transactions
* Withdrawal transactions
* Invalid transaction types
* Negative transaction amounts
* Insufficient balance
* Unknown users

### Database Testing

* PostgreSQL connection
* `users` table
* `transactions` table
* User creation in the database
* User balance updates after transactions

### Integration Testing

The project verifies the complete flow between the API and PostgreSQL database.

Examples:

* Create a user through the API → verify the user in PostgreSQL
* Create a deposit → verify the balance in PostgreSQL
* Create a withdrawal → verify the balance in PostgreSQL

## Project Structure

```text
finflow-qa/
├── .github/
│   └── workflows/
│       └── tests.yml
├── db/
│   └── init.sql
├── src/
│   ├── __init__.py
│   ├── database.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_database.py
│   ├── test_integration.py
│   ├── test_transaction_integration.py
│   ├── test_withdrawal_integration.py
│   └── test_smoke.py
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

## Running the Project

### 1. Start PostgreSQL

```bash
docker compose up -d
```

### 2. Activate virtual environment

Windows:

```cmd
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run tests

```bash
pytest -v
```

## Test Results

The current test suite contains **20 automated tests** covering API, database and integration scenarios.

All tests pass locally and in GitHub Actions.

## CI

GitHub Actions automatically runs the test suite on:

* push to `main`
* pull requests to `main`

The CI pipeline:

1. Starts PostgreSQL
2. Initializes the database schema
3. Installs Python dependencies
4. Runs the automated tests

## Future Improvements

Planned areas for further development:

* Apache Kafka testing
* Security testing
* Additional API scenarios
* Test reporting
* Improved test data management
* API documentation
