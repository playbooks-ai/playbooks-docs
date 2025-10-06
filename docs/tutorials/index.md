# Tutorial: Building an Order Status Assistant

**Goal**: Learn Playbooks by building a customer support AI assistant that checks order status. You'll start with "hello world" and progressively add user input, validation, Python playbooks, and more.

**What you'll learn**:

- Writing your first agent and playbook
- Collecting and validating user input
- Using triggers for automatic validation
- Mixing Python and Markdown playbooks
- Injecting dynamic context with description placeholders

**Prerequisites** (see [Getting Started](../getting-started/index.md)):

- Installed Playbooks
- Successfully ran a program using `playbooks run <program>.pb`

:information_source: **Code**: All examples available [here](https://github.com/playbooks-ai/playbooks/tree/main/examples/tutorials)

:bulb: **New to Playbooks?** This tutorial teaches by example. For comprehensive reference, see the [Programming Guide](../programming-guide/index.md).

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

**:bulb: The goal is to make the agent's behavior specification as readable as possible, 
as if it is written for a competent employee.**

:books: **Learn more**: See [Natural Language vs Explicit Syntax](../programming-guide/index.md#natural-language-vs-explicit-syntax) in the Programming Guide.

### 03.02 Using Triggers

Triggers automatically invoke playbooks when conditions are met - like CPU interrupts. Let's add a trigger to the `Validate order id` playbook to **automatically run** when the user provides an order id.

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

:bulb: **Key Benefit**: Main flow stays clean. Validation happens automatically. No explicit validation calls needed.

:books: **Learn more**: See [Triggers: Event-Driven Programming](../programming-guide/index.md#triggers-event-driven-programming) for patterns, best practices, and when to use (or avoid) triggers.

---

## 4) Mixing Python and Markdown Playbooks

### 04.01 Markdown → Python

Use Python playbooks when you need data access, deterministic logic, or external libraries. Define async functions decorated with `@playbook` inside python code blocks.

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

:books: **Learn more**: See [Python Playbooks - Hard Logic](../programming-guide/index.md#4-python-playbooks-hard-logic) for full details, decorator options, and when to extract Python playbooks to MCP servers.

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

### 04.03 Description Placeholders

We want to check if a shipped order is overdue, but the LLM doesn't know today's date. We can inject dynamic information using **description placeholders** with `{expression}` syntax:

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

Placeholder expressions are evaluated when the playbook starts. They can access variables, call playbooks, and use Python expressions. Import any needed modules in a Python code block.

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

:books: **Learn more**: See [Programming Guide](../programming-guide/index.md) for advanced patterns and best practices.

---

## Next Steps

Congratulations! You've built a working order assistant that:

- ✅ Greets users and collects input conversationally
- ✅ Validates input automatically with triggers
- ✅ Mixes Python and Markdown playbooks seamlessly
- ✅ Injects dynamic context with placeholders

**Continue Learning**:

- **[Programming Guide](../programming-guide/index.md)** - Comprehensive reference covering all features
  - [Multi-Agent Programs](../programming-guide/index.md#multi-agent-programs) - Multiple agents, meetings, cross-agent calls
  - [ReAct Playbooks](../programming-guide/index.md#2-react-playbooks-dynamic-reasoning) - Dynamic planning when steps aren't predetermined
  - [Raw Playbooks](../programming-guide/index.md#3-raw-prompt-playbooks-full-control) - Full prompt control for single-shot tasks
  - [Common Patterns](../programming-guide/index.md#common-patterns-and-best-practices) - Best practices and real-world patterns

**Reference Documentation**:

- [Agents](../reference/agents.md) - Agent configuration and structure
- [MCP Agents](../reference/mcp-agent.md) - Integrating external tools via MCP
- [Triggers](../reference/triggers.md) - Event-driven programming details
- [Playbook Types](../reference/playbook-types.md) - Deep dive on all playbook types

**Ready to build?** Start with the [Programming Guide](../programming-guide/index.md) and explore the examples in the [Playbooks repository](https://github.com/playbooks-ai/playbooks/tree/main/examples).
