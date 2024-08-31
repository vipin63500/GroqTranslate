# Importing necessary libraries
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetching the Groq API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the ChatGroq model with the specified model ID and API key
model = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)

# Creating a prompt template for the translation task
system_template = "Translate the following into {language}: "
prompt_template = ChatPromptTemplate(
    [
        ("system", system_template),
        ("user", "{text}")
    ]
)

# Creating a simple string output parser to handle the model's response
parser = StrOutputParser()

# Creating the chain by connecting the prompt template, model, and parser
chain = prompt_template | model | parser

# Initializing the FastAPI application
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server using LangChain Runnable Interface"
)

# Adding the chain as a route to the FastAPI app at the specified path
add_routes(
    app,
    chain,
    path="/chain"
)

# Main function to run the FastAPI app using Uvicorn when the script is executed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
