from backend.agent import run_agent

ticket_id = None

print("Zen agent (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    result = run_agent(
        user_message=user_input,
        ticket_id=ticket_id
    )

    ticket_id = result.get("ticket_id")

    print("\nAgent:", result["response"])
    print(f"(ticket_id={ticket_id})\n")
