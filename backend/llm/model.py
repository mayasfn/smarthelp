from langchain_openai import ChatOpenAI
import dotenv
dotenv.load_dotenv()


llm = ChatOpenAI(
    model="openai-gpt-5",
    temperature=1,
)
