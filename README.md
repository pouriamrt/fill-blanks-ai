# Fill Blanks App

An interactive quiz application that generates AI-powered fill-in-the-blank questions across multiple topics. Built with FastAPI backend and React frontend, this application uses OpenAI's GPT models to create engaging, topic-specific questions with multiple choice options.

## Features

- 🤖 **AI-Generated Questions**: Dynamically generates unique fill-in-the-blank questions using OpenAI's GPT models
- 📚 **Multiple Topics**: Choose from various topics including Science, Technology, and History
- ✅ **Score Tracking**: Track your performance with real-time score updates
- 💡 **Hint System**: Get hints when you're stuck on a question
- 📊 **Game History**: All attempts are logged in the database for future analysis
- 🎯 **Multiple Choice Format**: Questions include multiple choice options for interactive learning
- ⚡ **Fast & Responsive**: Built with modern frameworks for optimal performance

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLite**: Lightweight database for storing topics and game history
- **LangChain**: Framework for working with language models
- **OpenAI GPT-4**: AI model for generating questions
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **React 19**: Modern UI library
- **Vite**: Fast build tool and development server
- **Axios**: HTTP client for API requests
- **CSS**: Styling (inline styles)

## Project Structure

```
Fill_blanks_app/
├── backend/
│   ├── ai_q_gen/
│   │   └── question_generator.py    # AI question generation logic
│   ├── db/
│   │   ├── db.py                     # Database connection utilities
│   │   └── init_db.py                # Database initialization and schema
│   ├── models/
│   │   └── schemas.py                # Pydantic models for request/response
│   ├── main.py                       # FastAPI application entry point
│   └── db.sqlite3                    # SQLite database file
├── frontend/
│   ├── src/
│   │   ├── App.jsx                   # Main React component
│   │   ├── App.css                   # Application styles
│   │   ├── main.jsx                  # React entry point
│   │   └── index.css                 # Global styles
│   ├── package.json                  # Frontend dependencies
│   └── vite.config.js                # Vite configuration
├── LICENSE                           # MIT License
└── README.md                         # This file
```

## Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **OpenAI API Key**: Get your API key from [OpenAI Platform](https://platform.openai.com/)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Fill_blanks_app
```

### 2. Backend Setup

Navigate to the backend directory and install Python dependencies:

```bash
cd backend
pip install fastapi uvicorn langchain langchain-openai pydantic
```

Set up environment variables:

```bash
# On Linux/Mac
export OPENAI_API_KEY="your-openai-api-key-here"
export DB_FILE="db.sqlite3"  # Optional, defaults to db.sqlite3

# On Windows (PowerShell)
$env:OPENAI_API_KEY="your-openai-api-key-here"
$env:DB_FILE="db.sqlite3"
```

Initialize the database:

```bash
python -m db.init_db
```

### 3. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd ../frontend
npm install
```

## Running the Application

### Start the Backend Server

From the `backend` directory:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

You can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Start the Frontend Development Server

From the `frontend` directory:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173` (or the port shown in the terminal)

## API Endpoints

### `GET /topics`
Retrieve all available topics.

**Response:**
```json
[
  {"id": 1, "name": "Science"},
  {"id": 2, "name": "Technology"},
  {"id": 3, "name": "History"}
]
```

### `POST /get_question`
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

### `POST /submit_answer`
Submit an answer for evaluation.

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

### `GET /score/{topic_id}`
Get the score statistics for a specific topic.

**Response:**
```json
{
  "score": 8,
  "attempted": 10
}
```

## Database Schema

### `topics` Table
- `id` (INTEGER PRIMARY KEY): Unique topic identifier
- `name` (TEXT UNIQUE): Topic name

### `game_history` Table
- `id` (INTEGER PRIMARY KEY): Unique record identifier
- `topic_id` (INTEGER): Reference to topics table
- `sentence` (TEXT): The question sentence
- `choices` (TEXT): Available answer choices
- `answer` (TEXT): Correct answer
- `hint` (TEXT): Hint for the question
- `user_answer` (TEXT): User's submitted answer
- `correct` (INTEGER): 1 if correct, 0 if incorrect
- `timestamp` (DATETIME): When the answer was submitted

## How It Works

1. **Topic Selection**: Users select a topic from the available options (Science, Technology, History)
2. **Question Generation**: The backend uses LangChain and OpenAI GPT-4 to generate a unique fill-in-the-blank question based on the selected topic
3. **Question Display**: The frontend displays the question with multiple choice options
4. **Answer Submission**: Users submit their answers, which are evaluated against the correct answer
5. **Feedback & Scoring**: Instant feedback is provided, and scores are tracked in the database
6. **History Tracking**: All game sessions are logged for analysis and statistics

## Configuration

### Environment Variables

- `OPENAI_API_KEY` (Required): Your OpenAI API key for question generation
- `DB_FILE` (Optional): Path to the SQLite database file (defaults to `db.sqlite3`)

### Model Configuration

The question generator uses GPT-4 with a temperature of 0.9 for creative, varied question generation. You can modify the model settings in `backend/ai_q_gen/question_generator.py`.

## Development

### Adding New Topics

To add new topics, you can either:

1. **Via Database**: Insert directly into the `topics` table
2. **Via Code**: Modify `backend/db/init_db.py` to include new topics in the initial seed data

### Customizing Question Format

The question generation prompt can be customized in `backend/ai_q_gen/question_generator.py`. The current template generates questions with:
- A sentence with a blank (____)
- Four multiple choice options
- A correct answer
- A helpful hint

## Building for Production

### Frontend Build

```bash
cd frontend
npm run build
```

The built files will be in the `frontend/dist` directory.

### Backend Deployment

The FastAPI application can be deployed using:
- **Uvicorn** (development): `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Gunicorn** (production): `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`
- **Docker**: Containerize the application for easy deployment

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**Pouria Mortezaagha**

Copyright (c) 2026 Pouria Mortezaagha
