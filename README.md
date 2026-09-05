# FinFlow QA

QA automation project for a fintech REST API.

The project demonstrates automated API testing, PostgreSQL database testing, integration testing, security testing and CI execution using Python and Pytest.

## Tech Stack

* Python 3.13
* Pytest
* FastAPI
* PostgreSQL 16
* Psycopg
* Apache Kafka
* Docker / Docker Compose
* GitHub Actions
* Git

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

### Security Testing

The project includes basic API authorization checks:

* Access to user data without authentication
* IDOR-style access to another user's data
* Validation of `X-User-Id` authorization header

### Database Testing

* PostgreSQL connection
* `users` table
* `transactions` table
* User creation in the database
* User balance updates after transactions

### Integration Testing

The project verifies complete flows between the REST API and PostgreSQL database.

Examples:

* Create a user through the API → verify the user in PostgreSQL
* Create a deposit → verify the updated balance in PostgreSQL
* Create a withdrawal → verify the updated balance in PostgreSQL

### Kafka

Apache Kafka is integrated into the application for publishing transaction events.

The application publishes a `transaction.created` event after a successful transaction.

Kafka is included as part of the project architecture and Docker environment.

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
│   ├── kafka.py
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

### 1. Start Docker services

```bash
docker compose up -d
```

This starts the PostgreSQL and Kafka containers.

### 2. Activate the virtual environment

Windows:

```cmd
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the tests

```bash
pytest -v
```

## Test Results

The current test suite contains **22 automated tests** covering:

* API testing
* Database testing
* Integration testing
* Security testing
* Smoke testing

All tests pass locally and in GitHub Actions.

```text
22 passed
```

## CI/CD

GitHub Actions automatically runs the test suite on:

* Pushes to `main`
* Pull requests to `main`

The CI pipeline:

1. Starts PostgreSQL
2. Initializes the database schema
3. Installs Python dependencies
4. Runs the automated test suite

The current CI pipeline successfully executes all 22 tests.

## Project Goals

The project was created to practice and demonstrate:

* REST API automation
* Database validation with PostgreSQL
* Integration testing
* Security testing
* Event-driven architecture with Kafka
* Docker-based test environments
* CI/CD automation
* Python and Pytest

## Future Improvements

Possible areas for further development:

* Expanded Kafka integration testing
* API test reporting
* Improved test data management
* Additional negative API scenarios
* Authentication and authorization improvements
* API documentation
