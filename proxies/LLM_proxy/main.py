from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory

# Create an instance of the OpenAI LLM
llm = OpenAI(temperature=0.7, api_key='your_openai_api_key')

# Define a prompt template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write a detailed essay about {topic}.",
)

memory = ConversationBufferMemory()

# Create a LLMChain
conversation_chain = ConversationChain(llm=llm, memory=memory)


# Function to format the user input using the prompt template
def format_input(user_input):
    return prompt.format(topic=user_input)


# Start the conversation loop
print("Start chatting with the AI (type 'exit' or 'quit' to end):")
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Ending conversation.")
        break

    # Format the input using the prompt template
    formatted_input = format_input(user_input)

    # Get the response from the conversation chain
    response = conversation_chain.invoke(formatted_input)
    print(f"AI: {response}")
