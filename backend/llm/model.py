from langchain_mistralai import ChatMistralAI
import dotenv
import os

dotenv.load_dotenv()

# Support pour Snowflake Cortex ou OpenAI standard
base_url = os.getenv("OPENAI_BASE_URL")
model = "mistral-large" if base_url else "gpt-4o-mini"

llm = ChatMistralAI(
    model="mistral-small-latest",
    mistral_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=1,
    api_key=os.getenv("OPENAI_API_KEY"),
)
