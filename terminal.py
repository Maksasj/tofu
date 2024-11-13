import os
import pty
import subprocess
import time

class VirtualTerminal:
    def __init__(self):
        try:
            # Create a pseudo-terminal
            self.master_fd, self.slave_fd = pty.openpty()
            
            # Start a shell in the child process
            self.process = subprocess.Popen(
                "/bin/bash",  # Or "/bin/sh" or the shell of your choice
                stdin=self.slave_fd,
                stdout=self.slave_fd,
                stderr=self.slave_fd,
                text=True
            )
            
            # Give some time for the shell to initialize
            time.sleep(0.1)
        except Exception as e:
            self.close()
            raise RuntimeError(f"Failed to initialize shell: {e}")
        
    def execute_command(self, command):
        try:
            # Send command to the shell
            os.write(self.master_fd, (command + "\n").encode())
            
            # Read output until prompt (could vary depending on shell prompt settings)
            output = b""
            while True:
                try:
                    data = os.read(self.master_fd, 1024)
                    if not data:
                        break
                    output += data
                    # Stop reading if we get a prompt, usually "$ " or "# "
                    if b"$ " in output or b"# " in output:
                        break
                except OSError:
                    break

            return output.decode()
        except OSError as e:
            return f"Error during command execution: {e}"
    
    def close(self):
        # Ensure proper cleanup of resources
        if self.process:
            self.process.terminate()
            self.process.wait()
        if self.master_fd:
            os.close(self.master_fd)
        if self.slave_fd:
            os.close(self.slave_fd)