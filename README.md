Start the FastAPI Server

bash
Copy code
uvicorn main:app --reload
This will start the server at http://127.0.0.1:8000.


Using Swagger UI
Open your browser and navigate to:

arduino
Copy code
http://127.0.0.1:8000/docs

Using cURL
1. Get All Emails
bash
Copy code
curl -X GET "http://127.0.0.1:8000/emails" -H "accept: application/json"
2. Get Email by ID
bash
Copy code
curl -X GET "http://127.0.0.1:8000/emails/1" -H "accept: application/json"
3. Process an Email
bash
Copy code
curl -X POST "http://127.0.0.1:8000/process_email" \
-H "Content-Type: application/json" \
-d '{
  "subject": "Order Delay",
  "body": "My order hasn\'t arrived yet. What\'s the status?"
}'
