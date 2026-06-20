import subprocess


print("Sending a background ping probe...")

# Running the system command silently
# We pass the command as a list of individual string arguments
response = subprocess.run(["ping", "-n", "1", "8.8.8.8"], capture_output=True, text=True)

# The text output is safely stored inside the 'stdout' attribute of our response object
raw_output = response.stdout

print("--- Capture Successful! Here is the text Python trapped: ---")
print(raw_output)
