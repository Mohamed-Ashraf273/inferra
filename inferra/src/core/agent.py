import os

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent
from langchain.memory import ConversationBufferMemory

from inferra.src.llms.grok import GroqModel


class Agent:
    def __init__(self):
        self.prompt = hub.pull("hwchase17/react-chat")
        self.llm = self._load_llm()
        self.tools = self._get_tools()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            input_key="input",
            return_messages=True,
        )
        self.agent_executor = AgentExecutor(
            agent=self._create_agent(),
            tools=self.tools,
            memory=self.memory,
            max_iterations=3,
            handle_parsing_errors=True,
        )

    def _create_agent(self):
        return create_react_agent(
            llm=self.llm, tools=self.tools, prompt=self.prompt
        )

    def _get_tools(self):
        return []

    def _load_llm(self):
        if "GROK_API_KEY" not in os.environ:
            raise ValueError("GROK_API_KEY environment variable not set.")

        groq_model = GroqModel(
            model_name="llama-3.1-8b-instant",
            api_key=os.environ["GROK_API_KEY"],
        )
        return groq_model.model


agent = Agent()
