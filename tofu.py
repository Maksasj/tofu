import utils
from agent import Agent

import sys
import subprocess

agent = Agent("gpt-4o-mini")
agent.load_system_prompt("prompts/system_prompt.txt")

def run_shell_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

while True:
    command = agent.get_next_command()
    print("Command to run: '" + command + "'")

    if "IM DONE" in command:  # You can add a more specific check if needed
            break

    # Run the shell command
    stdout, stderr = run_shell_command(command)
    
    # Check for errors in the execution
    if stderr:
        result = "" + command + " - FAILED, WITH ERROR '" + stderr + "'"
        print("    " + result)

        history.append({
            "role": "assistant",
            "content": result
        })
    else:
        result = "" + command + " - RUNNED SUCCESSFULLY, AND PRINTED '" + stdout + "'"
        print("    " + result)

        history.append({
            "role": "assistant",
            "content": result
        })

  
    # Continue with the next iteration
    sys.stdout.flush()