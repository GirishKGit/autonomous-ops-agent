import logging
from agents import security_analysis_with_mcp

logging.basicConfig(level=logging.INFO)

def run_security_cli():
    print("\n🛡️ Welcome to NeoEdge Security Analyst CLI!")
    print("Paste your system logs below. Type 'exit' to quit.\n")

    while True:
        log_input = input("📜 Enter logs to analyze:\n").strip()

        if log_input.lower() == 'exit':
            print("👋 Exiting. Stay secure!")
            break

        if not log_input:
            print("⚠️ Please enter a non-empty log entry.")
            continue

        logging.info(f"Received log input: {log_input}")

        try:
            response = security_analysis_with_mcp(log_input)
            print("\n🧠 MonitorBot Analysis:\n" + response + "\n")
        except Exception as e:
            print(f"❌ Error processing log: {str(e)}")

if __name__ == "__main__":
    run_security_cli()
