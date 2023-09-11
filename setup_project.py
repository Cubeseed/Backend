import platform
import subprocess
import sys

def run_command(command, exit_on_fail=True):
    if platform.system() == "Windows":
        shell = True
        executable = None
    else:
        shell = True
        executable = '/bin/bash'
    
    process = subprocess.Popen(command, shell=shell, executable=executable, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(stderr.decode())
        if exit_on_fail:
            exit(1)
        else:
            return False
    print(stdout.decode())
    return True

def check_pip_installed():
    print("Checking for pip installation...")
    return run_command("pip --version", exit_on_fail=False)

def main():
    # Check if pip is installed
    if not check_pip_installed():
        print("pip is not installed. Please install pip and try again.")
        exit(1)

    # Check if --start-server option is provided
    start_server = '--start-server' in sys.argv

    # Set up and activate virtual environment
    python_command = "python3" if platform.system() != "Windows" else "python"
    run_command(f"{python_command} -m venv env")
    
    if platform.system() == "Windows":
        run_command("env\\Scripts\\activate.bat")
    else:
        run_command("source env/bin/activate")

    # Install all project dependencies
    run_command("pip install -r requirements.txt")

    # Migrate database
    run_command(f"{python_command} manage.py migrate")

    # Run the project server locally if the option is provided
    if start_server:
        run_command(f"{python_command} manage.py runserver")

if __name__ == "__main__":
    main()
