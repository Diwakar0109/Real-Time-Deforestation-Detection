import subprocess

try:
    subprocess.run(["python", "history.py"], check=True)
    print("Completed history.py.\n")
except subprocess.CalledProcessError as e:
    print(f"Error while running history.py: {e}")
    exit(1)

try:
    subprocess.run(["python", "tree_identify.py"], check=True)
    print("Completed tree_identify.py.\n")
except subprocess.CalledProcessError as e:
    print(f"Error while running tree_idetify.py: {e}")
    exit(1)

try:
    subprocess.run(["python", "api.py"], check=True)
    print("Completed api.py.\n")
except subprocess.CalledProcessError as e:
    print(f"Error while running api.py: {e}")
    exit(1)

try:
    subprocess.run(["python", "tree_image.py"], check=True)
    print("Completed tree_image.py.\n")
except subprocess.CalledProcessError as e:
    print(f"Error while running tree_image.py: {e}")
    exit(1)

try:
    subprocess.run(["python", "check_def.py"], check=True)
    print("Completed check_def.py.\n")
except subprocess.CalledProcessError as e:
    print(f"Error while running check_def.py: {e}")
    exit(1)

print("Workflow Completed")