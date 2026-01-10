# Fill Blanks App - Backend

A FastAPI-based backend service for generating AI-powered fill-in-the-blank questions. This backend uses OpenAI's GPT-4 model to create engaging, topic-specific questions and tracks user performance in an SQLite database.

## Features

- 🤖 **AI Question Generation**: Dynamically generates unique fill-in-the-blank questions using OpenAI GPT-4 via LangChain
- 📚 **Topic Management**: Supports multiple topics (Science, Technology, History) with easy extensibility
- ✅ **Answer Validation**: Validates user answers and provides instant feedback
- 📊 **Score Tracking**: Tracks scores and attempts per topic for analytics
- 💾 **Game History**: Persists all game sessions in SQLite database
- 🔒 **Type Safety**: Uses Pydantic models for request/response validation
- 🌐 **CORS Enabled**: Configured for cross-origin requests from frontend

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs with automatic OpenAPI documentation
- **SQLite**: Lightweight, file-based database for storing topics and game history
- **LangChain**: Framework for working with language models and prompts
- **OpenAI GPT-4**: AI model for generating questions (configurable via model parameter)
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications

## Project Structure

```
backend/
├── ai_q_gen/
│   └── question_generator.py    # AI question generation logic using LangChain
├── db/
│   ├── db.py                     # Database connection utilities
│   └── init_db.py                # Database initialization and schema creation
├── models/
│   └── schemas.py                # Pydantic models for request/response validation
├── main.py                       # FastAPI application entry point
├── db.sqlite3                    # SQLite database file (created automatically)
└── README.md                     # This file
```

## Prerequisites

- **Python 3.8+**
- **OpenAI API Key**: Get your API key from [OpenAI Platform](https://platform.openai.com/)

## Installation

### 1. Install Dependencies

```bash
pip install fastapi uvicorn langchain langchain-openai pydantic
```

Or create a `requirements.txt` file with the following dependencies:

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
langchain>=0.1.0
langchain-openai>=0.0.5
pydantic>=2.0.0
```

Then install:

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file or set environment variables:

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
export DB_FILE="db.sqlite3"  # Optional, defaults to db.sqlite3
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-openai-api-key-here"
$env:DB_FILE="db.sqlite3"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=your-openai-api-key-here
set DB_FILE=db.sqlite3
```

### 3. Initialize Database

The database is automatically initialized when the FastAPI app starts, but you can also initialize it manually:

```bash
python -m db.init_db
```

This will:
- Create the `topics` and `game_history` tables
- Seed initial topics (Science, Technology, History) if the table is empty

## Running the Server

### Development Mode

Run the server with auto-reload enabled:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Production Mode

For production, use multiple workers:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or with Gunicorn:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Documentation

Once the server is running, you can access interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Endpoints

#### `GET /topics`

Retrieve all available topics.

**Response:**
```json
[
  {"id": 1, "name": "Science"},
  {"id": 2, "name": "Technology"},
  {"id": 3, "name": "History"}
]
```

#### `POST /get_question`

Generate a new fill-in-the-blank question for a specific topic.

**Request Body:**
```json
{
  "topic_id": 1
}
```

**Response:**
```json
{
  "sentence": "The process of photosynthesis converts ____ into glucose.",
  "choices": "A) sunlight, B) water, C) carbon dioxide, D) oxygen",
  "answer": "A) sunlight",
  "hint": "Think about what plants need from the environment."
}
```

**Error Response:**
```json
{
  "error": "Invalid topic"
}
```

#### `POST /submit_answer`

Submit an answer for evaluation and store it in game history.

**Request Body:**
```json
{
  "topic_id": 1,
  "sentence": "The process of photosynthesis converts ____ into glucose.",
  "choices": "A) sunlight, B) water, C) carbon dioxide, D) oxygen",
  "answer": "A) sunlight",
  "hint": "Think about what plants need from the environment.",
  "user_answer": "A) sunlight"
}
```

**Response:**
```json
{
  "correct": true
}
```

#### `GET /score/{topic_id}`

Get score statistics for a specific topic.

**Response:**
```json
{
  "score": 8,
  "attempted": 10
}
```

Where:
- `score`: Total number of correct answers for this topic
- `attempted`: Total number of questions attempted for this topic

## Database Schema

### `topics` Table

Stores available question topics.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique topic identifier |
| `name` | TEXT | UNIQUE | Topic name |

### `game_history` Table

Stores all question attempts and answers.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique record identifier |
| `topic_id` | INTEGER | | Foreign key to topics table |
| `sentence` | TEXT | | The question sentence with blank |
| `choices` | TEXT | | Available answer choices |
| `answer` | TEXT | | Correct answer |
| `hint` | TEXT | | Hint for the question |
| `user_answer` | TEXT | | User's submitted answer |
| `correct` | INTEGER | | 1 if correct, 0 if incorrect |
| `timestamp` | DATETIME | DEFAULT CURRENT_TIMESTAMP | When the answer was submitted |

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key for question generation |
| `DB_FILE` | No | `db.sqlite3` | Path to the SQLite database file |

### Model Configuration

The question generator uses GPT-4 with the following settings (configurable in `ai_q_gen/question_generator.py`):

- **Model**: `gpt-4.1`
- **Temperature**: `0.9` (high creativity for varied questions)

To customize the model or temperature, edit the `generate_question` function in `ai_q_gen/question_generator.py`.

## Development

### Adding New Topics

You can add new topics in two ways:

1. **Via Database** (SQL):
   ```sql
   INSERT INTO topics (name) VALUES ('Literature');
   ```

2. **Via Code**: Edit `db/init_db.py` and add to the seed data:
   ```python
   cur.executemany(
       "INSERT INTO topics (name) VALUES (?)",
       [("Science",), ("Technology",), ("History",), ("Literature",)]
   )
   ```

### Customizing Question Format

The question generation prompt can be customized in `ai_q_gen/question_generator.py`. The current template:

- Generates a sentence with one blank (____)
- Provides four multiple choice options (separated by commas)
- Includes the correct answer
- Provides a helpful hint

Example prompt modification:
```python
prompt = ChatPromptTemplate.from_template("""
Write a challenging {topic} sentence. Hide one key concept with ____.
Provide four choices and a detailed hint. Format:
Sentence: ...
Choices: ...
Answer: ...
Hint: ...
""")
```

### Testing

To test the API endpoints, you can use:

1. **Swagger UI**: Interactive testing at `http://localhost:8000/docs`
2. **cURL**:
   ```bash
   curl -X GET "http://localhost:8000/topics"
   ```
3. **Python Requests**:
   ```python
   import requests
   response = requests.get("http://localhost:8000/topics")
   print(response.json())
   ```

## Error Handling

The API handles the following error cases:

- **Invalid Topic ID**: Returns `{"error": "Invalid topic"}` when a non-existent topic_id is provided
- **LLM Parsing Errors**: Raises exception if the AI response cannot be parsed correctly
- **Database Errors**: SQLite errors are raised and should be handled by FastAPI's error handling

## Deployment

### Docker (Recommended)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t fill-blanks-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key fill-blanks-backend
```

### Platform Deployment

The FastAPI application can be deployed on:

- **Heroku**: Use the Procfile: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Railway**: Auto-detects Python and runs `uvicorn`
- **AWS Lambda**: Use Mangum adapter
- **Google Cloud Run**: Container-based deployment
- **DigitalOcean App Platform**: Supports Python applications

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not found"**
   - Ensure the environment variable is set correctly
   - Verify the key is valid and has sufficient credits

2. **Database locked errors**
   - Ensure only one instance is writing to the database
   - Check file permissions on `db.sqlite3`

3. **LLM parsing errors**
   - The AI might return an unexpected format
   - Check the logs for the raw LLM response
   - Consider adjusting the prompt template

4. **CORS errors**
   - Ensure CORS middleware is configured correctly in `main.py`
   - For production, specify allowed origins instead of `["*"]`

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Author

**Pouria Mortezaagha**

Copyright (c) 2026 Pouria Mortezaagha
