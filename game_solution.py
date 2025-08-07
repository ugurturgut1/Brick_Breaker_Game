import tkinter as tk
from PIL import Image, ImageTk
import random

# Game settings
width = 600
height = 400
brick_width = 50
brick_height = 20
paddle_width = 80
paddle_height = 10
ball_size = 10
ball_speed = 5
brick_rows = 9
brick_cols = 11

# Color settings
brick_colors = [
    "#FF00FF", "#00FFFF", "#00FF00", "#FFFF00", "#FF5F00",
    "#8000FF", "#FF0000", "#39FF14"
]
paddle_color = "white"
ball_color = "white"

# Game state variables
bricks = []
paddle = None
ball = None
ball_x_direction = 1
ball_y_direction = -1
score = 0
lives = 3
paused = False

# Create main tkinter window
window = tk.Tk()
window.title("Brick Breaker")
window.resizable(False, False)

# Create start frame
start = tk.Frame(window, width=612, height=480, bg="black")
start.place(x=0, y=0, relwidth=1, relheight=1)

# Declare the background image using its path
image_bg_path = "night.png"
image_bg = Image.open(image_bg_path)
image_bg = image_bg.resize((612, 480))
image_tk_bg = ImageTk.PhotoImage(image_bg)

# Create the label to display the background image
image_label = tk.Label(start, image=image_tk_bg)
image_label.place(x=0, y=0, relwidth=1, relheight=1)

# Display the title of the game
start_text = tk.Label(
    start,
    text="B R I C K    B R E A K E R",
    font=("ArcadeClassic", 25),
    fg="white",
    bg="black"
)
start_text.place(relx=0.5, rely=0.2, anchor="center")

# Frames for settings and difficulty screens
show_diff = tk.Frame(window, width=612, height=480, bg="black")
show_diff.place(x=0, y=0, relwidth=1, relheight=1)

show_settings = tk.Frame(window, width=612, height=480, bg="black")
show_settings.place(x=0, y=0, relwidth=1, relheight=1)

# Load the background image for the settings and difficulty frames
image_label = tk.Label(show_settings, image=image_tk_bg)
image_label.place(x=0, y=0, relwidth=1, relheight=1)

image_label = tk.Label(show_diff, image=image_tk_bg)
image_label.place(x=0, y=0, relwidth=1, relheight=1)

# Work frame for boss key
work_frame = tk.Frame(window)

# Loading background image for the work frame
image_work_path = "fake_excel.png"
image_work = Image.open(image_work_path)
image_work = image_work.resize((612, 480))
image_tk_work = ImageTk.PhotoImage(image_work)

# Create label with image in the work frame
work_label = tk.Label(work_frame, image=image_tk_work)
work_label.place(x=0, y=0, relwidth=1, relheight=1)

# Main game canvas
canvas = tk.Canvas(window, width=width, height=height)
canvas.pack()

# Set background image on the game canvas
bg = tk.PhotoImage(file="night.png")
canvas.create_image(0, 0, anchor="nw", image=bg)

# Difficulty label and options
diff_lbl = tk.Label(
    show_diff,
    text="Please    Select   Difficulty: ",
    font=("ArcadeClassic", 20),
    fg="white",
    bg="black"
)
diff_lbl.pack()

diff_opt = ["Easy", "Medium", "Hard"]  # Available difficulty options
diff = tk.StringVar(show_diff)  # Variable to hold the selected difficulty
diff.set(None)

diff_frame = tk.Frame(show_diff, bg="black")
diff_frame.pack()

def save_keys():
    """
    Save user-defined key bindings and give confirmation that they are saved.

    Retrieve the key-bindings inputted by the user, using the entry widgets in the settings frame, and update global variables to store them.
    """
    global left_key, right_key, pause_key, save_key, load_key, show_settings
    left_key = left_key_entry.get()
    right_key = right_key_entry.get()
    pause_key = pause_key_entry.get()
    save_key = save_key_entry.get()
    load_key = load_key_entry.get()

    # Show confirmation message after saving keys
    confirm_message = tk.Label(
        show_settings,
        text="Keys saved!",
        font=("ArcadeClassic", 12),
        fg="white",
        bg="black"
    )
    confirm_message.pack(pady=5)
    show_settings.lift()

def open_settings():
    """
    Open the settings frame and hide all other frames.

    Hide start and show_diff frames making only the show_settings frame visible with its widgets.
    """
    global start, show_diff, show_settings
    start.place_forget()
    show_diff.place_forget()
    show_settings.place(x=0, y=0, relwidth=1, relheight=1)
    show_settings.lift()

    # Ensure that all widgets in settings are on top
    for widget in show_settings.winfo_children():
        widget.lift()
    image_label.lower()

def show_diff_screen():
    """
    Open the difficulty selection frame and discard all other frames.

    Hide start and show_settings frames making only the difficulty selection frame(show_diff) visible.
    Implement the necessary widgets in the difficulty selection frame.
    """
    global start, show_settings, show_diff, diff_frame
    start.place_forget()
    show_settings.place_forget()
    show_diff.place(x=0, y=0, relwidth=1, relheight=1)
    show_diff.lift()
    diff_lbl.place(relx=0.5, rely=0.1, anchor="center")
    diff_frame.place(relx=0.5, rely=0.4, anchor="center")
    confirm_btn.place(relx=0.5, rely=0.7, anchor="center")

    # Ensure that all widgets in difficulty screen are on top
    for widget in show_diff.winfo_children():
        widget.lift()
    image_label.lower()

# Key binding inputs and entry widgets
left_key_label = tk.Label(
    show_settings,
    text="Move Left: ",
    font=("ArcadeClassic", 15),
    fg="white",
    bg="black"
)
left_key_label.place(relx=0.2, rely=0.1, anchor="center")

left_key_entry = tk.Entry(show_settings, font=("ArcadeClassic", 15))
left_key_entry.insert(0, "left")
left_key_entry.place(relx=0.8, rely=0.1, relwidth=0.3, anchor="center")

right_key_label = tk.Label(
    show_settings,
    text="Move Right: ",
    font=("ArcadeClassic", 15),
    fg="white",
    bg="black"
)
right_key_label.place(relx=0.2, rely=0.2, anchor="center")

right_key_entry = tk.Entry(show_settings, font=("ArcadeClassic", 15))
right_key_entry.insert(0, "right")
right_key_entry.place(relx=0.8, rely=0.2, relwidth=0.3, anchor="center")

pause_key_label = tk.Label(
    show_settings,
    text="Pause/Start Game: ",
    font=("ArcadeClassic", 15),
    fg="white",
    bg="black"
)
pause_key_label.place(relx=0.2, rely=0.3, anchor="center")

pause_key_entry = tk.Entry(show_settings, font=("ArcadeClassic", 15))
pause_key_entry.insert(0, "space")
pause_key_entry.place(relx=0.8, rely=0.3, relwidth=0.3, anchor="center")

save_key_label = tk.Label(
    show_settings,
    text="Save Game: ",
    font=("ArcadeClassic", 15),
    fg="white",
    bg="black"
)
save_key_label.place(relx=0.2, rely=0.4, anchor="center")

save_key_entry = tk.Entry(show_settings, font=("ArcadeClassic", 15))
save_key_entry.insert(0, "s")
save_key_entry.place(relx=0.8, rely=0.4, relwidth=0.3, anchor="center")

load_key_label = tk.Label(
    show_settings,
    text="Load Game: ",
    font=("ArcadeClassic", 15),
    fg="white",
    bg="black"
)
load_key_label.place(relx=0.2, rely=0.5, anchor="center")

load_key_entry = tk.Entry(show_settings, font=("ArcadeClassic", 15))
load_key_entry.insert(0, "l")
load_key_entry.place(relx=0.8, rely=0.5, relwidth=0.3, anchor="center")

# Confirm button to save key mappings
confirm_keys_button = tk.Button(
    show_settings,
    text="Confirm  Keys",
    font=("ArcadeClassic", 20),
    bg="black",
    fg="white",
    command=lambda: save_keys()
)
confirm_keys_button.place(relx=0.5, rely=0.7, anchor="center")

left_key = "Left"
right_key = "Right"
pause_key = "space"
save_key = "s"
load_key = "l"

def go_back_to_start():
    """
    Go back to the start frame using the back button in the settings frame.

    Hide show_settings and show_diff frames making only the start frame which is necessary when returning from the settings frame so that the game is playable.
    """
    global start, show_diff, show_settings
    show_settings.place_forget()  # Hide settings frame
    show_diff.place_forget()  # Hide difficulty selection frame
    start.place(x=0, y=0, relwidth=1, relheight=1)
    start.lift()

    # Ensure that all widgets in difficulty screen are on top
    for widget in start.winfo_children():
        widget.lift()

    start_button.config(state=tk.NORMAL)
    settings_button.config(state=tk.NORMAL)
    image_label.lower()

# Button to go back to the start frame
back_button = tk.Button(
    show_settings,
    text="Back",
    font=("ArcadeClassic", 20),
    command=go_back_to_start,
    fg="white",
    bg="black"
)
back_button.place(relx=0.5, rely=0.9, anchor="center")

def show_lvl():
    """
    Open the level selection frame and place all related widgets.

    If the difficulty frame is visible, forget it and its widgets.
    Then, place all the necessary widgets for the level selection frame.
    """
    global diff_frame, show_diff, level_frame
    if diff_frame.winfo_ismapped():  # If the difficulty selection frame is visible
        diff_frame.place_forget()  # Hide difficulty selection frame
        diff_lbl.place_forget()
        confirm_btn.place_forget()

        level_lbl.place(relx=0.5, rely=0.1, anchor="center")
        level_frame.place(relx=0.5, rely=0.4, anchor="center")
        play_btn.place(relx=0.5, rely=0.7, anchor="center")

        # Ensure that all widgets in difficulty screen are on top
        for widget in show_diff.winfo_children():
            widget.lift()
        image_label.lower()

def play():
    """
    Discard all frames before starting the game.

    Hide start and show_diff frames to make the window ready to display the canvas on which the game will be ran.
    """
    global start, show_diff
    start.place_forget()  # Hide start frame
    show_diff.place_forget()  # Hide difficulty selection frame
    start_game()

def pause(event):
    """
    Toggle the pause state of the game.

    Switches paused states based on player input with the pause key.
    
    Parameters: 
        event: The event object triggering this function(key-press)
    """
    global paused
    paused = not paused  # Changed paused state
    if paused:
        canvas.create_text(
            width // 2,
            height // 2,
            text="Paused",
            font=("ArcadeClassic", 30),
            fill="white",
            tag="paused"
        )  # Create paused text
    else:
        canvas.delete("paused")
        move_ball()  # Keep playing the game again

# Buttons on the start frame to start the game and access settings
start_button = tk.Radiobutton(
    start,
    text="Start Game",
    font=("ArcadeClassic", 20),
    value=1,
    variable=tk.StringVar(),
    command=show_diff_screen,
    fg="white",
    bg="black",
    selectcolor="black",
    width=15,
    height=2,
    indicatoron=0
)
start_button.place(relx=0.5, rely=0.4, anchor="center")

settings_button = tk.Radiobutton(
    start,
    text="Settings",
    font=("ArcadeClassic", 20),
    value=1,
    variable=tk.StringVar(),
    command=open_settings,
    fg="white",
    bg="black",
    selectcolor="black",
    width=15,
    height=2,
    indicatoron=0
)
settings_button.place(relx=0.5, rely=0.6, anchor="center")

# Radiobuttons for available difficulty options
for option in diff_opt:
    tk.Radiobutton(
        diff_frame,
        text=option,
        variable=diff,
        value=option,
        font=("ArcadeClassic", 25),
        fg="white",
        bg="black",
 selectcolor="gray",
        width=10,
        height=2,
        borderwidth=2,
        indicatoron=0
    ).pack(side="left", padx=5)

level_lbl = tk.Label(
    show_diff,
    text="Please   Select   Level",
    font=("ArcadeClassic", 20),
    fg="white",
    bg="black"
)

level_opt = ["Level-1", "Level-2", "Level-3"]  # Available level options
level = tk.StringVar(show_diff)  # Variable to hold selected level
level.set(level_opt[0])  # Set default level to level 1

# Create level frame and set background
level_frame = tk.Frame(show_diff, bg="black")

image_label = tk.Label(level_frame, image=image_tk_bg)
image_label.place(x=0, y=0, relwidth=1, relheight=1)

# Radiobuttons for available level options
for option in level_opt:
    tk.Radiobutton(
        level_frame,
        text=option,
        variable=level,
        value=option,
        font=("ArcadeClassic", 25),
        fg="white",
        bg="black",
        selectcolor="gray",
        width=10,
        height=2,
        borderwidth=2,
        indicatoron=0
    ).pack(side="left", pady=5)

def start_game():
    """
    Create the game canvas and start the game according to selected difficulty and level.

    Based on the selected difficulty by the player change the global variables ball_speed and paddle_width to implement static difficulty.
    Hide show_diff, show_settings and start frames and delete all widgets to display the game canvas.
    Based on the selected level use the three separate generate_bricks functions to create the predefined shape for the level.
    """
    global ball_speed, brick_rows, brick_cols, paddle_width, start, show_diff, show_settings, canvas, background

    sel_diff = diff.get()  # Get player selected difficulty
    sel_lvl = level.get()  # Get player selected level

    if sel_diff == "Easy":
        ball_speed = 3  # Slow ball
        paddle_width = 100  # Wide paddle
    elif sel_diff == "Medium":
        ball_speed = 4  # Medium speed ball
        paddle_width = 80  # Medium width paddle
    else:
        ball_speed = 5  # Fast ball
        paddle_width = 60  # Narrow paddle

    canvas.delete("all")
    show_diff.place_forget()
    show_settings.place_forget()
    start.place_forget()
    show_diff.lift()

    # Create labels to keep track of score and lives
    global score_lbl, lives_lbl
    score_lbl = canvas.create_text(
        10, 10, text=f"Score: {score}", fill="white", font=("ArcadeClassic", 20), anchor="nw"
    )
    lives_lbl = canvas.create_text(
        width - 10, 10, text=f"Lives: {lives}", fill="white", font=("ArcadeClassic", 20), anchor="ne"
    )

    if sel_lvl == "Level-1":
        background_image = tk.PhotoImage(file="level1_bg.png")
        create_bricks_lvl1()  # Create pre-defined shape for level 1
        create_paddle()
        create_ball()
        move_ball()
    elif sel_lvl == "Level-2":
        background_image = tk.PhotoImage(file="level2_bg.png")
        create_bricks_lvl2()  # Create pre-defined shape for level 2
        create_paddle()
        create_ball()
        move_ball()
    else:
        background_image = tk.PhotoImage(file="level3_bg.png")
        create_bricks_lvl3()  # Create pre-defined shape for level 3
        create_paddle()
        create_ball()
        move_ball()

    # Set background images for levels
    background_tag = "background"
    background = canvas.create_image(0, 0, image=background_image, anchor="nw", tag=background_tag)
    canvas.image = background_image
    canvas.tag_lower(background_tag)
    canvas.pack(fill="both", expand=True)

# Buttons for the select difficulty frame
play_btn = tk.Button(
    show_diff,
    text="PLAY",
    font=("ArcadeClassic", 20),
    bg="black",
    fg="white",
    command=play
)
confirm_btn = tk.Button(
    show_diff,
    text="CONFIRM",
    font=("ArcadeClassic", 20),
    bg="black",
    fg="white",
    command=show_lvl
)
confirm_btn.pack(pady=5)

# Difficulty selection frame background image
show_diff_bg = tk.PhotoImage(file="night.png")
show_diff.configure(bg='black')

def load_highscores(level):
    """
    Open the leaderboard file of the selected level and load top five scores from all saved scores.

    Based on the selected level open the related leaderboard text file and load the top five scores from the file.

    Parameters:
        level: the player-selected level on the level selection screen, one of Level-1/Level-2/Level-3.

    Returns:
        list: return the top five scores from the leaderboard text file as a list.
    """
    filename = f"highscores_{level}.txt"  # Open the file based on the level
    with open(filename, "r") as file:  # Open the file in reading mode
        scores = []
        for line in file:
            name, score = line.strip().split(", ")  # Get names and scores separately
            scores.append((name, int(score)))

        # Use bubble sort
        for i in range(len(scores)):
            for j in range(len(scores) - i - 1):
                if scores[j][1] < scores[j + 1][1]:
                    scores[j], scores[j + 1] = scores[j + 1], scores[j]
        return scores[:5]  # Return top 5 scores in the files

def save_highscores(level, name, score):
    """
    Open the leaderboard file of the selected level and store the score if it is bigger than the smallest value in the file.

    Using the load_highscores method add all the highscores to a list.
    Implement bubble-sort to see if the player score is higher than the smallest entry on that list.
    If so, the entry is added to the list and displayed as one of the top five highscores.

    Parameters:
        level: the player-selected level on the level selection screen.
        name:  the player-input of the players initials as the name for the leaderboard.
        score: the final score of the player.
    """
    scores = load_highscores(level)
    scores.append((name, score))

    # Compare scores to determine if it's going to be added
    for i in range(len(scores)):
        for j in range(len(scores) - i - 1):
            if scores[j][1] < scores[j + 1][1]:
                scores[j], scores[j + 1] = scores[j + 1], scores[j]
    scores = scores[:5]  # Return top 5 scores

    filename = f"highscores_{level}.txt"
    with open(filename, "w") as file:  # Open file in write mode
        for player, score in scores:
            file.write(f"{player}, {score}\n")

def leaderboard_entry(score):
    """
    Create the entry frame and its related widgets.

    Get the selected level value from the player and create the entry frame.
    Add all necessary widgets and background image.

    Parameter:
        score: the final score of the player.
    """
    global level, entry_frame, start
    level_name = level.get()  # Get user selected level

    # Create entry frame, set background and images
    entry_frame = tk.Frame(window)
    entry_frame.place(x=0, y=0, relwidth=1, relheight=1)

    image_bg_path = "night.png"
    image_bg = Image.open(image_bg_path)
    image_bg = image_bg.resize((612, 480))
    global image_tk_bg
    image_tk_bg = ImageTk.PhotoImage(image_bg)

    image_label = tk.Label(entry_frame, image=image_tk_bg)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)

    prompt_label = tk.Label(
        entry_frame,
        text=f"GAME  OVER\nYOUR  SCORE: {score}\nENTER   YOUR   INITIALS (2   LETTERS): ",
        font=("ArcadeClassic", 20),
        fg="white",
        bg="black"
    )
    prompt_label.pack(side="top", padx=5, pady=10)

    name_entry = tk.Entry(entry_frame, font=("ArcadeClassic", 20))
    name_entry.pack(side="top", pady=60, padx=10)

    def submit_name():
        """
        Ask user for their initials as entries for the leaderboard frame.

        Get player entry using the entry widget on the entry frame.
        If the length of the player entry is two characters save the highscore.
        If not ask for player for entry on the entry frame again.
        """
        global entry_frame
        name = name_entry.get()  # Get player name entry
        if len(name) == 2:  # Check length of entry
            save_highscores(level_name, name.upper(), score)
            show_leaderboard(level_name)
        else:
            prompt_label.config(text="INVALID   NAME!\nENTER   TWO   LETTERS   AS   INITALS")  # Ask for entry again
            name_entry.delete(0, tk.END)  # Delete the text in the entry widget

    # Button to submit name entry
    submit_button = tk.Button(
        entry_frame,
        text="SUBMIT",
        font=("ArcadeClassic", 20),
        bg="black",
        fg="white",
        command=submit_name
    )
    submit_button.pack(side="top", pady=50)

def show_leaderboard(level_name):
    """
    Create the leaderboard frame and display the top five scores stored in the leaderboard file of the respective level.

    Create the frame and add all necessary widgets and the background image.
    Using the load_highscores function, get the values to display on the frame.

    Parameters:
        level_name: the player-selected level on the level selection screen, one of Level-1/Level-2/Level-3.
    """
    global leaderboard_frame, start

    # Create leaderboard frame, set widgets and background
    leaderboard_frame = tk.Frame(window, bg="black")
    leaderboard_frame.place(x=0, y=0, relwidth=1, relheight=1)

    image_bg_path = "night.png"
    image_bg = Image.open(image_bg_path)
    image_bg = image_bg.resize((612, 480))
    global image_tk_bg
    image_tk_bg = ImageTk.PhotoImage(image_bg)

    image_label = tk.Label(leaderboard_frame, image=image_tk_bg)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)

    leaderboard_label = tk.Label(
        leaderboard_frame,
        text="LEADERBOARD",
        font=("ArcadeClassic", 30),
        fg="white",
        bg="black"
    )
    leaderboard_label.pack(pady=20)

    high_scores = load_highscores(level_name)  # Get the scores to display
    for name, score in high_scores:
        tk.Label(
            leaderboard_frame,
            text=f"{name}: {score}",
            font=("ArcadeClassic", 20),
            fg="white",
            bg="black"
        ).pack(pady=5)

    # Menu button to go back to the start frame
    menu_button = tk.Button(
        leaderboard_frame,
        text="MENU",
        font=("ArcadeClassic", 20),
        bg="black",
        fg="white",
        command=lambda: back_to_start()
    )
    menu_button.pack(pady=20)

def back_to_start(event=None):
    """
    Return back to the start frame from the leaderboard frame using the menu button.

    Hide every frame other than the start frame.
    Change global game state variables to default values to ensure game replayability.
    Show the start frame as the only visible frame and reload background images.

    Parameters:
        event: the event object that triggers the function(menu button press)
    """
    global start, leaderboard_frame, entry_frame, show_diff, show_settings, bricks, paddle, ball, ball_x_direction, ball_y_direction, score, lives, paused, image_label, bg, image_tk_bg

    # Forget all frames other than start
    leaderboard_frame.place_forget()
    entry_frame.place_forget()
    level_frame.place_forget()
    level_lbl.place_forget()
    show_diff.place_forget()
    show_settings.place_forget()

    # Reset game variables
    bricks = []
    paddle = None
    ball = None
    ball_x_direction = 1
    ball_y_direction = -1
    score = 0
    lives = 3
    paused = False

    start.place(x=0, y=0, relwidth=1, relheight=1)
    start.lift()

    # Ensure no overlap
    reload_background_images()

    # Bind keys and buttons again for replayability
    window.bind("<KeyPress>", keyboard_binding)
    start_button.config(state=tk.NORMAL)
    settings_button.config(state=tk.NORMAL)

def reload_background_images():
    """
    Reload background images to ensure visibility when the game is replayed and to remove any widget overlaps.

    Create the background image again and keep a reference for garbage collection.
    Based on displayed frames and widgets ensure that there are no widget or frame overlaps and the game is replayable.
    """
    global image_tk_bg, bg

    # Set background image
    image_bg = Image.open("night.png")
    image_bg = image_bg.resize((612, 480))
    image_tk_bg = ImageTk.PhotoImage(image_bg)

    # If a frame has a label which is an image configure it
    for widget in start.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("image"):
            widget.configure(image=image_tk_bg)
            widget.image = image_tk_bg

    for widget in show_diff.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("image"):
            widget.configure(image=image_tk_bg)
            widget.image = image_tk_bg

    for widget in show_settings.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("image"):
            widget.configure(image=image_tk_bg)
            widget.image = image_tk_bg

    for widget in level_frame.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("image"):
            widget.configure(image=image_tk_bg)
            widget.image = image_tk_bg

    for frame in [start, show_diff, show_settings, level_frame]:
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("image"):
                widget.lower()

def save_game():
    """
    Save the state of game in a save text file.

    Save the necessary states of the game to create it when loaded back, such as: paddle position, ball position, brick positions, brick colors, score, lives and brick existence.
    """
    global score, lives, paddle, bricks, ball

    # Save paddle and ball positions
    paddle_pos = canvas.coords(paddle)
    ball_pos = canvas.coords(ball)

    # Save brick existence, positions, colors
    brick_states = []
    brick_positions = []
    brick_colors = []
    for brick in bricks:
        brick_coords = canvas.coords(brick)
        if canvas.itemcget(brick, "state") != "hidden":
            brick_states.append(1)
            brick_positions.append(brick_coords)
            brick_colors.append(canvas.itemcget(brick, "fill"))
        else:
            brick_states.append(0)

    # Write everything that is saved to a text file
    with open("save_game.txt", "w") as file:
        file.write(f"{score}\n")
        file.write(f"{lives}\n")
        file.write(f"{paddle_pos[0]},{paddle_pos[1]},{paddle_pos[2]},{paddle_pos[3]}\n")
        file.write(f"{ball_pos[0]},{ball_pos[1]},{ball_pos[2]},{ball_pos[3]}\n")
        file.write(",".join(map(str, brick_states)) + "\n")
        for pos in brick_positions:
            file.write(",".join(map(str, pos)) + "\n")
        for color in brick_colors:
            file.write(f"{color}\n")

def load_game():
    """
    Load the game accordingly reading from the saved game state in the save text file.

    Read from the text file the values of score and lives labels.
    Determine which bricks exist and their position and colors.
    Load the game based on the saved states.
    """
    global score, lives, paddle, bricks, ball, paddle_pos, ball_pos, brick_colors

    # Load game state variables
    with open("save_game.txt", "r") as file:
        score = int(file.readline().strip())
        lives = int(file.readline().strip())
        paddle_pos = list(map(float, file.readline().strip().split(",")))
        ball_pos = list(map(float, file.readline().strip().split(",")))
        brick_states = list(map(int, file.readline().strip().split(",")))

        # Load bricks
        num_visible_bricks = sum(brick_states)
        brick_positions = [list(map(float, file.readline().strip().split(","))) for _ in range(num_visible_bricks)]
        brick_colors = [file.readline().strip() for _ in range(num_visible_bricks)]

        # Load positions
        canvas.coords(paddle, paddle_pos[0], paddle_pos[1], paddle_pos[2], paddle_pos[3])
        canvas.coords(ball, ball_pos[0], ball_pos[1], ball_pos[2], ball_pos[3])

        # If the brick has been broken before a load recreate it
        visible_index = 0
        for index, state in enumerate(brick_states):
            if state == 1:
                x1, y1, x2, y2 = brick_positions[visible_index]
                color = brick_colors[visible_index]
                if index < len(bricks):
                    canvas.coords(bricks[index], x1, y1, x2, y2)
                    canvas.itemconfig(bricks[index], fill=color, state="normal")
                else:
                    brick = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                    bricks.append(brick)
                visible_index += 1
            else:
                if index < len(bricks):
                    canvas.itemconfig(bricks[index], state="hidden")

        # Configure score and lives labels
        canvas.itemconfig(score_lbl, text=f"Score: {score}")
        canvas.itemconfig(lives_lbl, text=f"Lives: {lives}")
        game_over()

buffer = ""  # Buffer to save sequence of characters
buffer_max = 10  # Max length of buffer

def increase_ball():
    """Increase the size of the ball by a defined ratio when the cheat code is entered."""
    global ball

    # Coordinates of ball
    current = canvas.coords(ball)
    x1, y1, x2, y2 = current

    increase = 30  # Increase ratio

    new_x1 = x1 - increase / 2
    new_y1 = y1 - increase / 2
    new_x2 = x2 + increase / 2
    new_y2 = y2 + increase / 2

    # Set new coordinates
    canvas.coords(ball, new_x1, new_y1, new_x2, new_y2)

def increase_paddle():
    """Increase the width of the paddle by a defined amount when the cheat code is entered."""
    global paddle

    # Coordinates of paddle
    current = canvas.coords(paddle)
    x1, y1, x2, y2 = current

    increase = 200  # Increase ratio

    new_x2 = x2 + increase

    # Set new coordinates
    canvas.coords(paddle, x1, y1, new_x2, y2)

def win():
    """Determine if there are any bricks remaining on the screen."""
    if len(bricks) == 0:  # Check number of bricks left
        game_over()

def create_bricks_lvl1():
    """
    Create the bricks for level 1 following a predefined shape.

    Following a predefined shape colors are picked randomly using the random library method, shuffle.
    The color selection is implemented before iterating over the columns to make sure each row has the same color.
    """
    global bricks
    bricks = []

    # Shuffle colors to randomize order
    random.shuffle(brick_colors)
    color_index = 0
    for row in range(brick_rows):

        # Pick a random color for the row
        color = brick_colors[color_index]
        color_index += 1
        if color_index == len(brick_colors):
            random.shuffle(brick_colors)
            color_index = 0
        for col in range(brick_cols):

            # Create bricks in a pre-defined shape
            if (row + col) % 2 == 0:
                x = col * brick_width + 20
                y = row * brick_height + 50
                brick = canvas.create_rectangle(
                    x, y, x + brick_width, y + brick_height, fill=color, outline="gray"
                )
                bricks.append(brick)

def create_bricks_lvl2():
    """
    Create the bricks for level 2 following a predefined shape.

    Following a predefined shape colors are picked randomly using the random library method, shuffle.
    The color selection is implemented before iterating over the columns to make sure each row has the same color.
    """
    global bricks
    bricks = []

    # Shuffle colors to randomize order
    random.shuffle(brick_colors)
    color_index = 0
    for row in range(brick_rows):

        # Pick a random color for the row
        color = brick_colors[color_index]
        color_index += 1
        if color_index == len(brick_colors):
            random.shuffle(brick_colors)
            color_index = 0

        # Create bricks in a pre-defined shape    
        for col in range(brick_cols // 2 - abs(brick_rows // 2 - row), brick_cols // 2 + abs(brick_rows // 2 - row) + 1):
            x = col * brick_width + 20
            y = row * brick_height + 50
            brick = canvas.create_rectangle(
                x, y, x + brick_width, y + brick_height, fill=color, outline="gray"
            )
            bricks.append(brick)

def create_bricks_lvl3():
    """
    Create the bricks for level 3 following a predefined shape.

    Following a predefined shape colors are picked randomly using the random library method, shuffle.
    The color selection is implemented before iterating over the columns to make sure each row has the same color.
    """
    global bricks
    brick_rows = 11
    bricks = []

    # Shuffle colors to randomize order
    random.shuffle(brick_colors)
    color_index = 0
    for row in range(brick_rows):

        # Pick a random color for the row
        color = brick_colors[color_index]
        color_index += 1
        if color_index == len(brick_colors):
            random.shuffle(brick_colors)
            color_index = 0
        for col in range(brick_cols):

            # Create bricks in a pre-defined shape
            if row == col or row + col == brick_cols - 1:
                x = col * brick_width + 20
                y = row * brick_height + 50
                brick = canvas.create_rectangle(
                    x, y, x + brick_width, y + brick_height, fill=color, outline="gray"
                )
                bricks.append(brick)

def create_paddle():
    """Create the paddle for the ball to bounce off."""
    global paddle
    paddle = canvas.create_rectangle(
        width / 2 - paddle_width / 2,
        height - paddle_height - 20,
        width / 2 + paddle_width / 2,
        height - 20,
        fill=paddle_color,
        outline="white"
    )  # Create paddle

def create_ball():
    """Create the ball."""
    global ball
    paddle_pos = canvas.coords(paddle)  # Get paddle coordinates
    ball = canvas.create_oval(
        paddle_pos[0] + (paddle_pos[2] - paddle_pos[0]) / 2 - ball_size / 2,
        height - paddle_height - ball_size - 20,
        paddle_pos[0] + (paddle_pos[2] - paddle_pos[0]) / 2 + ball_size / 2,
        height - paddle_height - 20,
        fill=ball_color,
        outline="white"
    )  # Create ball

def respawn():
    """Delete the old ball when it goes below the paddle."""
    global ball, ball_x_direction, ball_y_direction
    canvas.delete(ball)  # Delete ball

    def new_ball():
        """Create a new ball when the old one is destroyed due to bouncing below the paddle and causing the player to lose a life."""
        global ball, ball_x_direction, ball_y_direction
        paddle_pos = canvas.coords(paddle)  # Get paddle coordinates

        ball = canvas.create_oval(
            paddle_pos[0] + (paddle_pos[2] - paddle_pos[0]) / 2 - ball_size / 2,
            height - paddle_height - ball_size - 20,
            paddle_pos[0] + (paddle_pos[2] - paddle_pos[0]) / 2 + ball_size / 2,
            height - paddle_height - 20,
            fill=ball_color,
            outline="white"
        )  # Create new ball

        # Set ball directions
        ball_x_direction = 1
        ball_y_direction = -1

        move_ball()

    window.after(1000, new_ball)  # Wait some time to spawn in the ball

def update_score():
    """Update the score and lives labels."""
    global score
    canvas.itemconfig(score_lbl, text=f"Score: {score}")  # Update score
    canvas.itemconfig(lives_lbl, text=f"Lives: {lives}")  # Update lives

def move_bricks_down():
    """Move each brick down one row when a life is lost making the game harder to complete for the player."""
    global bricks
    brick_height_increment = brick_height  

    for brick in bricks:
        # Get brick coordinates
        x1, y1, x2, y2 = canvas.coords(brick)

        new_y1 = y1 + brick_height_increment
        new_y2 = y2 + brick_height_increment

        # Move down one row
        if new_y2 >= height - paddle_height - 20:
            canvas.delete(brick)
            bricks.remove(brick)
        else:
            canvas.coords(brick, x1, new_y1, x2, new_y2)  # Set new coordinates

def move_ball():
    """
    Move the ball at a predefined speed, calculate and implement collision mechanics based on its coordinates.

    Check if the game is in a paused state and if it is return.
    Else based on the created ball's coordinates implement collision mechanics and checks with other game objects.
    If the ball collides with the paddle or side and top walls it bounces reversing the direction it came in.
    Colliding with the bricks causes the bricks to break and score to be incremented by one.
    If the ball falls under the paddle it disappears causing the player to lose a life.
    """
    global ball_x_direction, ball_y_direction, score, lives, score_lbl, lives_lbl

    # If paused don't do anything
    if paused:
        return

    canvas.move(ball, ball_x_direction * ball_speed, ball_y_direction * ball_speed)
    ball_pos = canvas.coords(ball)  # Get ball coordinates

    # Check for collision with paddle
    if ball_pos[0] <= 0 or ball_pos[2] >= width:
        ball_x_direction *= -1
    if ball_pos[1] <= 0:
        ball_y_direction *= -1
    if ball_pos[3] >= height:
        lives -= 1  # Lose life when ball falls below paddle
        update_score()
        if lives == 0:  # When lives are equal to 0
            game_over()
            return
        move_bricks_down()
        respawn()
        return
    
    # Reverse y direction
    if ball_pos[3] >= height - paddle_height - 20 and ball_pos[0] >= canvas.coords(paddle)[0] and ball_pos[2] <= canvas.coords(paddle)[2]:
        ball_y_direction *= -1

    # Check collision with bricks
    for brick in bricks:  
        brick_coords = canvas.coords(brick)
        if (ball_pos[2] >= brick_coords[0] and ball_pos[0] <= brick_coords[2] and ball_pos[3] >= brick_coords[1] and ball_pos[1] <= brick_coords[3]):
            ball_y_direction *= -1
            score += 1  # Increase score if brick broken
            update_score()
            canvas.delete(brick)  
            bricks.remove(brick)  
            break 

    win()

    # Wait some time and move ball based on ball speed.
    if ball_speed == 3:
        window.after(50, move_ball)  
    elif ball_speed == 5:
        window.after(30, move_ball)  
    else:
        window.after(20, move_ball)

def game_over():
    """Determine if there are any bricks remaining on the game canvas. If not display the entry frame and final score."""
    visible_bricks = []
    for brick in bricks:
        if canvas.itemcget(brick, "state") == "normal":
            visible_bricks.append(brick)
    
    # Check if any bricks are left
    if len(visible_bricks) == 0 or lives == 0:  
        global score
        canvas.delete(ball)  # Delete ball
        window.unbind("<KeyPress>")  # Disable movement
        canvas.itemconfig(score_lbl, text=f"GAME OVER! FINAL SCORE: {score}")  # Display the final score
        leaderboard_entry(score)  # Show entry frame

was_paused = False  # Variable to track paused state

def keyboard_binding(event):
    """
    Bind the user selected keys to game movement mechanics. Bind cheat codes to their respective methods.

    Bind cheat codes by checking if the string stored in the buffer matches the cheat codes.
    Bind other player-inputted keybindings to game and player actions.

    Parameters:
        event: an event object that triggers the function(key-press)
    """
    global paused, buffer, ball, paddle, was_paused
    buffer += event.char.upper()  # Add the uppercase version of the character to buffer

    if "ABAB" in buffer:  # Cheat code
        increase_ball()
        buffer = ""  # Reset buffer
    elif "BABA" in buffer:  # Cheat code
        increase_paddle()
        buffer = ""  # Reset buffer

    paddle_pos = canvas.coords(paddle)  # Get paddle coordinates

    # Bind keys based on user input and pause state
    if event.keysym == left_key and paddle_pos[0] > 0 and not paused:
        canvas.move(paddle, -20, 0)  
    elif event.keysym == right_key and paddle_pos[2] < width and not paused:
        canvas.move(paddle, 20, 0)
    elif event.keysym == pause_key:
        if paused:
            paused = False
            canvas.delete("paused")
            move_ball()
        else:
            paused = True
            canvas.create_text(width // 2, height // 2, text="PAUSED", font=("ArcadeClassic", 30), fill="white", tag="paused")
    elif event.keysym == save_key:
        save_game()
    elif event.keysym == load_key:
        load_game()
    elif event.keysym == "e":
        was_paused = paused
        paused = True
        canvas.pack_forget()
        work_frame.place(x=0, y=0, relheight=1, relwidth=1)
    elif event.keysym == "r":
        canvas.pack()
        work_frame.place_forget()
        if was_paused:
            paused = True  
            canvas.create_text(width // 2, height // 2, text="PAUSED", font=("ArcadeClassic", 30), fill="white", tag ="paused")
        else:
            paused = False 
            move_ball()

window.bind("<KeyPress>", keyboard_binding)  # Bind the keys
start.lift()  # Place to start frame on top
window.mainloop()  # Run the main window
