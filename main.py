from agents import PolicyBot, MonitorBot
from crewai import Crew, Task

# Task 1 — Ask a policy question
task1 = Task(
    description="""Analyze and explain the company's policy on remote work and flexible hours.
    Please provide:
    1. Eligibility criteria
    2. Application process
    3. Any department-specific variations
    4. Core working hours requirements
    5. Equipment and workspace requirements
    
    If specific policy details are not available, clearly state this and suggest where to find the information.""",
    agent=PolicyBot
)

# Task 2 — Analyze a suspicious log entry
log_sample = """\
[ERROR] 2025-04-23 10:12:45 - AuthService - Multiple failed login attempts from IP 192.168.1.100
[WARN] 2025-04-23 10:13:02 - Disk usage exceeds 90% on /dev/sda1
[INFO] 2025-04-23 10:13:15 - BackupService - Starting scheduled backup
[ERROR] 2025-04-23 10:13:30 - AuthService - Account locked: user@example.com
"""

task2 = Task(
    description=f"""Analyze the following system logs and provide a detailed security report:
    
    {log_sample}
    
    Please include:
    1. Severity assessment for each event
    2. Potential security implications
    3. Recommended immediate actions
    4. Suggested preventive measures
    5. Any patterns or correlations between events""",
    agent=MonitorBot
)

# Create the crew with both agents
crew = Crew(
    agents=[PolicyBot, MonitorBot],
    tasks=[task1, task2],
    verbose=True
)

# Run the interaction
crew.kickoff()
