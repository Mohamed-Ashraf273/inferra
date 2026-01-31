from inferra.src.core.agent import Agent


class ChatModel:
    def __init__(self, agent: Agent):
        self.agent = agent

    def generate_reply(self, message: str) -> str:
        result = self.agent.agent_executor.invoke({"input": message})
        return result.get("output", "No response generated")
