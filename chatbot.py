from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import uvicorn
import os
import pandas as pd
import json

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Load product spreadsheet into memory
PRODUCTS_DF = pd.read_excel("products.xlsx")

# Define the expected format of incoming Facebook messages
class FBMessage(BaseModel):
    sender_id: str
    message: str

# Create a webhook endpoint to receive and handle Facebook messages
@app.post("/webhook")
async def handle_message(payload: FBMessage):
    user_input = payload.message

    # Step 1: Ask GPT to extract structured filters from the user's free text
    extraction = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Extract product filters as JSON from the user's message. Fields: product, color, price_max, delivery_preference."},
            {"role": "user", "content": user_input}
        ]
    )

    # Step 2: Parse the extracted filters
    filters = extraction.choices[0].message.content
    try:
        filters_dict = json.loads(filters)
    except json.JSONDecodeError:
        filters_dict = {}  # Default to empty if GPT response is invalid

    # Step 3: Filter products based on extracted filters
    results = PRODUCTS_DF.copy()

    # Filter by product name
    product_name = filters_dict.get("product")
    if product_name:
        results = results[results["Name"].str.lower().str.contains(product_name.lower())]

    # Filter by color
    color = filters_dict.get("color")
    if color:
        results = results[results["Color"].str.lower() == color.lower()]  

    # Filter by max price
    price_max = filters_dict.get("price_max")
    if price_max:
        results = results[results["Price"] <= price_max]

    # Filter by delivery preference
    delivery_preference = filters_dict.get("delivery_preference")
    if delivery_preference:
        results = results[results["Delivery"] == True]

    # Step 4: Summarize the best match to feed into GPT
    if not results.empty:
        top_result = results.iloc[0]  # Pick the first matching product
        summary = f"{top_result['Name']}: {top_result['Color']} color, ${top_result['Price']}, delivery available: {top_result['Delivery']}"
    else:
        summary = "No matching product found."

    # Step 5: Ask GPT to generate a nice, human-friendly response
    final_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful store assistant. Here's the product info: {summary}"},
            {"role": "user", "content": user_input}
        ]
    )

    # Step 6: Return the generated reply back to Facebook
    reply = final_response.choices[0].message.content
    return {"reply": reply}

# Start the server when running the script directly
if __name__ == "__main__":
    uvicorn.run("chatbot:app", host="0.0.0.0", port=8000, reload=True)