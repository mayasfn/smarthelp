from langchain_mistralai import ChatMistralAI
import dotenv
import os
dotenv.load_dotenv()


llm = ChatMistralAI(
    model="mistral-small-latest",
    mistral_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=1,
)
