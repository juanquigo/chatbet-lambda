# ChatBet Lambda

ChatBet Lambda is an API developed with **FastAPI** that manages sports betting information through different providers. It uses a modular system with routers, providers, and mappers to efficiently handle data and queries.

## **Run with Docker**

If you prefer to run the project in Docker, use the following commands:

```sh
$ docker pull juanquigo/chatbet-lambda
$ docker run -p 8000:8000 juanquigo/chatbet-lambda
```

## Installation

### **Requirements**

- Python 3.8 or higher
- pip (Python package manager)
- Virtualenv (optional but recommended)

### **Creating a `.env` File**

Before running the application, create a `.env` file in the root directory and add the required environment variables:

```
# .env file example
APP_NAME="ChatBet"
PROVIDERS__DIGITAIN__BASE_URL="askForMe"

```

This file is used to store sensitive configuration settings securely.

### **Installation and Execution Steps**

```sh
# Clone the repository
$ git clone https://github.com/juanquigo/chatbet-lambda.git
$ cd chatbet-lambda

# Create a virtual environment (optional but recommended)
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
$ pip install -r requirements.txt

# Run the application
$ fastapi dev
```

### **Swagger**

Once the application is running, you can access the Swagger documentation at:

```
http://localhost:8000/docs
```

### **Run Tests**

You can run tests with the following command:

```
pytest --cov=app --cov-report=html --cov-config=.coveragerc
```

## **Project Structure**

```
app/
│── main.py               # Main entry point
│── settings.py           # Application configuration
│── schemas.py            # Pydantic model definitions
│
├── routers/              # Route definitions
│   ├── digitain.py       # Routes related to Digitain
│   ├── provider.py       # Provider routes
│
├── providers/            # Provider implementations
│   ├── base_provider.py  # Base class for providers
│   ├── digitain_provider.py # Implementation for Digitain
│   ├── provider_factory.py  # Provider factory
│
├── mappers/              # Data transformers
│   ├── base_mapper.py    # Base class for mappers
│   ├── digitain_mapper.py # Mapper for Digitain
│   ├── mapper_factory.py # Mapper factory
│
├── services/             # Auxiliary services
│   ├── http_client.py    # HTTP client for external calls
│   ├── odds_service.py   # Odds service
```

## **Main Endpoints**

### **1. Get Odds Information**

`GET /provider/digitain/odds`

- **Description**: Retrieves odds information from the Digitain provider.
- **Query Parameters**:
  - `match_id` (integer, required): Identifier of the match entity.
  - `tournament_id` (integer, required): Tournament identifier of that match.
  - `language_code_id` (integer, optional): Identifier of
    language.
- **Example Request:**

```
http://localhost:8000/provider/digitain/odds?match_id=24262532&tournament_id=4651&language_code_id=13
```

- **Expected Response**:

```json
{
  "status": "string",
  "main_market": "string",
  "result": {
    "homeTeam": {
      "name": "string",
      "profit": 0,
      "odds": 0,
      "betId": 0
    },
    "awayTeam": {
      "name": "string",
      "profit": 0,
      "odds": 0,
      "betId": 0
    },
    "tie": {
      "name": "string",
      "profit": 0,
      "odds": 0,
      "betId": 0
    }
  },
  "result_regular_time": null,
  "score": null,
  "both_teams_to_score": null,
  "double_chance": null,
  "over_under": {
    "over": {
      "name": "string",
      "profit": 0,
      "odds": 0,
      "betId": 0
    },
    "under": {
      "name": "string",
      "profit": 0,
      "odds": 0,
      "betId": 0
    }
  },
  "handicap": {
    "homeTeam": {
      "name": "string",
      "profit": 0,
      "odds": 0,
      "betId": 0
    },
    "awayTeam": {
      "name": "string",
      "profit": 0,
      "odds": 0,
      "betId": 0
    }
  },
  "half_time_total": null,
  "half_time_result": null,
  "half_time_handicap": null,
  "win": null
}
```

---

You're all set! Now you can start using ChatBet Lambda 🚀
