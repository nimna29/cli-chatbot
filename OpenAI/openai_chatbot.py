from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Initialize the OpenAI API client with the API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

# Run a continuous conversation loop to ineract with the assistant
while True:
    # Make a streaming completion request to the OpenAI chat model
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
        temperature=0.7,
        stream=True
    )
    
    # Initialize an empty message for the assistant's response
    new_message = {"role": "assistant", "content": ""}
    
    print("\nRoz:")
    # Iterate over the completion chunks and print the assistant's response
    for chunk in completion:
        if chunk.choices[0].delta.content:
            # Extract and display each piece of the assistant's response
            assistant_response = chunk.choices[0].delta.content
            print(assistant_response, end="", flush=True)
            # Append the assistant's response to the new message
            new_message["content"] += assistant_response
    # Append the full assistant response to the conversation history
    history.append(new_message)
    
    print("\n")
    user_prompt = input("You: ")
    history.append({"role": "user", "content": user_prompt})
    
    if user_prompt in ["stop", "thanks", "thank you"]:
        print("Roz: Goodbye, Have a nice day!")
        break