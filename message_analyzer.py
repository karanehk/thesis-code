from proxies.LLM_proxy.gpt_chat import GPTChat

class MessageAnalyzer:
    def __init__(self):
        self.chatgpt = GPTChat()

    def analyze_commit_message(self, commit, diff):
        commit_message = commit.msg.strip()
        commit_data = dict()
        commit_data["message"] = commit_message
        response = self.chatgpt.ask_gpt_about_commit(diff, commit_data)
        return response
