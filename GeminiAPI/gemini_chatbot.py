import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set the path for system prompt
project_path = os.path.dirname(os.path.abspath(__file__))
sys_prompt_path = os.path.join(project_path, './system_prompt.txt')

# Read the system prompt from the file
with open(sys_prompt_path, 'r') as file:
    system_prompt = file.read()

# Define the default user prompt
default_user_prompt = "Introduce Yourself. And ask How may I help you?"

# Initialize the history (conversation) with the system prompt and default user prompt
history = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": default_user_prompt}
]

# Configure Gemini API with API key from environment
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize Gemini model for generating content
model = genai.GenerativeModel("gemini-1.5-flash")

# Run a continuous conversation loop to interact with the assistant
while True:
    # Format history into a single string to feed into Gemini
    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])

    # Generate response using Gemini model with streaming enabled
    response = model.generate_content(conversation_history, stream=True)

    # Initialize an empty message to hold the full response from the assistant
    new_message = {"role": "assistant", "content": ""}

    # Print assistant's response in real-time as it streams
    print("\nRoz:")
    for chunk in response:
        if chunk.text:
            # Display each chunk of the assistant's response as it streams
            print(chunk.text, end="", flush=True)
            # Append each chunk to the new message
            new_message["content"] += chunk.text


    # Append the full assistant response to the conversation history
    history.append(new_message)

    # Get user input for the next message
    user_prompt = input("\nYou: ")
    history.append({"role": "user", "content": user_prompt})

    # Exit loop if the user wants to end the conversation
    if user_prompt.lower() in ["stop", "thanks", "thank you"]:
        print("Roz: Goodbye, Have a nice day!")
        break
