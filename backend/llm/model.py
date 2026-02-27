from langchain_mistralai import ChatMistralAI
import dotenv
dotenv.load_dotenv()


llm = ChatMistralAI(
    model="mistral-small-latest",
    mistral_api_key="uYjtS4EklNWuYR87xB0KLXNiIqxcT4mx",
    temperature=1,
)
