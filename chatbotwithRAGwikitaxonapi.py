import requests
import streamlit as st

# Function to fetch content from Wikipedia based on a topic
def fetch_wikipedia_content(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", None)  # Return None if no extract is found
    else:
        return None

# Function to use the Gemini API to generate an answer based on the question and context
def generate_answer(question, context=None):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyCx13fbPx6FC4nUYkVlWWDKIJAoY9fHR8g"
    headers = {"Content-Type": "application/json"}
    
    # If no context (Wikipedia data) is found, use the question directly as context
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"Context: {context}" if context else f"Question: {question}"}
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

# Streamlit UI Setup
def chatbot():
    st.title("Crop Disease Chatbot")
    st.write("Ask about crop diseases, or type 'exit' to quit.")
    
    # User input field
    question = st.text_input("You:", "")

    # If the user submits a question
    if question:
        if question.lower() == 'exit':
            st.write("Goodbye!")
            return

        # Search Wikipedia for the user query
        context = fetch_wikipedia_content(question)
        
        # Use Gemini API to generate an answer
        if context:
            # If context is found in Wikipedia, pass it to Gemini API
            answer = generate_answer(question, context)
        else:
            # If no context is found from Wikipedia, just pass the question to Gemini API
            answer = generate_answer(question)
        
        # Display the answer
        st.write(f"**Chatbot:** {answer}")

# Run the chatbot in the Streamlit app
if __name__ == '__main__':
    chatbot()
