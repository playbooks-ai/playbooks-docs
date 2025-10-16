# Playbooks vs Traditional Agent Frameworks

One of the core promises of Playbooks is **radical simplicity**: building AI agents should be accessible, readable, and maintainable. To illustrate this difference, let's compare how the same agent is built in Playbooks versus traditional agent frameworks. We'll use LangGraph as a representative example of graph-based orchestration frameworks. 

:bulb: It is easy to migrate from traditional agent frameworks to Playbooks. See [Migrating from Other Agent Frameworks](../getting-started/migrating.md) for details.

## The Challenge

We'll build a "Country Facts Agent" that:

1. Asks the user what country they're from
2. Handles conversational back-and-forth if the user doesn't immediately provide a country
3. Finds 5 nearby countries
4. Retrieves and shares interesting historical facts about each country
5. Gracefully exits

This is a realistic agent with multiple steps, conditional logic, LLM calls, and Python code execution-perfect for comparing frameworks.

---

## The Playbooks Implementation: 29 Lines

Here is **country-facts.pb**, a Playbooks program. This **29 line, highly readable program** accomplishes the same task as the much longer traditional framework implementation shown below.

````markdown linenums="1" title="country-facts.pb"
# Country facts agent
This agent prints interesting facts about nearby countries

## Main
### Triggers
- At the beginning
### Steps
- Ask user what $country they are from
- If user did not provide a country, engage in a conversation and gently nudge them to provide a country
- List 5 $countries near $country
- Tell the user the nearby $countries
- Inform the user that you will now tell them some interesting facts about each of the countries
- process_countries($countries)
- End program

```python
from typing import List

@playbook
async def process_countries(countries: List[str]):
    for country in countries:
        # Calls the natural language playbook 'GetCountryFact' for each country
        fact = await GetCountryFact(country)
        await Say("user", f"{country}: {fact}")
```

## GetCountryFact($country)
### Steps
- Return an unusual historical fact about $country
````

### What's Happening in the Playbooks Code?

The Playbooks program naturally expresses agent behavior:

- **Lines 4-14**: The `Main` playbook defines the conversational flow in plain English. No state management, no routing logic - just the steps the agent should follow.
- **Line 13**: Python code seamlessly integrates - the natural language playbook calls `process_countries()`, a Python playbook.
- **Lines 19-24**: The Python playbook `process_countries` uses standard Python control flow (a for loop) and awaits both a natural language playbook (`GetCountryFact`) and a built-in playbook (`Say`).
- **Lines 27-29**: `GetCountryFact` is another natural language playbook that returns a fact.

Notice there's **no boilerplate**: no graph definitions, no state schemas, no routing functions, no manual prompt engineering. Just behavior specification.

---

## Traditional Framework Implementation: 272 Lines

For comparison, here's how the same agent is built using LangGraph, a leading agent framework. Similar complexity would be found in other traditional frameworks like CrewAI, AutoGen, or custom LangChain implementations.

````python linenums="1" title="country-facts.langgraph.py"
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
````

### What's Happening in the LangGraph Code?

The LangGraph implementation includes:

- **Lines 19-27**: A TypedDict defining the state structure with 7 fields to track conversation state, countries, facts, and control flow.
- **Lines 30-160**: Six node functions (`ask_for_country`, `process_user_response`, `find_nearby_countries`, `get_country_fact`, `end_program`) that manually manage state transitions.
- **Lines 163-193**: Four routing functions to determine which node to execute next based on state.
- **Lines 196-232**: Graph construction code wiring together nodes, edges, conditional edges, and routing logic.
- **Lines 234-272**: Additional scaffolding for running the agent.

This requires the developer to:

1. Explicitly manage all state transformations
2. Define all possible execution paths
3. Write routing logic for every decision point
4. Manually craft prompts for each LLM call
5. Handle the mechanics of graph execution

Most critically: **the agent's behavior is scattered across multiple functions and routing logic**. Understanding what the agent does requires reading the entire file and mentally reconstructing the flow.

---

## Key Differences

| Aspect | Playbooks | Traditional Framework (LangGraph) |
|--------|-----------|------------------------|
| **Lines of Code** | 29 | 250+ |
| **Readability** | Natural language, immediately understandable | Requires understanding graphs, state machines, routing |
| **State Management** | Automatic | Manual state definitions with many fields |
| **Control Flow** | Natural steps + Python control structures | Explicit graph with nodes, edges, routing functions |
| **Prompt Engineering** | Declarative (LLM infers from steps) | Imperative (manually write each prompt) |
| **Mixed Execution** | Python and natural language on same call stack | Separate nodes requiring state passing |
| **Business User Friendly** | ✅ Yes - readable and modifiable | ❌ No - requires programming expertise |
| **Maintainability** | High - behavior is centralized | Low - logic is distributed |
| **Debugging** | Step through playbooks like functions | Trace through graph execution |

---

## Why This Matters

### 1. **Accessibility**

The Playbooks version can be read, understood, and even modified by non-technical stakeholders. A product manager can review the `Main` playbook and understand exactly what the agent does. They could even propose changes:

> "After asking for the country, let's also ask if they'd like facts about culture or history."

With LangGraph, this requires a developer to understand state machines, modify routing logic, and update multiple node functions.

### 2. **Maintainability**

In Playbooks, the agent's behavior is **centralized** in the `Main` playbook. Want to add a step? Add a line. Want to change the order? Reorder the steps.

In LangGraph, behavior is **distributed** across state definitions, node functions, routing functions, and graph edges. A simple change might require modifying 4-5 different sections.

### 3. **Cognitive Load**

Playbooks lets you **think at the behavioral level**: "What should the agent do?"

LangGraph requires thinking at the **mechanical level**: "How do I wire up state, nodes, and edges to make this happen?"

### 4. **Development Speed**

The 11x reduction in code size isn't just about lines-it's about **time to value**. Building an agent in Playbooks takes minutes. Building the equivalent in LangGraph takes hours.

### 5. **Verifiability**

Because Playbooks programs are concise and readable, they're easier to verify. You can audit agent behavior by reading 29 lines instead of 272.

---

## When to Use Each Approach

### Choose Playbooks If:

- ✅ You want to build agents quickly with minimal boilerplate
- ✅ Non-technical stakeholders need to understand/approve agent behavior
- ✅ You value readability and maintainability over low-level control
- ✅ You want seamless mixing of Python and natural language
- ✅ You prefer declarative behavior specification

### Choose Traditional Frameworks If:

- ⚙️ You need extremely fine-grained control over every LLM call and state transition
- ⚙️ You're comfortable with graph-based programming paradigms
- ⚙️ Your team consists entirely of experienced developers
- ⚙️ You want to manually optimize every aspect of execution

---

## Try It Yourself

Both implementations are available:

- **Playbooks**: Copy the `.pb` file above and run it
- **LangGraph example**: See [country-facts.langgraph.py](../assets/country-facts.langgraph.py)

Run them side by side and experience the difference firsthand.

Then ask yourself: **Which would you rather maintain?**

---

## Learn More

- [Getting Started with Playbooks](../getting-started/index.md)
- [Migrating from Other Agent Frameworks](../getting-started/migrating.md)
- [Playbooks Programming Guide](../programming-guide/index.md)
- [Understanding Playbooks Assembly Language](playbooks-assembly-language.md)