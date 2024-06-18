from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from openai import OpenAI
from time import sleep



class GPTChat:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
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

        self.memory = ConversationBufferMemory(human_prefix="Human", input_key="input", max_len=200)


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
            f"We are analyzing a GitHub repository. I will give you the diff value of a commit in this repository and I want you to tell me what files were changed for what purpose. "
            "Give a bulleted list of your findings based on the data I will provide you.\nAs an example, consider the following diff text and its corresponding bullet list:\n"
            'DIFF_TXT: """File Path: calculator.py\nChange Type: modified_file\nDiff:\nAdded: def subtract(num1, num2):\nAdded: return num1 - num2\nAdded:\nAdded: subtract(num1, num2)\nRemoved: sub(num1, num2)"""\n\n'
            'BULLET_LIST: """ - The calculator.py file was modified.\n\n - The commit intended to add the subtract function\n - They changed their mind about the name of the function from sub to subtraction.\n - This is considered a feat/feature commit"""\n'
            f'now answer for the following:\nDIFF_TXT: """{diff}"""',
            f"Now, considering the bulleted list you provided for the given diff, let's analyze the corresponding commit message and see if it was chosen correctly and rationally.\n"
            'First of all, keep the following points about commit message analysis in mind:\n""" - Descriptive Message: A clear and descriptive commit message often indicates a well-thought-out change. Look for specific, action-oriented verbs (e.g., "fix", "add", "remove", "refactor").\n'
            ' - Presence of Keywords: Keywords like "fix", "bug", "feature", "refactor", and "optimize" can provide clues about the nature of the change."""\n'
            'Secondly, remember the last example I gave you, that commit\'s message was "adding subtract function". In this message, we see the keyword add, which is what was done in the commit, we see the name of the function/feature that was added. '
            f'So overall, it is considered a good, clear, and descriptive commit message. Now, the commit you analyzed, had the following message: """{commit_data["message"]}""". '
            "Tell me what you think about this message. What score do you give it between 0-10? State your reasons for the score you gave."
        ]

        # Start the conversation loop
        # print("Start chatting with the AI (type 'exit' or 'quit' to end):")
        response_text = ""

        for i in range(len(user_inputs)):
            formatted_input = self.format_input(user_inputs[i])
            # Get the response from the conversation chain
            response = self.conversation_chain.predict(history=self.memory.load_memory_variables({})['history'], input=formatted_input)
            response_text += response + "\n"
            sleep(3)
            # Get the response from the conversation chain

        self.memory.clear()
        return response_text
        #print(f"AI: {response}")
