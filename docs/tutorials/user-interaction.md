# User Interaction

In this tutorial, you'll learn how to create playbooks that interact with users, gather input, and respond dynamically.

## Objective

By the end of this tutorial, you'll understand:

- How to ask users for information
- How to store user responses in variables
- How to validate user input
- How to create conversational flows that adapt to user input

## Prerequisites

- Completion of [Adding Triggers](adding-triggers.md)
- Understanding of playbook structure and triggers

## Basic User Interaction

The most basic form of user interaction is asking a question and receiving a response. Let's create a simple example:

```markdown
# Personalized Greeting
This program greets the user by name

## Greet
### Triggers
- At the beginning
### Steps
- Ask the user for their name
- Say hello to the user by name and welcome them to Playbooks
- End program
```

## Storing User Responses in Variables

To create more complex interactions, you'll often need to store user responses in variables for later use:

```markdown
# Personal Information
This program collects and uses personal information.

## Collect
### Triggers
- At the beginning
### Steps
- Ask the user for their $name
- Ask the user for their favorite $color
- Say hello to the user by $name and say that your will remember their favorite color is $color
- End program
```

In this example:

- `$name` stores the user's name
- `$color` stores the user's favorite color
- These variables are then used in the response

## Input Validation

You can validate user input using natural language conditions:

```markdown
# PIN Validator
This program validates a user's PIN.

## Main
### Triggers
- At the beginning
### Steps
- Ask the user to enter a 4-digit $pin
- While $pin is not a 4-digit number
  - Tell the user their PIN is invalid
  - Ask the user to enter a 4-digit $pin again
- Tell the user their PIN has been accepted
- End program
```

This example:

- Asks for a PIN
- Checks if the PIN is a 4-digit number
- If not, it asks again until a valid PIN is provided

## Handling Specific Responses

You can create branching conversations based on user responses:

```markdown
# Food Preference
This program recommends restaurants based on food preferences.

## Main
### Triggers
- At the beginning
### Steps
- Ask the user what type of food they're in the mood for
- $preference = user's response
- If $preference indicates Italian food
  - Tell the user about some great Italian restaurants
- If $preference indicates Mexican food
  - Tell the user about some great Mexican restaurants
- If $preference indicates Asian food
  - Tell the user about some great Asian restaurants
- Otherwise
  - Tell the user you don't have recommendations for that type of food
- End program
```

This example creates different responses based on the keywords in the user's input.

## Advanced Validation Using Triggers

For more sophisticated validation, you can use triggers to handle user input:

```markdown
# Account Access
This program validates user credentials.

## Main
### Triggers
- At the beginning
### Steps
- Ask user for a $pin
- Ask user for $email
- Load user account
- Tell the user their account balance

## Validation($pin)
### Triggers
- When user provides a PIN
### Steps
- While $pin is not 4 digits
  - Tell user $pin is not valid and ask for $pin again
  - If the user gives up
    - Apologize and end the conversation
- Return $pin

## EmailValidation($email)
### Triggers
- When user provides an email
### Steps
- While email is not a valid email or is a throwaway email
  - Tell user email is not valid and ask for email again
- Return email
```

In this example:

- The `Validation` playbook triggers when a user provides a PIN
- It validates that the PIN is 4 digits
- Similarly, the `EmailValidation` playbook validates email addresses

## Creating a Practical Example

Let's put everything together in a practical example that collects user information:

1. Create a new file named `user-form.md` with the following content:

```markdown
# User Registration
This program collects registration information from users.

## Main
### Triggers
- At the beginning
### Steps
- Welcome the user to the registration process
- Ask the user for their $name
- Ask the user for their $email
- Ask the user to create a $password
- Ask the user for their $age
- Tell the user: "Thank you, $name! Your registration is complete."
- Provide a summary of the collected information (excluding the password)
- End program

## EmailValidation
### Triggers
- When user provides an email address
### Steps
- While $email does not contain "@" and "."
  - Tell the user their email is invalid
  - Ask the user to provide a valid $email address
- Return $email

## PasswordValidation
### Triggers
- When user creates a password
### Steps
- While length of $password < 8
  - Tell the user their password is too short
  - Ask the user to create a stronger password with at least 8 characters
  - $password = user's response
- Return $password

## AgeValidation($age)
### Triggers
- When user provides their age
### Steps
- While $age < 18 or $age > 120
  - If $age < 18
    - Tell the user they must be 18 or older to register
  - If $age > 120
    - Tell the user the provided age seems incorrect
  - Ask the user to provide their correct $age
- Return $age
```

2. Run your playbook:

```bash
python src/playbooks/applications/agent_chat.py user-form.md --verbose
```

When you run this program, you'll experience:

- A guided registration process
- Different validation rules for each field
- Trigger-based validation that runs automatically when the user provides input

## Best Practices for User Interaction

- Be clear about what information you're requesting
- Provide helpful error messages when validation fails
- Use variables to personalize responses
- Break complex interactions into multiple steps
- Use triggers for validation to keep your main flow clean
- Always provide feedback so users know their input was received

## Exercises

1. Create a playbook that plays a simple number guessing game
2. Extend the registration form to collect additional information like address or phone number
3. Create a playbook that adapts its responses based on the user's sentiment (detected from their responses)

## Next Steps

Now that you know how to interact with users, you're ready to learn about [Calling Playbooks](calling-playbooks.md) to create more modular programs. 