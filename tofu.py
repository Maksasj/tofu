import sys
import utils
from agent import Agent

if __name__ == "__main__":
    agent = Agent("gpt-4o-mini")
    agent.load_system_prompt("prompts/system_prompt.txt")
    agent.load_user_prompt(input())

    while True:
        command = agent.get_next_command()
        print("Command to run: '" + command + "'")

        if "IM DONE" in command:
            break

        stdout, stderr = utils.run_shell_command(command)
        
        if stderr:
            result = "FAILED, WITH ERROR '" + stderr + "'"
            agent.save_command_result(result)
        else:
            result = "RUNNED SUCCESSFULLY, AND PRINTED '" + stdout + "'"
            agent.save_command_result(result)
    
        sys.stdout.flush()