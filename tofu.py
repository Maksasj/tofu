import utils

from openai import OpenAI
import sys
import subprocess

client = OpenAI()

history = [
    { "role": "system", "content": utils.read_file_content("prompts/system_prompt.txt")},
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