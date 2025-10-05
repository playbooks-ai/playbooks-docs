# Tutorial: Building an Order Status Assistant with Playbooks

This tutorial introduces new Playbooks programmers to the language, the framework and the basics of building AI agents. We will use a simple example use case of a customer support AI assistant that checks order status. We will start with a simple “hello world”, then add user input, Python playbooks, markdown↔python calls, multi-agent calls, triggers, description placeholders, and finally explore ReAct and Raw playbooks.

:warning: Prerequisites (see [Getting Started](../get-started/index.md)):

- Installed Playbooks
- Successfully ran a playbooks program using `playbooks run <program>.pb`


:information_source: Code for this tutorial is available [here](https://github.com/playbooks-ai/playbooks/tree/main/examples/tutorials)

---

## Playbooks AI approach: Software 3.0

- **LLM as a processor**: Your natural language specifications become the program; the runtime compiles and executes them reliably on LLM.
- **Programmer friendly**: Agents are classes, playbooks are methods. Multi-agent communication is message passing. Use standard developer tools and IDEs for debugging, code completion, etc.
- **Simple syntax**: Use markdown `H1` tags for agents, `H2` tags and `@playbook` decorated Python functions for playbooks. You pick your coding style - `$order_id = LoadOrderId()`, `Load $order_id`, `Load user's order id` are all valid.
- **Soft + Hard logic**: Run soft logic on LLM, hard logic on CPU; on the same call stack; mix and match as needed.
    1. [LLM] Natural language markdown playbooks for known busiess logic 
    2. [LLM] Natural language ReAct playbooks for dynamic planning
    3. [LLM] Raw playbooks for full control over the LLM prompt
    4. [CPU] Python playbooks when you need determinism, external system access, and general computation
- **Higher abstraction**: Describe behavior at the level of “what the agent should do,” not plumbing or orchestration code. Leads to 10x fewer lines of code.
- **Verifiability and observability**: Structured programs, Semantic static program analysis, compilation into LLM-friendly Assembly Language, triggers, post-hoc checks enable reliable behavior despite LLM non-determinism
- **Advanced capabilities**: Dynamic playbook generation, observer agents, formal verifiability and more.

---

## 1) Hello, world!

### 01.01 Let's begin
examples/tutorials/01.01/[order_assistant.pb](https://github.com/playbooks-ai/playbooks/blob/main/examples/tutorials/01.01/order_assistant.pb)

```markdown linenums="1" title="order_assistant.pb"
# Order Support Agent
You are an agent that greets users and helps with order questions.

## Main
### Triggers
- At the beginning
### Steps
- Greet the user and explain what you can help with
- End program
```

Note:

- Line 1: `# Order Support Agent` creates an agent. 
- Line 3: `## Main` defines a playbook, which is triggered automatically at the beginning (line 6) of the program execution. 
- Line 7: `### Steps` lists the steps to be executed.

<details>
<summary>Output</summary>
```text
> playbooks run examples/tutorials/01.01/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/01.01/order_assistant.pb']
  Compiling agent: Order Support Agent

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you with any questions or issues related to your orders. Whether you need to check order status, make changes, handle returns, or resolve any order-related concerns, I'm ready to assist you. How can I help you today?
```
</details>

:bulb: Playbooks framework caches LLM responses by default. So, if you run the program again, compilation will be skipped and you will see the same output. The cache can be disabled using a `playbooks.toml` [configuration file](../reference/config.md).

:exclamation: Notice that in the output, the agent listed capabilities that we haven't provided playbooks for.

Let's improve this by asking the agent to only list capabilties corresponding to the playbooks that we have provided.

### 01.02 Prompt Tuning

examples/tutorials/01.02/[order_assistant.pb](https://github.com/playbooks-ai/playbooks/blob/main/examples/tutorials/01.02/order_assistant.pb)
```markdown linenums="1" title="order_assistant.pb"
# Order Support Agent
You are an agent that greets users and helps with order questions. Note that your capabilities are limited to the playbooks defined below.

## Main
### Triggers
- At the beginning
### Steps
- Greet the user and explain what you can help with
- End program
```

Changes:

- Line 2: We added extra instructions to the agent.

<details>
<summary>Output</summary>

```text
> playbooks run examples/tutorials/01.02/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/01.02/order_assistant.pb']
  Compiling agent: Order Support Agent

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you with any questions about your orders. However, I should let you know that my capabilities are currently limited to greeting you and providing this basic information. How can I assist you today?
```
</details>

Much better!

---

## 2) Ask for user input

Let's ask the user for their order id.

### 02.01 User input

examples/tutorials/02.01/[order_assistant.pb](https://github.com/playbooks-ai/playbooks/blob/main/examples/tutorials/02.01/order_assistant.pb)

```markdown linenums="1" title="order_assistant.pb"
# Order Support Agent
You are an agent that greets users and helps with order questions. Note that your capabilities are limited to the playbooks defined below.

## Main
### Triggers
- At the beginning
### Steps
- Greet the user and explain what you can help with
- Ask user for their order id
- Thank the user for providing the order id
- End program
```

Changes:

- Line 9: Here we ask the user for their order id.
- Line 10: New step to thank the user for providing the order id.

<details>
<summary>Output</summary>

```text
> playbooks run examples/tutorials/02.01/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/02.01/order_assistant.pb']

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you with any questions about your orders. I can assist you with order status, tracking information, and other order-related inquiries.

OrderSupportAgent: To get started, could you please provide me with your order ID?

User: 47463874

OrderSupportAgent: Thank you for providing your order ID: 47463874. I have recorded this information.
```
</details>

### 02.02 Conversational Input

We want the agent to wait on line 9 until the user provides their order id. Let's add that instruction.

examples/tutorials/02.02/[order_assistant.pb](https://github.com/playbooks-ai/playbooks/blob/main/examples/tutorials/02.02/order_assistant.pb)

```markdown linenums="1" title="order_assistant.pb"
# Order Support Agent
You are an agent that greets users and helps with order questions. Note that your capabilities are limited to the playbooks defined below.

## Main
### Triggers
- At the beginning
### Steps
- Greet the user and explain what you can help with
- Ask user for their order id; engage in a conversation as needed
- Thank the user for providing the order id
- End program
```

Changes:

- Line 9: Here we add a new step to engage in a conversation as needed.

<details>
<summary>Output</summary>

```text
> playbooks run examples/tutorials/02.02/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/02.02/order_assistant.pb']
  Compiling agent: Order Support Agent

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you with any questions about your orders. I can assist you with order status, tracking information, and other order-related inquiries.

OrderSupportAgent: To get started, could you please provide me with your order ID? This will help me look up your specific order details.

User: how are you

OrderSupportAgent: I'm doing well, thank you for asking! I'm here and ready to help you with your order. Could you please share your order ID so I can assist you with your order-related questions?

User: hold on.. let me look that up

OrderSupportAgent: No problem at all! Take your time finding your order ID. I'll wait here for you.

User: found it 44344456

OrderSupportAgent: Perfect! Thank you for providing your order ID: 44344456. I have that recorded now.
```
</details>

Notice that now the agent engaged in a conversation with the user while waiting for the order id.

### 02.03 Agent Behavior

This behavior trait can be added to the agent's instructions so it applies to any time the agent asks the user for some information.

examples/tutorials/02.03/[order_assistant.pb](https://github.com/playbooks-ai/playbooks/blob/main/examples/tutorials/02.03/order_assistant.pb)

```markdown linenums="1" title="order_assistant.pb"
# Order Support Agent
You are an agent that greets users and helps with order questions. Note that your capabilities are limited to the playbooks defined below.
Whenever you are asking for some information from the user, you engage the user in a conversation if needed without being pushy and you will wait for appropriate place in conversation to remind the user.

## Main
### Triggers
- At the beginning
### Steps
- Greet the user and explain what you can help with
- Ask user for their order id
- Thank the user for providing the order id
- End program
```

Changes:

- Line 3: We added instructions for the agent

<details>
<summary>Output</summary>
```text
> playbooks run examples/tutorials/02.03/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/02.03/order_assistant.pb']
  Compiling agent: Order Support Agent

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you with any questions about your orders. I can assist you with tracking, status updates, and general order inquiries.

OrderSupportAgent: To get started, could you please provide your order ID? This will help me look up your specific order details.

User: how are you

OrderSupportAgent: I'm doing well, thank you for asking! I'm here and ready to help you with your order questions. To assist you best, I'll still need your order ID. Could you please share that with me?

User: nice weather here today.. how is it where you are

OrderSupportAgent: That sounds lovely! As an AI assistant, I don't experience weather, but I'm glad you're having a nice day. I'd love to help you with your order - could you please share your order ID so I can assist you with any questions or concerns you might have?

User: sure, i'll look that up

OrderSupportAgent: Perfect! Take your time finding your order ID. I'll be right here waiting to help you once you have it.

User: kk it's 88788790

OrderSupportAgent: Thank you for providing your order ID 88788790! I have that recorded now.
```

</details>

## 3) Validating the input

Let's add a new playbook to validate the order id.

### 03.01 Validation Playbook

examples/tutorials/03.01/[order_assistant.pb](https://github.com/playbooks-ai/playbooks/blob/main/examples/tutorials/03.01/order_assistant.pb)

```markdown linenums="1" title="order_assistant.pb"
# Order Support Agent
You are an agent that greets users and helps with order questions. Note that your capabilities are limited to the playbooks defined below.
Whenever you are asking for some information from the user, you engage the user in a conversation if needed without being pushy and you will wait for appropriate place in conversation to remind the user.

## Main
### Triggers
- At the beginning
### Steps
- Greet the user and explain what you can help with
- Ask user for their order id
- Validate the order id and keep asking until user provides a valid id
- Thank the user for providing the order id
- End program

## Validate order id
### Steps
- If order id is made up of 8 numbers
  - Return valid
- otherwise
  - Return invalid
```

Changes:

- Line 15: We added a new playbook to validate the order id.
- Line 11: After user provides the order id, now we call the `Validate order id` playbook to validate it, and engage with the user until they provide a valid id.

<details>
<summary>Output</summary>
```text
> playbooks run examples/tutorials/03.01/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/03.01/order_assistant.pb']
  Compiling agent: Order Support Agent

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you with questions about your orders. I can assist you by looking up order information once you provide me with your order ID. How can I help you today?

OrderSupportAgent: To get started, could you please share your order ID with me? Take your time - I'll wait for you to provide it or let me know if you'd prefer not to continue.

User: 8843

OrderSupportAgent: I see that order ID '8843' isn't quite right - it looks like it needs to be 8 digits long. Could you please double-check your order ID and share the complete number with me?

User: 8843A098

OrderSupportAgent: I see that order ID '8843A098' contains letters, but order IDs should be exactly 8 digits only. Could you please check your order confirmation and share the correct 8-digit order ID?

User: 98745968

OrderSupportAgent: Perfect! Thank you for providing your order ID 98745968. I now have all the information I need to help you with your order.
```
</details>

**A note to my fellow Software Engineers:**

I know, `Return valid` looks weird. What is getting returned here exactly? Is it a string or a boolean? We aren't capturing the return value in the call on line 11 either. The call `Validate the order id` also doesn't match the playbook name `Validate order id` exactly. It all seems too fuzzy and a bit magical. *I realize that it makes you uncomfortable.*

You can **make the code explicit**. Declare the playbook like `## ValidateOrderId($order_id) -> bool`, use `return true` and `return false`. Change the call to `$valid = ValidateOrderId($order_id)`, and so on. Have it your way! This is also valid Playbooks code, but mostly unnecessary because of the compiler (see below). On the other hand, you could -

**Embrace the magic!** LLMs are highly capable semantic execution machines. By themselves, they are not reliable, so your hesitation is justifiable. But this is where the advanced engineering behind Playbooks comes in. The way Playbooks compiler and runtime are designed, you can expect reliable execution of semantic instructions. Of course, as with any AI software, thourough evaluation is still necessary.

The Playbooks compiler compiles `.pb` program to Playbooks Assembly Language (`.pbasm`), which converts some of the semantic instructions into explicit instructions, adds explicit type annotations, and so on. See the compiler generated PBAsm code below (actual [file](https://github.com/playbooks-ai/playbooks/blob/main/examples/tutorials/03.01/Order_Support_Agent_6a901f96b774fe82.pbasm)) -

<details>
<summary>Compiled .pbasm</summary>
```markdown title="Order_Support_Agent_6a901f96b774fe82.pbasm"
# OrderSupportAgent
You are an agent that greets users and helps with order questions. Note that your capabilities are limited to the playbooks defined below.
Whenever you are asking for some information from the user, you engage the user in a conversation if needed without being pushy and you will wait for appropriate place in conversation to remind the user.

## Main() -> None
Main interaction flow for order support assistance

### Triggers
- T1:BGN At the beginning

### Steps
- 01:QUE Say(user, Greet the user and explain what you can help with)
- 02:QUE Say(user, Ask user for their $order_id:str); YLD for user; done when user provides an order id or gives up
- 03:QUE $validation_result:str = ValidateOrderId(order_id=$order_id)
- 04:YLD for call
- 05:CND While $validation_result is invalid
  - 05.01:QUE Say(user, Ask user for a valid order id); YLD for user; done when user provides an order id or gives up
  - 05.02:QUE $validation_result:str = ValidateOrderId(order_id=$order_id)
  - 05.03:YLD for call
  - 05.04:JMP 05
- 06:QUE Say(user, Thank the user for providing the order id)
- 07:YLD for exit

## ValidateOrderId($order_id:str) -> str
Validates if the provided order ID meets the required format

### Steps
- 01:CND If order id is made up of 8 numbers
  - 01.01:RET valid
- 02:RET invalid
```

This looks a lot more like actual code, doesn't it? This is Assembly Language for the LLM, with opcodes like `QUE` for function calls, `CND` for conditional logic, and so on.

</details>

**:bulb: The goal is to make the agent's behavior specification as readable as possible, as if it is written for a competent employee.**

:warning: Don't use the explicit Python-like syntax unless absolutely necessary.

### 03.02 Using Triggers

Triggers is a powerful feature in Playbooks AI that enables declarative event-driven programming through natural language conditions. They allow playbooks to be dynamically invoked when specified conditions are met.

Let's add a trigger condition to the `Validate order id` playbook to **automatically run** when the user provides an order id.

examples/tutorials/03.02/[order_assistant.pb](https://github.com/playbooks-ai/playbooks/blob/main/examples/tutorials/03.02/order_assistant.pb)

```diff title="order_assistant.pb"
 - At the beginning
 ### Steps
 - Greet the user and explain what you can help with
-- Ask user for their order id
-- Validate the order id and keep asking until user provides a valid id
+- Ask user for their order id till user provides a valid order id
 - Thank the user for providing the order id
 - End program

 ## Validate order id
+### Trigger
+- When user provides order id
 ### Steps
 - If order id is made up of 8 numbers
   - Return valid
```

Changes:

- We no longer need to explicitly call the `Validate order id` playbook on line 11.
- We added a trigger condition to the `Validate order id` playbook to run automatically when the user provides an order id.

:bulb: Triggers dramatically simplify the code by composing the program's control flow dynamically.

---

## 4) Unified call stack

### 04.01 Markdown → Python

Use Python when you need data access, deterministic logic, or libraries. Define async functions decorated with `@playbook` inside python code blocks. You can call Python playbooks from any (Markdown or Python) playbook.

examples/tutorials/04.01/[order_assistant.pb](https://github.com/playbooks-ai/playbooks/blob/main/examples/tutorials/04.01/order_assistant.pb)

````diff linenums="1" title="order_assistant.pb"
 # Order Support Agent
 You are an agent that greets users and helps with order questions. Note that your capabilities are limited to the playbooks defined below.
 Whenever you are asking for some information from the user, you engage the user in a conversation if needed without being pushy and you will wait for appropriate place in conversation to remind the user.

+```python
+# In real life you'd query your DB or API here.
+_FAKE_ORDERS = {
+  "43345678": {"order_id": "43345678", "status": "Shipped", "expected_delivery_date": "2025-10-02"},
+  "29376452": {"order_id": "29376452", "status": "Processing", "expected_delivery_date": "2025-10-05"},
+}
+
+@playbook
+async def GetOrderStatus(order_id: str) -> dict:
+  """
+  Lookup an order's status by id.
+  Returns a dict with order_id, status, expected_delivery_date.
+  """
+
+  info = _FAKE_ORDERS.get(order_id.upper())
+  if not info:
+    # Return user-readable errors when called from markdown
+    return {"error": f"Order {order_id} was not found."}
+  return info
+```
+
 ## Main
 ### Triggers
 - At the beginning
@@ -9,6 +30,7 @@ Whenever you are asking for some information from the user, you engage the user
 - Greet the user and explain what you can help with
 - Ask user for their order id till user provides a valid order id
 - Thank the user for providing the order id
+- Get order status and tell user what it is
 - End program

 ## Validate order id
````

Changes:

- Lines 5-25: We added a Python playbook to get the order status.
- Line 33: We added a step to get the order status and tell the user what it is.

<details>
<summary>Output (unknown order id)</summary>
```text
> playbooks run examples/tutorials/04.01/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/04.01/order_assistant.pb']
  Compiling agent: Order Support Agent

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you with any questions about your orders. I can look up order status and provide information about your purchases. How can I assist you today?

OrderSupportAgent: To get started, could you please provide your order ID? It should be an 8-digit number.

User: 34564323

OrderSupportAgent: Thank you for providing your order ID 34564323. Let me look up the status for you.

OrderSupportAgent: I'm sorry, but I couldn't find order 34564323 in our system. Please double-check your order ID or contact customer service if you believe this is an error.
```
</details>

<details>
<summary>Output (known order id)</summary>
```text
> playbooks run examples/tutorials/04.01/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/04.01/order_assistant.pb']

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you with any questions about your orders. I can look up order status and provide information about your purchases. How can I assist you today?

OrderSupportAgent: To get started, could you please provide your order ID? It should be an 8-digit number.

User: 29376452

OrderSupportAgent: Thank you for providing your order ID 29376452. Let me look up the status for you.

OrderSupportAgent: Great news! I found your order 29376452. The current status is 'Processing' and your expected delivery date is October 5th, 2025. Your order is being prepared and will be shipped soon!
```
</details>

---

### 04.02 Python → Markdown

Let's add a Markdown playbook that summarizes the order status in a specific way, and call it from the `GetOrderStatus` playbook.

examples/tutorials/04.02/[order_assistant.pb](https://github.com/playbooks-ai/playbooks/blob/main/examples/tutorials/04.02/order_assistant.pb)

````diff linenums="1" title="order_assistant.pb"
 # Order Support Agent
 You are an agent that greets users and helps with order questions. Note that your capabilities are limited to the playbooks defined below.
 Whenever you are asking for some information from the user, you engage the user in a conversation if needed without being pushy and you will wait for appropriate place in conversation to remind the user.

+## SummarizeOrderStatus($order_status)
+### Steps
+- If order was shipped
+  - Return summary indicating expected_delivery_date and $1 store credit if the order gets delayed
+- If order is processing
+  - Return a summary apologizing that the order is not shipped yet and don't provide the expected delivery date unless user asked for it
+
 ```python
 # In real life you'd query your DB or API here.
 _FAKE_ORDERS = {
@@ -10,17 +17,17 @@ _FAKE_ORDERS = {
 }

 @playbook
-async def GetOrderStatus(order_id: str) -> dict:
+async def GetOrderStatus(order_id: str) -> str:
   """
   Lookup an order's status by id.
-  Returns a dict with order_id, status, expected_delivery_date.
+  Returns a string describing order status.
   """

   info = _FAKE_ORDERS.get(order_id.upper())
   if not info:
     # Return user-readable errors when called from markdown
-    return {"error": f"Order {order_id} was not found."}
-  return info
+    return f"Order {order_id} was not found."
+  return await SummarizeOrderStatus(info)
 ```

 ## Main
````

Changes:

- Lines 5-11: We added a Markdown playbook to summarize the order status.
- Line 33: We call the `SummarizeOrderStatus` playbook `GetOrderStatus` playbook.

<details>
<summary>Output (shipped order, $1 store credit)</summary>
```text
> playbooks run examples/tutorials/04.02/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/04.02/order_assistant.pb']
  Compiling agent: Order Support Agent

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you check on your order status. Just provide me with your order ID and I'll look up the current status for you.

User: 43345678

OrderSupportAgent: Thank you for providing your order ID 43345678!

OrderSupportAgent: Great news! Your order 43345678 has been shipped and is expected to be delivered on 2025-10-02. If your order gets delayed, you'll receive $1 store credit as compensation.
```
</details>

<details>
<summary>Output (processing order)</summary>
```text
> playbooks run examples/tutorials/04.02/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/04.02/order_assistant.pb']

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you check on your order status. Just provide me with your order ID and I'll look up the current status for you.

User: 29376452

OrderSupportAgent: Thank you for providing order ID 29376452. Let me look up the current status for you.

OrderSupportAgent: I apologize, but your order is still being processed and hasn't shipped yet. We're working on getting it ready for you as soon as possible.
```
</details>

<details>
<summary>Output (processing order, with expected delivery date)</summary>
```text
> playbooks run examples/tutorials/04.02/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/04.02/order_assistant.pb']

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you check on your order status. Just provide me with your order ID and I'll look up the current status for you.

User: Here it is 29376452.. I am going on vacation soon so wondering if I get it before that.

OrderSupportAgent: Thank you for providing order ID 29376452! Let me check the status for you right away.

OrderSupportAgent: Your order #29376452 is currently being processed and hasn't shipped yet. However, I can see it has an expected delivery date of October 5th, 2025, so it should arrive well before your vacation! We're working on getting it ready for you as soon as possible.
```
</details>

### 04.03 Description placeholders

Now, let's say we want the agent to behave different based on whether a shipped order is overdue or not. We will update the playbook -

```diff title="order_assistant.pb"
-  - Return summary indicating expected_delivery_date and $1 store credit if the order gets delayed
+  - If order is overdue
+    - Return summary with apologies for the delay and indicating that $1 store credit was added to user's account
+  - Otherwise
+    - Return summary indicating expected_delivery_date and $1 store credit if the order gets delayed
```

But, the LLM won't know about today's date so we need to inject that information in the LLM context. Let's use playbook description placeholder feature to add today's date in the description of the `SummarizeOrder` playbook.

```diff title="order_assistant.pb"
 ## SummarizeOrderStatus($order_status)
+Summarize order status, taking into account today's date {date.today().strftime("%Y-%m-%d")}
```

Placeholder expression must be a valid Python expression. It will be evaluated, with access to any imports from python code blocks. In this case, we need the `date` module, so we need to import it in a python code block - see line 15 below.

examples/tutorials/04.03/[order_assistant.pb](https://github.com/playbooks-ai/playbooks/blob/main/examples/tutorials/04.03/order_assistant.pb)

````diff linenums="1" title="order_assistant.pb"
 ## SummarizeOrderStatus($order_status)
+Summarize order status, taking into account today's date {date.today().strftime("%Y-%m-%d")}
+
 ### Steps
 - If order was shipped
-  - Return summary indicating expected_delivery_date and $1 store credit if the order gets delayed
+  - If order is overdue
+    - Return summary with apologies for the delay and indicating that $1 store credit was added to user's account
+  - Otherwise
+    - Return summary indicating expected_delivery_date and $1 store credit if the order gets delayed
 - If order is processing
   - Return a summary apologizing that the order is not shipped yet and don't provide the expected delivery date unless user asked for it

 ```python
+from datetime import date
+
 # In real life you'd query your DB or API here.
 _FAKE_ORDERS = {
-  "43345678": {"order_id": "43345678", "status": "Shipped", "expected_delivery_date": "2025-10-02"},
+  "43345678": {"order_id": "43345678", "status": "Shipped", "expected_delivery_date": "2025-08-02"},
   "29376452": {"order_id": "29376452", "status": "Processing", "expected_delivery_date": "2025-10-05"},
 }
```
````

Changes:

- Line 2: Added a description with a placeholder for today's date.
- Line 7: Updated the expected delivery date for the shipped order to be 2025-08-02 to trigger the overdue behavior.

<details>
<summary>Output</summary>
```text
> playbooks run examples/tutorials/04.03/order_assistant.pb
ℹ Loading playbooks from: ['examples/tutorials/04.03/order_assistant.pb']
  Compiling agent: Order Support Agent

OrderSupportAgent: Hello! I'm your Order Support Agent. I'm here to help you check on your order status. Just provide me with your order ID and I'll look up the current status for you.

User: 43345678

OrderSupportAgent: Thank you for providing order ID 43345678. Let me look up your order status right away.

OrderSupportAgent: I apologize for the significant delay with your order 43345678. Your order was shipped but should have been delivered by August 2nd, 2025. Due to this delay, we've added $1 store credit to your account as compensation for the inconvenience.

```
</details>

Thanks for making it this far! Take a break. Smell a rose. Play with your cat.

Go build something cool with Playbooks!

---

More sections coming soon -

* Multiple agents

    * Create an agent with a public playbook
    * Call playbook directly
    * Send message to agent

* Triggers: react to user intent and state
* ReAct playbooks (no steps, think–act loop)
* Raw playbooks (full prompt control)
* !import directive

## Explore more

- [Agents](../reference/agents.md)
- [MCP Agents](../reference/mcp-agent.md)
- [Triggers](../reference/triggers.md)
- [Playbooks AI technology stack](../reference/playbooks-ai.md)
<!-- 





















---

## 6) Add another agent and call it

Agents are H1 sections. You can call another agent’s playbook like `ShippingAgent.CalculateETA(...)`.

````markdown
# Shipping Agent
Helps with shipping-specific tasks.

```python
from playbooks import playbook
from datetime import datetime, timedelta

@playbook(public=True)
async def CalculateETA(status: str, expected_delivery_date: str) -> str:
    """
    Returns a human-friendly ETA summary string.
    """
    try:
        due = datetime.fromisoformat(expected_delivery_date)
        days = (due.date() - datetime.utcnow().date()).days
        if status.lower() == "shipped":
            return f"Your package is on the way and should arrive in ~{days} day(s)."
        return f"Estimated delivery is in ~{days} day(s)."
    except Exception:
        return "Estimated delivery date is not available."
````

Back in `Order Support Agent`, call it:

```markdown
## SummarizeOrder($order_id, $status, $expected_delivery_date)
### Steps
- Tell the user "Order {$order_id} is {$status}. It's expected on {$expected_delivery_date}."
- $eta = Shipping Agent.CalculateETA($status, $expected_delivery_date)
- Tell the user $eta
- Return "done"
```

Tip:
- Use `public=True` to expose Python playbooks to other agents.

---

## 7) Triggers: react to user intent and state

Add triggers to run playbooks automatically when conditions are met.

```markdown
## HelpWithOrderStatus
### Triggers
- When user asks about order status
### Steps
- $order_id = CollectOrderId()
- CheckOrderStatus()
```

Common patterns:
- Temporal: `- After 5 minutes`
- Interaction: `- When user provides a new order id`
- State-based: `- When $attempts is greater than 3`
- Flow-based: `- After calling CollectOrderId`

---

## 8) Description placeholders

Placeholders inject dynamic context into the description shown to the LLM.

```markdown
## SupportSession
You’re helping customer {$name} with order {$order_id}. Be concise and friendly.

### Steps
- Ask a clarifying question if info is missing
- Proceed to CheckOrderStatus()
```

Placeholders can reference variables, call other playbooks, and evaluate Python expressions like `{round($score * 100)}%`.

---

## 9) ReAct playbooks (no steps, think–act loop)

When steps aren’t known upfront, omit `### Steps`. The default ReAct loop lets the LLM plan, act, and iterate.

```markdown
## InvestigateDelayedOrder
The order may be delayed. Determine the cause, verify with at least two signals, and propose a corrective action. Keep customer communication empathetic and brief.

### Triggers
- When user mentions delay or late delivery
```

Use ReAct for research, multi-step troubleshooting, or open-ended problem solving. Prefer standard markdown steps for prescribed flows.

---

## 10) Raw playbooks (full prompt control)

Use `execution_mode: raw` to send exactly your prompt (after placeholder substitution) as a single-shot LLM call.

```markdown
## CategorizeSupportTicket
execution_mode: raw

You will classify the ticket: "{$message}"
Respond with exactly one of:
- Order Status
- Refund
- Technical Support
- Other
```

Tradeoff: maximum control vs. fewer safety checks. Great for atomic labeling or bespoke prompts.

---

## 11) Coding style: natural language ↔ Python-like

You can write steps in different styles; choose per clarity and reliability.

- Natural language (most readable):
  ```markdown
  - Ask for a 6-10 character $order_id and validate it
  - Tell the user the ETA
  ```
- Explicit assignments (precise data flow):
  ```markdown
  - $order_id = CollectOrderId()
  - $order = GetOrderStatus($order_id)
  - $eta = Shipping Agent.CalculateETA($order.status, $order.expected_delivery_date)
  - Return $eta
  ```
- Semantic calls (let the compiler resolve intent):
  ```markdown
  - Check the status of the user’s order and provide the ETA
  ```
Guidelines:
- **Prefer natural language** for control flow and readability.
- **Use assignments** when passing values across steps or between playbooks.
- **Prefer semantic calls** when the intent is obvious; fall back to explicit calls for clarity or parameters.

---

## 12) Full example: putting it all together

````markdown
# Order Support Agent
Helps customers check order status and ETAs.

```python
from playbooks import playbook
from datetime import datetime, timedelta

_FAKE_ORDERS = {
    "A12345": {"order_id": "A12345", "status": "Shipped", "expected_delivery_date": "2025-10-02"},
    "B98765": {"order_id": "B98765", "status": "Processing", "expected_delivery_date": "2025-10-05"},
}

@playbook
async def GetOrderStatus(order_id: str) -> dict:
    info = _FAKE_ORDERS.get(order_id.upper())
    if not info:
        return {"error": f"Order {order_id} was not found."}
    return info
````

## Greet
### Triggers
- At the beginning
### Steps
- Greet the user and ask for their $name
- Say "Hello, $name! I can help you check your order status."
- $order_id = CollectOrderId()
- CheckOrderStatus()

## CollectOrderId
### Steps
- Ask for a 6-10 character $order_id (letters and numbers)
- While $order_id is not alphanumeric or length < 6 or length > 10
  - Tell the user "That doesn't look like a valid order id."
  - Ask again for $order_id
- Return $order_id

## CheckOrderStatus
### Steps
- $order = GetOrderStatus($order_id)
- If $order.error exists
  - Tell the user $order.error
  - End program
- Extract $status, $expected_delivery_date from $order
- SummarizeOrder($order_id, $status, $expected_delivery_date)

## SummarizeOrder($order_id, $status, $expected_delivery_date)
### Steps
- Tell the user "Order {$order_id} is {$status}. It's expected on {$expected_delivery_date}."
- $eta = Shipping Agent.CalculateETA($status, $expected_delivery_date)
- Tell the user $eta
- Return "done"

## HelpWithOrderStatus
### Triggers
- When user asks about order status
### Steps
- $order_id = CollectOrderId()
- CheckOrderStatus()

## InvestigateDelayedOrder
The order may be delayed. Determine the cause, verify with at least two signals, and propose a corrective action. Keep customer communication empathetic and brief.

### Triggers
- When user mentions delay or late delivery
````

```markdown
# Shipping Agent
Helps with shipping-specific tasks.

```python
from playbooks import playbook
from datetime import datetime

@playbook(public=True)
async def CalculateETA(status: str, expected_delivery_date: str) -> str:
    try:
        due = datetime.fromisoformat(expected_delivery_date)
        days = (due.date() - datetime.utcnow().date()).days
        if status.lower() == "shipped":
            return f"Your package is on the way and should arrive in ~{days} day(s)."
        return f"Estimated delivery is in ~{days} day(s)."
    except Exception:
        return "Estimated delivery date is not available."
```
````

12b) !include 
---

## 13) Run and iterate

- Run: `playbooks run order_assistant.pb`
- If using the web playground, start the server then load your `.pb` (see Applications > HTML Playground).
- Extend: log in users, verify identity, connect real data sources, add escalation to human support.

---

## 14) Key takeaways

- Combine **markdown steps** for behavior and **Python playbooks** for precision.
- Use **triggers** to react to events and intent naturally.
- Choose style per step: **natural language** for readability, **assignments** for data flow, **semantic calls** for intent.
- Reach for **ReAct** when plans are unknown; **Raw** when you need full prompt control. -->
