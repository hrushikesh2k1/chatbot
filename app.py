from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import json
import re
from datetime import datetime
import random
from dotenv import load_dotenv

load_dotenv()
import os

app = Flask(__name__)

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["chatbot_db"]
cache_collection = db["response_cache"]

# Load knowledge base from JSON
def load_knowledge_base():
    try:
        with open("knowledge_base.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"qa_pairs": []}


knowledge_base = load_knowledge_base()


def find_matching_answer(question):
    """Search for matching keywords in knowledge base"""
    question_lower = question.lower()

    # First check knowledge base
    for qa in knowledge_base.get("qa_pairs", []):
        keywords = qa.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in question_lower:
                return qa.get("answer")

    return None


def get_cached_response(question):
    """Check if response is cached in MongoDB"""
    cached = cache_collection.find_one({"question": question.lower()})
    if cached:
        return cached["answer"]
    return None


def generate_mock_ai_response(question):
    """Generate a mock AI response based on question content (FREE - no API needed)"""
    question_lower = question.lower()

    # Question type detection patterns
    patterns = {
        "what_is": r"\bwhat is\b|\bwhat are\b|\bwhat\'s\b",
        "how_to": r"\bhow to\b|\bhow do\b|\bhow can\b",
        "why": r"\bwhy\b",
        "when": r"\bwhen\b",
        "where": r"\bwhere\b",
        "who": r"\bwho\b",
        "which": r"\bwhich\b",
        "can_you": r"\bcan you\b|\bcould you\b",
        "should": r"\bshould\b",
        "explain": r"\bexplain\b|\btell me about\b",
    }

    # Detect question type
    question_type = None
    for qtype, pattern in patterns.items():
        if re.search(pattern, question_lower):
            question_type = qtype
            break

    # Generate contextual responses based on question type
    if question_type == "what_is":
        topic = (
            question_lower.replace("what is", "")
            .replace("what are", "")
            .replace("what's", "")
            .strip()
        )
        responses = [
            f"Based on my understanding, {topic} is an interesting topic. Let me share what I know: it's a concept/thing that many people find useful.",
            f"Great question! {topic} refers to something that has specific characteristics and purposes.",
        ]
        return random.choice(responses)

    elif question_type == "how_to":
        return f"To accomplish what you're asking about, here are some general steps: 1) Understand the goal clearly, 2) Gather necessary resources, 3) Follow best practices, 4) Practice and refine your approach."

    elif question_type == "why":
        return f"That's a thought-provoking question! There are usually multiple factors involved, including practical reasons, historical context, and logical connections. Would you like me to explore a specific aspect?"

    elif question_type == "when":
        return "The timing can vary depending on context and circumstances. Generally, it relates to specific conditions or timeframes."

    elif question_type == "where":
        return "Location-based questions depend on various factors. It could be in different places depending on the specific situation you're referring to."

    elif question_type == "who":
        return "That would depend on the specific context. Different individuals or groups might be involved depending on the situation."

    elif question_type == "can_you":
        return "I can try to help with that! While I have limitations, I'll do my best to provide useful information or assistance."

    elif question_type == "should":
        return "That's a decision that depends on your specific situation, goals, and constraints. Consider the pros and cons before making a choice."

    elif question_type == "explain":
        topic = (
            question_lower.replace("explain", "").replace("tell me about", "").strip()
        )
        return f"Let me help explain {topic}. This is a topic with various aspects worth exploring. Generally, it involves key concepts and practical applications."

    # Check for specific topics in the question
    elif any(
        word in question_lower for word in ["python", "programming", "code", "coding"]
    ):
        return "Python is a versatile programming language! It's great for beginners and powerful for experts. You can use it for web development, data science, automation, and much more."

    elif any(
        word in question_lower
        for word in ["ai", "artificial intelligence", "machine learning"]
    ):
        return "AI and machine learning are fascinating fields! They involve training computers to learn from data and make intelligent decisions. It's transforming many industries today."

    elif any(word in question_lower for word in ["help", "assist", "support"]):
        return "I'm here to help! Feel free to ask me questions and I'll provide the best answers I can based on my knowledge."

    elif any(word in question_lower for word in ["weather", "temperature", "climate"]):
        return "For current weather information, I'd recommend checking a weather service or app, as I don't have access to real-time weather data."

    else:
        # Generic fallback responses
        fallback_responses = [
            "That's an interesting question! Based on my training, I can tell you that this topic has various aspects to consider.",
            "I understand you're asking about this. While I may not have complete information, I can share that it's a topic worth exploring further.",
            "Good question! This relates to several concepts that are interconnected. Let me know if you'd like more specific details.",
            "I appreciate your curiosity! The answer involves understanding some key principles and practical considerations.",
        ]
        return random.choice(fallback_responses)


def cache_response(question, answer):
    """Store response in MongoDB cache"""
    try:
        cache_collection.insert_one(
            {
                "question": question.lower(),
                "answer": answer,
                "timestamp": datetime.now(),
            }
        )
    except Exception as e:
        print(f"Error caching response: {e}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please ask a question!"})

    # Step 1: Check knowledge base for keyword match
    answer = find_matching_answer(question)
    source = "knowledge_base"

    # Step 2: Check MongoDB cache
    if not answer:
        answer = get_cached_response(question)
        if answer:
            source = "cache"

    # Step 3: Generate mock AI response and cache it
    if not answer:
        answer = generate_mock_ai_response(question)
        source = "ai_generated"

        # Cache the AI-generated response for future use
        if answer and answer != "I am still learning":
            cache_response(question, answer)

    return jsonify({"answer": answer, "source": source})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
