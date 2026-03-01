from langchain_mistralai import ChatMistralAI
import dotenv
import os

dotenv.load_dotenv()

# Support pour Snowflake Cortex ou OpenAI standard

llm = ChatMistralAI(
    model="mistral-small-latest",
    mistral_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=1,
    api_key=os.getenv("OPENAI_API_KEY"),
)
