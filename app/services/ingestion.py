import faker
from openai import OpenAI
import os

fake = faker.Faker()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None

def generate_synthetic_transcript() -> str:
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Generate a short sales call transcript between an agent and customer."}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM error: {e}")
            return "Agent: Hello, how can I help? Customer: I need info on product X. Agent: Sure, it's great!"
    return f"Agent: Hello, how can I help? Customer: I need info on product X. Agent: Sure, it's great!"
