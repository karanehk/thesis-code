from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from openai import OpenAI
from time import sleep
from langchain.schema import AIMessage




class GPTChat:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            timeout=None,
            max_tokens=1000,
            max_retries=5
            # base_url="...",
            # organization="...",
            # other params...
        )

        self.prompt_template = PromptTemplate(input_variables=['history', 'input'], 
                                template='The following is a analystic conversation between a human and an AI. The AI is professional data analyst and software expert. AI provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.\n\nCurrent conversation:\n{history}\nHuman: {input}\n')

        self.memory = ConversationBufferMemory(input_key="input")


        self.conversation_chain = ConversationChain(
            llm=self.llm,
            prompt=self.prompt_template,
            memory=self.memory,
            verbose=False
        )

    def format_input(self, user_input):
        return self.prompt_template.format(history=str(self.memory.chat_memory), input=user_input)

    def df_to_md(self, df, row_limit=40):
        df = df.head(row_limit)
        result = df.to_markdown(index=False, tablefmt="grid")
        return result

    def ask_gpt_about_commit(self, diff, commit_data):

        user_inputs = [
        f"""We are analyzing a GitHub repository. I will provide you with the diff of a commit, and I want you to tell me what files were changed and for what purpose. Provide a detailed bulleted list of your findings based on the given data.
        Here's an example diff and its corresponding analysis:
        DIFF_TXT: 
        \"\"\"File name: calculator.py
        Change type: MODIFY
        Changes:
        added: 1  def subtract(num1, num2):
        added: 2      return num1 - num2
        added: 3  
        deleted: 22          sub(num1, num2)
        added: 25          subtract(num1, num2)
        \"\"\"
        BULLET_LIST:
        \"\"\" - The file `calculator.py` was modified.
        - A new function `subtract` was added.
        - The return statement for the new function was added.
        - The function call was updated to use `subtract` instead of `sub`.
        - This commit represents a feature addition (feat/feature).
        \"\"\"
        Now, please analyze the following diff and provide a similar bulleted list and Keep in mind that if the DIFF_TXT is "First commit, so no diff provided." then you don't need to give a list.:
        DIFF_TXT: \"\"\"{diff}\"\"\"
        """,
        f"""Now, let's analyze the commit message for the given diff. Consider the following points when evaluating the commit message:
        1. Descriptive Message: A clear and descriptive commit message often indicates a well-thought-out change. Look for specific, action-oriented verbs (e.g., "fix", "add", "remove", "refactor", "initiate", "init").
        2. Presence of Keywords: Keywords like "fix", "bug", "feature", "refactor", and "optimize" can provide clues about the nature of the change.
        Here's an example of a good commit message:
        - Commit Message: "adding subtract function"
          - Analysis: The message includes the keyword "add," which clearly indicates the action performed. It specifies the function added, making it clear and descriptive.
        Now, consider the commit you analyzed. The commit message was:
        \"\"\"{commit_data["message"]}\"\"\"
        Analyze this message and rate its clarity and descriptiveness on a scale from 0 to 10. Keep in mind that if the DIFF_TXT is "First commit, so no diff provided." then messages like first commit, initial commit, init and such are ok. Provide your reasons for the score you assign.
        """
    ]

        # Start the conversation loop
        # print("Start chatting with the AI (type 'exit' or 'quit' to end):")
        response_text = ""
        to_save = self.memory.chat_memory.messages.copy()

        for i in range(len(user_inputs)):
            formatted_input = self.format_input(user_inputs[i])
            # Get the response from the conversation chain
            response = self.conversation_chain.predict(history=self.memory.load_memory_variables({})['history'], input=formatted_input)
            response_text += response + "\n"
            '''if i == 0:
                to_save.append(AIMessage(content=response))
            else:
                self.memory.clear()'''
            sleep(3)
        to_save.append(AIMessage(content=response_text))
        self.memory.clear()
        self.memory.chat_memory.messages = to_save

        return response_text
