# Speed
max_threads = 100       # Maximum number of threads the program will work with.
thread_multiplier = 10  # Multiplies the number of threads passed in the flag. (must be greater than 0)
delay = 0.4             # Delay between request attempts.

# View
debug = False           # Debug mode to show hidden program runtime information.
logo = True             # Enables or disables the program logo.
output_print = True     # Enables or disables any print screen within the program (the progress bar remains active and the resulting links are still displayed).
color = True            # Activates or deactivates any color in the program.
color_ansi = ""         # Changes the overall color of the program, like a theme. ("" -> off)
update_bar = 0.01       # tqdm bar update time.

# Update
auto_update = False     # Updates the boards automatically.

#bonus
logs = False            # Enables detailed execution logs saved to a log file.
auto_cls = False        # Executes the "cls" command automatically.
all_boards = False      # Enables searching on all boards; not recommended for use by anyone other than developers.