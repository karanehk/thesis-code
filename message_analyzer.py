from proxies.LLM_proxy.gpt_chat import GPTChat

class MessageAnalyzer:
    def __init__(self):
        self.chatgpt = GPTChat()

    def analyze_commit_message(self, commit, diff, commit_num):
        commit_message = commit.msg.strip()
        commit_data = dict()
        commit_data["message"] = commit_message
        commit_data["num"] = commit_num
        response = self.chatgpt.ask_gpt_about_commit(diff, commit_data)
        return response
