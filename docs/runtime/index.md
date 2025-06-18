# Playbooks Runtime
Playbooks runtime executes Playbooks Assembly Language (PBASM) programs. This is structured as a runtime main loop that repeatedly calls LLM to execute a fragment of a playbook each time. 

- Runtime main loop
  - Decide which playbook to execute next
    - If processing a specific playbook call with provided parameters, load that playbook to execute
    - If call stack is empty, load all BGN triggerred playbooks to execute
  - Executing a playbook
    - Markdown Playbook execution loop
      - Call LLM to execute the next fragment of the playbook
        - Parse LLM response
        - Verify LLM control flow and detect unexpected control flow
        - Update execution state, variables, call stack, etc.
        - Execute any queued playbooks
    - Python Playbook execution loop
      - Use an isolated Python environment to execute the playbook function
    - External Playbook (i.e. playbook from another Agent) execution loop
      - Use an isolated Python environment to execute the playbook function which calls appropriate agent / external service, such as MCP or Playbooks server.


## Runtime Execution Contract

The PBAsm runtime contract ensures deterministic execution despite the probabilistic nature of LLMs:

### LLM Output Format
```
recap – one-sentence summary of current state
plan  – one-sentence immediate goal
`Var[$name, <value>]`
`SaveArtifact($name, "summary", "content...")`
trig? <no | `Trigger["PB:Ln:Code"]`>
`Step["Playbook:LineNumber:CommandCode"]` optional inline: `Say("…")` or `$x = Func($y)`
trig? <no | `Trigger["PB:Ln:Code"]`>
what? handle unexpected situation intelligently and safely
`Step["Playbook:LineNumber:CommandCode"]` `Return[<value> | ]` `Var[$__, 1-5 line summary]`
yld <user | call | exit>
```

- `recap` and `plan` start the response.
- For every executed step, one or more of the following are output:
  - `Var[$name, <value>]` is used to update the state.
  - `Step["Playbook:LineNumber:CommandCode"]` is used to execute a step.
  - `trig? <no | `Trigger["PB:Ln:Code"]`>` is used to check for triggers.
- Finally, `yld <user | call | exit>` is produced and control is yielded back to the runtime main loop.

### Verification Rules
1. **Structured parsing**: All outputs must be parseable by the runtime
2. **Variable tracking**: State changes must be explicitly declared with types
3. **Trigger evaluation**: Must check for triggers after each step and variable update
4. **Execution tracing**: Each step must be logged with precise line numbers
5. **Control flow**: Must use proper yield statements for control transfer
6. **Summary generation**: Must generate $__ variable with execution summary before returning


