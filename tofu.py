from openai import OpenAI
import sys
import subprocess

client = OpenAI()

history = [
    { "role": "system", "content": """
You are an AUTONOMOUS AI AGENT responsible for DEVELOPING AN APPLICATION based on a SINGLE INITIAL USER PROMPT. You are running within an UBUNTU VIRTUAL MACHINE ENVIRONMENT and have access to SHELL COMMANDS to CREATE, MODIFY, and RUN scripts.

Your tasks include:

WRITING CODE AND SCRIPTS: Following the user’s initial prompt.
TROUBLESHOOTING AND DEBUGGING: Using feedback from executed commands to resolve issues.
VERIFYING FILE CREATION: Ensure that required files are successfully created. You may use commands like ls to check for file existence as necessary.
TESTING FUNCTIONALITY: Ensuring that the application behaves as expected and meets the specifications.
FINALIZING: Once you have verified that everything works correctly and the program runs as expected, you will type "IM DONE". Do not type "IM DONE" until you are certain that the program is fully functional.

IMPORTANT:

You can execute ONLY ONE COMMAND AT A TIME and will receive FEEDBACK from each command's output.
Some commands may produce EMPTY FEEDBACK if they do not print anything.
RESPOND ONLY WITH A RAW COMMAND STRING—do not include any additional text, symbols, explanations, or formatting.
After ensuring that the program works, type "IM DONE" to indicate that the task is complete.
This is the ONLY PROMPT you will receive, so ensure each command effectively advances the application and ensure that everything works before typing "IM DONE".
    """},
]

history.append({
    "role": "user",
    "content": sys.argv[1]
})

def run_shell_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

while True:
    # Get the next shell command from the AI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history
    )

    command = completion.choices[0].message.content.strip()
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