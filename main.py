# main.py

import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import random
from openai import OpenAI
import os
from dotenv import load_dotenv
import sqlite3

# Load environment variables from .env file
load_dotenv()

DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
client = OpenAI()

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI(title="Automated Email Response System")

# Create SQLite database and insert context data
def create_context_db():
    conn = sqlite3.connect('context_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS context (
            category TEXT PRIMARY KEY,
            context TEXT
        )
    ''')
    context_data = [
        ("Quotes", "Please provide a detailed quote for the requested product."),
        ("Order Inquiries", "Provide an update on the order status and expected delivery time."),
        ("Angry Customers", "Apologize for the inconvenience and assure the customer that their issue will be resolved promptly.")
    ]
    cursor.executemany('INSERT OR REPLACE INTO context (category, context) VALUES (?, ?)', context_data)
    conn.commit()
    conn.close()

# Generate sample data on startup
create_context_db()

# Read emails into a DataFrame
emails_df = pd.read_csv('sample_data/emails.csv')

# Pydantic models
class Email(BaseModel):
    subject: str
    body: str

class Response(BaseModel):
    category: str
    reply: str

# Email classification
def classify_email(email_body):
    messages = [
        {"role": "system", "content": "Classify the following email into one of the categories: Quotes, Order Inquiries, Angry Customers."},
        {"role": "user", "content": f"Email:\n{email_body}\n\nCategory:"}
    ]

    if DEBUG:
        return "Order Inquiries"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages
        )
        category = response.choices[0].message['content'].strip()
        return category
    except Exception as e:
        print(f"Error during classification: {e}")
        return "Unknown"

# Fetch context data from SQLite database
def get_context_from_db(category):
    conn = sqlite3.connect('context_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT context FROM context WHERE category = ?', (category,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else ""

def process_email(email: Email):
    # Classify email
    category = classify_email(email.body)
    if category == "Unknown":
        raise HTTPException(status_code=500, detail="Email classification failed")

    # Fetch context data for the category from the database
    context = get_context_from_db(category)

    # Generate response with context
    reply = generate_response(email.body, category, context)
    return Response(category=category, reply=reply)

# Update generate_response to accept context
def generate_response(email_body, category, context):
    messages = [
        {"role": "system", "content": "You are an assistant generating an email response."},
        {"role": "user", "content": f"Email Category: {category}\nContext: {context}\nLanguage Level: Grade 3 English\nTone: Concise, respectful, and sales-optimized.\n\nEmail Body:\n{email_body}\n\nGenerate a response:"}
    ]

    if DEBUG:
        return "This is a sample response for the given email body with context"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages
        )
        reply = response.choices[0].message['content'].strip()
        return reply
    except Exception as e:
        print(f"Error during response generation: {e}")
        return "Sorry, I couldn't generate a response at this time."

@app.get("/")
def read_root():
    return {"message": "Welcome to the Automated Email Response System API"}

@app.get("/emails")
def get_emails():
    return emails_df.to_dict(orient='records')

@app.get("/emails/{email_id}")
def get_email(email_id: int):
    email = emails_df[emails_df['id'] == email_id]
    if email.empty:
        raise HTTPException(status_code=404, detail="Email not found")
    return email.to_dict(orient='records')[0]

@app.post("/process_email", response_model=Response)
def process_email(email: Email):
    # Classify email
    category = classify_email(email.body)
    if category == "Unknown":
        raise HTTPException(status_code=500, detail="Email classification failed")

    # Fetch context data for the category from the database
    context = get_context_from_db(category)

    # Generate response with context
    reply = generate_response(email.body, category, context)
    return Response(category=category, reply=reply)
