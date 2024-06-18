from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from openai import OpenAI

# Create an instance of the OpenAI LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.2,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="",  
    # base_url="...",
    # organization="...",
    # other params...
)

# Define a prompt template
prompt_template = PromptTemplate(input_variables=['history', 'input'], 
                                template='The following is a analystic conversation between a human and an AI. The AI is professional data analyst and software expert. AI provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.\n\nCurrent conversation:\n{history}\nHuman: {input}\n')

memory = ConversationBufferMemory(human_prefix="Human", input_key="input")


# Create a LLMChain
conversation_chain = ConversationChain(
    llm=llm,
    prompt=prompt_template,
    memory=memory,
    verbose=True
)

def format_input(user_input):
    return prompt_template.format(history=str(memory.chat_memory), input=user_input)


# Start the conversation loop
print("Start chatting with the AI (type 'exit' or 'quit' to end):")
while True:
    user_input = input("You: ")

    if user_input.lower() in ['exit', 'quit']:
        print("Ending conversation.")
        break

    formatted_input = format_input(user_input)

    # Get the response from the conversation chain
    response = conversation_chain.predict(input=formatted_input)

    print(f"AI: {response}")
