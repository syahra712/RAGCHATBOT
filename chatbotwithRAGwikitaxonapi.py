import streamlit as st
import requests

# Function to fetch content from Wikipedia based on a topic
def fetch_wikipedia_content(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No information available.")
    else:
        return "No information available."

# Function to use the Gemini API to generate an answer based on the question and context
def generate_answer(question, context):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyCx13fbPx6FC4nUYkVlWWDKIJAoY9fHR8g"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"Context: {context}"},
                    {"text": f"Question: {question}"}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "Error generating response."

# Expanded list of diseases relevant to Pakistan
disease_keywords = [
    "wheat septoria", "wheat rust", "wheat yellow rust", "wheat leaf spot", "wheat stem rust", 
    "rice blast", "rice sheath blight", "rice bacterial blight", "rice tungro virus", 
    "cotton leaf curl", "cotton bollworm", "cotton root rot", "cotton mosaic virus", 
    "maize leaf blight", "maize smut", "maize stalk rot", "maize rust", 
    "tomato leaf curl virus", "tomato blight", "tomato mosaic virus", 
    "potato blight", "potato tuber moth", "potato black leg", 
    "chili mosaic virus", "chili wilt", "chili blight", 
    "sugarcane smut", "sugarcane top shoot borer", "sugarcane rust", 
    "peanut rust", "peanut blight", "peanut wilt", 
    "mango anthracnose", "mango malformation", "mango hoppers", 
    "citrus canker", "citrus greening", "citrus fruit drop", 
    "grapevine downy mildew", "grapevine powdery mildew", 
    "banana bunchy top virus", "banana wilt", "banana weevil borer"
]

# Function to extract potential crop disease from the user's question
def extract_relevant_term(question):
    # Normalize question to lowercase and search for keywords
    question = question.lower()
    
    # Search for crop diseases
    for disease in disease_keywords:
        if disease in question:
            return disease, "disease"
    
    return None, None

# Streamlit UI
def chatbot():
    st.title("Crop Disease Chatbot")
    st.subheader("Ask about crop diseases in Pakistan and get instant responses!")

    # Input text box for the user's question
    user_input = st.text_input("You: Ask about a crop disease (e.g., 'What is rice blast?')")

    if user_input:
        # Extract the relevant term from the user's question
        term, term_type = extract_relevant_term(user_input)
        
        if term:
            # Fetch Wikipedia content based on the term (disease)
            context = fetch_wikipedia_content(term)
            
            # Display the context fetched from Wikipedia
            st.write("### Disease Information:")
            st.write(context)

            # Generate a response using Gemini API
            answer = generate_answer(user_input, context)
            
            # Display the chatbot's answer
            st.write("### Chatbot's Response:")
            st.write(answer)
        else:
            st.warning("Chatbot: I'm sorry, I couldn't detect a relevant disease from your question.")
    
    # Optional: Add a button to reset the chat
    if st.button("Clear Chat"):
        st.experimental_rerun()

# Run the chatbot in the Streamlit app
if __name__ == '__main__':
    chatbot()
