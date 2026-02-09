See the recent developments in feature branch

# Chatbot Application

## Overview

This project is a lightweight web-based chatbot application built using **Python (Flask)**.
The chatbot is designed to answer user questions using a hybrid approach that combines:

1. **Predefined knowledge base lookup** – retrieves answers from a local JSON knowledge base.
2. **Cached response retrieval** – improves performance by returning previously stored responses when available.
3. **Fallback processing** – handles unanswered queries through additional logic when no match is found.

The application provides a simple browser-based interface where users can enter questions and receive responses in real time.

---

## Key Features

* Web-based chatbot interface powered by Flask
* Knowledge-base-driven response system using `knowledge_base.json`
* Response caching mechanism for faster repeated queries
* REST API endpoint for processing chatbot requests
* Basic test structure for validating application behavior
* Pre-commit configuration for maintaining code quality

---

## Project Structure

```
chatbot/
├── app.py                  # Main Flask application
├── requirements.txt        # Project dependencies
├── knowledge_base.json     # Static knowledge base for chatbot responses
├── templates/
│   └── index.html          # Web interface for chatbot
├── tests/                  # Unit tests
├── .pre-commit-config.yaml # Pre-commit hooks configuration
└── .github/                # GitHub workflow configurations
```

---

## How It Works

1. A user submits a question through the web interface.
2. The application checks the local **knowledge base** for matching keywords.
3. If no match is found, the system checks the **cached responses**.
4. If still unresolved, fallback logic generates or retrieves an alternative response.
5. The answer is returned to the user through the web UI or API response.

---

## Installation

### Prerequisites

* Python 3.8+
* pip

### Setup

```bash
git clone https://github.com/hrushikesh2k1/chatbot.git
cd chatbot
pip install -r requirements.txt
```

---

## Running the Application

```bash
python app.py
```

The application will start on:

```
http://0.0.0.0:5000
```

Open the URL in your browser to interact with the chatbot.

---

## Future Enhancements

* Integration with LLM-based responses
* Improved NLP-based intent detection
* Persistent database-backed conversation history
* Authentication and multi-user support
* CI/CD integration for automated testing and deployment

---

## License

This project is intended for educational and demonstration purposes.
