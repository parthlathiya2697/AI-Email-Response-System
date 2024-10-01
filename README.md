# Automated Email Response System

This project is an automated email response system that classifies incoming emails into predefined categories and generates appropriate responses using context data stored in an SQLite database.

## Features

- Classifies emails into categories such as "Quotes", "Order Inquiries", and "Angry Customers".
- Generates responses based on the email category and context data.
- Stores context data in an SQLite database.
- Provides a REST API for email processing.

## Setup

### Prerequisites

- Python 3.7+
- SQLite3
- [OpenAI API Key](https://beta.openai.com/signup/)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/automated-email-response-system.git
    cd automated-email-response-system
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    DEBUG=True  # Set to False in production
    ```

5. Run the server:
    ```sh
    uvicorn main:app --reload
    ```

## Usage

### API Endpoints

- **GET /**: Welcome message.
- **GET /emails**: Retrieve all sample emails.
- **GET /emails/{email_id}**: Retrieve a specific email by ID.
- **POST /process_email**: Process an email and generate a response.

### Example Request

To process an email, send a POST request to `/process_email` with the following JSON body:
