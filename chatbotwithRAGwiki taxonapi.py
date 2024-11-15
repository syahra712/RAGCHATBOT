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

# Function to fetch vector species data (with SSL verification skipped)
def fetch_vector_species_data(taxon_name):
    url = f"https://insectvectors.science/api/vectors?name={taxon_name.replace(' ', '%20')}"
    
    # Disable SSL verification (temporary workaround)
    response = requests.get(url, verify=False)  # verify=False disables SSL certificate validation
    
    if response.status_code == 200:
        data = response.json()
        if data["count"] > 0:
            species_data = data["results"][0]["data"]
            distribution = species_data.get("distribution", "No distribution info available.")
            genus = species_data.get("genus", "Unknown genus")
            specific_epithet = species_data.get("specificepithet", "Unknown epithet")
            image_url = species_data.get("image", {}).get("url", "No image available.")
            
            return (
                f"Species: {genus} {specific_epithet}\n"
                f"Distribution: {distribution}\n"
                f"Image: {image_url}"
            )
        else:
            return "No vector species data found for the given name."
    else:
        return "Error fetching vector species data."

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

# Main function to handle user queries
def chatbot():
    print("Welcome to the Crop Disease Chatbot! Ask about crop diseases, or type 'exit' to quit.")
    while True:
        question = input("\nYou: ")
        
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Fetch Wikipedia content based on the user's question
        crop_disease = "wheat septoria"  # Replace this with code to parse specific crop diseases if needed
        context = fetch_wikipedia_content(crop_disease)
        
        # Fetch vector species data (e.g., Philaenus spumarius)
        taxon_name = "philaenus spumarius"  # Example taxon name
        vector_data = fetch_vector_species_data(taxon_name)
        
        # Use Gemini API to generate an answer
        answer = generate_answer(question, context)
        
        print(f"\nChatbot: {answer}")
        print(f"\nVector Data: {vector_data}")

# Run the chatbot
if __name__ == '__main__':
    chatbot()
