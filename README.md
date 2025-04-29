## 🛒 E-commerce AI Chatbot For Facebook Messenger (OpenAI + FastAPI)

An AI-powered chatbot that answers customer questions about Facebook Marketplace listings via Facebook Messenger by reading product details from an inventory spreadsheet.

### ✨ Features
- Uses **OpenAI GPT-3.5 Turbo** to understand user questions  
- Reads product data from an Excel file (`products.xlsx`)  
- Returns intelligent responses based on filters (e.g., color, price, delivery)  
- Built with **FastAPI**, tested via **Ngrok** and **Postman**

### 🧰 Tech Stack
- Python 3.9+  
- FastAPI  
- OpenAI  
- Pandas  
- Uvicorn  
- python-dotenv  

### 📦 Installation

```bash
git clone https://github.com/gayantharaka/E-commerce-AI-Chatbot-For-Facebook-Messenger.git
cd E-commerce-AI-Chatbot-For-Facebook-Messenger
pip install -r requirements.txt
```

### ⚙️ Setup
1. Create `.env` file in your project folder and add your OpenAI API key to a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

2. Make sure `products.xlsx` exists in the root directory with columns:  
`Name`,`Price`,`Available`,`Color`,`Delivery`

### 🚀 Run the App

```bash
python -m uvicorn chatbot:app --reload --port 8000
```

Test the webhook locally using **Postman** or via **Ngrok**.