import os
from dotenv import load_dotenv
from agents import policy_tool

# Load environment variables
load_dotenv()

print("\n📘 Welcome to NeoEdge PolicyBot CLI!")
print("Type your company policy questions below.")
print("Type 'exit' to quit.\n")

while True:
    query = input("🔍 Ask PolicyBot: ").strip()
    if query.lower() in ["exit", "quit"]:
        print("👋 Exiting. Have a good day!")
        break
    if not query:
        continue
    try:
        result = policy_tool.run(query)
        print("\n🧠 PolicyBot Response:\n" + result + "\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
