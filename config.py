# Speed
max_threads = 150       # Maximum number of threads the program will work with.
thread_multiplier = 1   # Take the maximum number of threads and multiply it by that number.
delay = 0.15            # Delay between requests.

# View
debug = False           # Debug mode to show hidden program runtime information.
logo = True             # Enables or disables the program logo.
output_print = True     # Enables or disables any print screen within the program (the progress bar remains active and the resulting links are still displayed).
logs = False            # Enables detailed execution logs saved to a log file.
color = True            # Activates or deactivates any color in the program.
color_ansi = ""         # Changes the overall color of the program, like a theme.

# Update
auto_update = False     # Updates the boards automatically.

# Network
from httpx import Client, Timeout, Limits
clients_number = 2      # Number of simultaneous customers.
clients = [Client(      # Global client for requesting an HTTPX library.
    http2=True,
    timeout= Timeout(4.0, connect=1.5),
    limits= Limits(
        max_keepalive_connections=70,
        max_connections= 70
    ),
    headers = {
        "Connection": "keep-alive",
        "Accept-Encoding": "br, gzip"
    }
) for _ in range(clients_number)]