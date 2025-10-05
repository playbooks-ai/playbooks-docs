"""
Country Facts Agent - LangGraph Implementation
This agent asks for a user's country, finds nearby countries,
and shares interesting historical facts about each one.
"""

from typing import Annotated, List, Optional, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

# Initialize the LLM (you can replace with any LangChain-compatible LLM)
llm = ChatOpenAI(model="gpt-4", temperature=0.7)


# Define the state structure
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_country: Optional[str]
    nearby_countries: List[str]
    country_facts: dict
    current_step: str
    countries_to_process: List[str]
    processed_countries: List[str]


# Node functions
def ask_for_country(state: AgentState) -> AgentState:
    """Ask the user what country they are from."""
    response = AIMessage(
        content="Hello! I'm here to share interesting facts about countries near you. What country are you from?"
    )
    return {"messages": [response], "current_step": "waiting_for_country"}


def process_user_response(state: AgentState) -> AgentState:
    """Process user's response and extract country if provided."""
    last_message = state["messages"][-1]

    if not isinstance(last_message, HumanMessage):
        return state

    # Use LLM to extract country from user's message
    extract_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Extract the country name from the user's message. If no country is mentioned, respond with 'NONE'. Only respond with the country name or 'NONE'.",
            ),
            ("user", "{message}"),
        ]
    )

    chain = extract_prompt | llm
    result = chain.invoke({"message": last_message.content})
    country = result.content.strip()

    if country and country != "NONE":
        return {"user_country": country, "current_step": "find_nearby_countries"}
    else:
        # Gently nudge for country
        nudge_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "The user hasn't provided their country yet. Engage in friendly conversation and gently nudge them to share what country they're from. Be conversational and natural.",
                ),
                ("user", "{message}"),
            ]
        )

        chain = nudge_prompt | llm
        response = chain.invoke({"message": last_message.content})

        return {"messages": [response], "current_step": "waiting_for_country"}


def find_nearby_countries(state: AgentState) -> AgentState:
    """Find 5 countries near the user's country."""
    nearby_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "List exactly 5 countries that are geographically near {country}. Respond with only the country names separated by commas, nothing else.",
            ),
            ("user", "Find nearby countries"),
        ]
    )

    chain = nearby_prompt | llm
    result = chain.invoke({"country": state["user_country"]})

    # Parse the countries from the response
    countries = [c.strip() for c in result.content.split(",")][:5]

    # Inform user about the nearby countries
    message = f"Great! I found these 5 countries near {state['user_country']}: {', '.join(countries)}. Let me share some interesting historical facts about each of them!"

    return {
        "nearby_countries": countries,
        "countries_to_process": countries,
        "processed_countries": [],
        "country_facts": {},
        "messages": [AIMessage(content=message)],
        "current_step": "process_countries",
    }


def get_country_fact(state: AgentState) -> AgentState:
    """Get an unusual historical fact about the next country to process."""
    if not state.get("countries_to_process"):
        return {"current_step": "complete"}

    # Get the next country to process
    country = state["countries_to_process"][0]

    # Use LLM to get an unusual historical fact
    fact_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Provide one unusual and interesting historical fact about {country}. The fact should be surprising, educational, and engaging. Keep it to 2-3 sentences.",
            ),
            ("user", "Give me a fact"),
        ]
    )

    chain = fact_prompt | llm
    result = chain.invoke({"country": country})
    fact = result.content

    # Store the fact and update state
    country_facts = state.get("country_facts", {})
    country_facts[country] = fact

    # Remove processed country and add to processed list
    remaining_countries = state["countries_to_process"][1:]
    processed = state.get("processed_countries", []) + [country]

    # Create message with the fact
    message = AIMessage(content=f"**{country}**: {fact}")

    return {
        "country_facts": country_facts,
        "countries_to_process": remaining_countries,
        "processed_countries": processed,
        "messages": [message],
        "current_step": "process_countries" if remaining_countries else "complete",
    }


def end_program(state: AgentState) -> AgentState:
    """End the program with a closing message."""
    message = AIMessage(
        content="That's all the fascinating facts about the countries near you! I hope you found these historical tidbits interesting. Feel free to ask if you'd like to learn about countries from another region!"
    )
    return {"messages": [message], "current_step": "end"}


# Routing functions
def route_after_user_input(state: AgentState) -> str:
    """Determine next step after user input."""
    if state.get("current_step") == "waiting_for_country":
        return "process_response"
    return "end"


def route_after_processing(state: AgentState) -> str:
    """Determine next step after processing user response."""
    if state.get("current_step") == "find_nearby_countries":
        return "find_nearby"
    elif state.get("current_step") == "waiting_for_country":
        return "wait_for_input"
    return "end"


def route_after_countries_found(state: AgentState) -> str:
    """Determine next step after finding countries."""
    if state.get("current_step") == "process_countries":
        return "get_fact"
    return "end"


def route_after_fact(state: AgentState) -> str:
    """Determine next step after getting a fact."""
    if state.get("current_step") == "process_countries":
        return "get_fact"
    elif state.get("current_step") == "complete":
        return "end_program"
    return "end"


# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("ask_country", ask_for_country)
workflow.add_node("process_response", process_user_response)
workflow.add_node("find_nearby", find_nearby_countries)
workflow.add_node("get_fact", get_country_fact)
workflow.add_node("end_program", end_program)

# Set entry point
workflow.set_entry_point("ask_country")

# Add edges
workflow.add_edge("ask_country", "wait_for_input")
workflow.add_conditional_edges(
    "wait_for_input",
    route_after_user_input,
    {"process_response": "process_response", "end": END},
)
workflow.add_conditional_edges(
    "process_response",
    route_after_processing,
    {"find_nearby": "find_nearby", "wait_for_input": "wait_for_input", "end": END},
)
workflow.add_conditional_edges(
    "find_nearby", route_after_countries_found, {"get_fact": "get_fact", "end": END}
)
workflow.add_conditional_edges(
    "get_fact",
    route_after_fact,
    {"get_fact": "get_fact", "end_program": "end_program", "end": END},
)
workflow.add_edge("end_program", END)

# Add a wait node for user input (this would integrate with your UI)
workflow.add_node("wait_for_input", lambda x: x)

# Compile the graph
app = workflow.compile()

# Example usage
if __name__ == "__main__":
    import asyncio

    async def run_agent():
        """Run the country facts agent."""
        # Initialize state
        initial_state = {
            "messages": [],
            "user_country": None,
            "nearby_countries": [],
            "country_facts": {},
            "current_step": "start",
            "countries_to_process": [],
            "processed_countries": [],
        }

        # Run the agent
        async for event in app.astream(initial_state):
            # Print the latest messages
            for node_name, node_state in event.items():
                if "messages" in node_state and node_state["messages"]:
                    for msg in node_state["messages"]:
                        if isinstance(msg, AIMessage):
                            print(f"Agent: {msg.content}")
                        elif isinstance(msg, HumanMessage):
                            print(f"User: {msg.content}")

            # Check if waiting for user input
            if node_name == "wait_for_input":
                user_input = input("You: ")
                # Add user message to state and continue
                await app.ainvoke({"messages": [HumanMessage(content=user_input)]})

    # Run the async function
    asyncio.run(run_agent())


# Alternative synchronous usage
def run_agent_sync():
    """Synchronous version of the agent for easier testing."""

    # Initialize state
    state = {
        "messages": [],
        "user_country": None,
        "nearby_countries": [],
        "country_facts": {},
        "current_step": "start",
        "countries_to_process": [],
        "processed_countries": [],
    }

    # Start the conversation
    for event in app.stream(state):
        for node_name, node_state in event.items():
            if "messages" in node_state and node_state["messages"]:
                for msg in node_state["messages"]:
                    if isinstance(msg, AIMessage):
                        print(f"Agent: {msg.content}")

            # Simulate user input when needed
            if (
                node_name == "wait_for_input"
                and node_state.get("current_step") == "waiting_for_country"
            ):
                user_input = input("You: ")
                # Create new state with user message
                state = {
                    **node_state,
                    "messages": node_state["messages"]
                    + [HumanMessage(content=user_input)],
                }

                # Continue the flow with user input
                for event in app.stream(state):
                    for inner_node, inner_state in event.items():
                        if "messages" in inner_state and inner_state["messages"]:
                            for msg in inner_state["messages"]:
                                if isinstance(msg, AIMessage):
                                    print(f"Agent: {msg.content}")
