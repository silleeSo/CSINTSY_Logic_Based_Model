import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageSequence
import sys
import os
from functools import partial
import json
import janus_swi as janus

#prolog = Prolog()
janus.consult("prolog_advice.pl")
#read dictionary for more detailed results
with open('results_dictionary.json', 'r') as file:
    data = json.load(file)
class StdRedirector(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, message):
        pass  # Suppress the message

    def flush(self):
        pass  # Do nothing
    
sys.stderr = StdRedirector(sys.stderr)

# Initialize the main window
root = tk.Tk()
root.title("Ms. Cupid")
root.geometry("1920x1080")

# Determine the directory where the Python script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load and display the background image 
image_path = os.path.join(script_dir, "Assets", "Background", "start_background_photo.png")
background_image = Image.open(image_path)
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load the GIF
gif_path = os.path.join(script_dir,"Assets", "Buttons", "start_button.gif")
gif_image = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame.copy().convert('RGBA')) for frame in ImageSequence.Iterator(gif_image)]

# Function to keep track of the current page
page_counter = 0


# Inputs for prolog
input_selected_mbti = None
input_love_language = None
input_ranked_values = []
input_selected_interests = []

#PROLOG Query Funtions
def get_pl_attachment_style(mbti):
    query = f"recommended_attachment_style({mbti}, Style)."
    result = list(janus.query(query))
    if result:
        style = result[0]['Style']
        return style
    else:
        return "No attachment style found."
    
def get_pl_communication_style(mbti):
    query = f"recommended_communication_style({mbti}, Style)."
    result = list(janus.query(query))
    if result:
        style = result[0]['Style']
        return style
    else:
        return "No commmunication style found."
def get_pl_partner_match(mbti):
    query = f"recommended_partner({mbti}, Partner)."
    result = list(janus.query(query))
    if result:
        style = result[0]['Partner']
        return style
    else:
        return "No partner match found."
def get_pl_partner_love_language(loveLanguage):
    query = f"recommended_partner_love_language({loveLanguage.lower().replace(" ", "_")}, Language)."
    result = list(janus.query(query))
    if result:
        language = result[0]['Language']
        return language
    else:
        return "No love language found."
def get_partner_value(value):
    query = f"recommended_partner_value({value.lower().replace(" ", "_")}, PartnerValue)."
    result = list(janus.query(query))
    if result:
        partner_value = result[0]['PartnerValue']
        return partner_value
    else:
        return "No complement found."
def get_partner_interest(interest):
    query = f"recommended_partner_interest({interest.lower().replace(" ", "_")}, PartnerInterest)."
    result = list(janus.query(query))
    if result:
        partner_interest = result[0]['PartnerInterest']
        return partner_interest
    else:
        return "No complement found."
def get_pl_partner_values(values):
    complementingValues = []
    for value in values:
        print("Value: ", value)
        complementingValues.append(get_partner_value(value))
    return complementingValues

def get_pl_partner_interests(interests):
    complementingValues = []
    for interest in interests:
        print("Interest: ", interest)
        complementingValues.append(get_partner_interest(interest))
    return complementingValues

def show_pl_results(text):
    print("Value diplayed: ", text)
    bg_color = "#e188b4"
    label_font = tkfont.Font(family="Helvetica", size=45, weight="bold")
    advice_label = tk.Label(root, text="Advice will be shown here.", height= 120, width=15,bg=bg_color, font=label_font)
    advice_label.pack(pady=500, padx=20, anchor='center')
    advice_label.config(text=f"{text.upper().replace("_", " ")}")

def add_to_counter():
    global page_counter
    page_counter += 1
    print(f"Current Page: {page_counter}")

# Function to animate the GIF
def update_frame(frame_index):
    frame = frames[frame_index]
    start_button.config(image=frame)
    root.after(40, update_frame, (frame_index + 1) % len(frames))

# Function to open the gender selection screen
def open_gender_selection():
    # Clear the current widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Set the background color
    root.configure(bg='#FDA1FF')
    
    # Add new background
    global gender_background_photo  # Keep a reference to avoid garbage collection
    gender_image_path = os.path.join(script_dir, "Assets", "Background","gender_background_photo.png")
    gender_background_image = Image.open(gender_image_path)
    gender_background_photo = ImageTk.PhotoImage(gender_background_image)
    
    gender_background_label = tk.Label(root, image=gender_background_photo)
    gender_background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Load gender images
    global female_photo, male_photo  # Keep a reference to avoid garbage collection
    female_image_path = os.path.join(script_dir, "Assets", "Buttons","Female.png")
    male_image_path = os.path.join(script_dir, "Assets", "Buttons","Male.png")
    
    female_image = Image.open(female_image_path)
    male_image = Image.open(male_image_path)
    
    female_photo = ImageTk.PhotoImage(female_image)
    male_photo = ImageTk.PhotoImage(male_image)
    
    # Create buttons for gender selection
    female_button = tk.Button(root, image=female_photo,  background='#DD7FBA',  highlightthickness=0, activebackground="lightpink",command=mbti_selection)
    female_button.image = female_photo  # Keep a reference to avoid garbage collection
    male_button = tk.Button(root, image=male_photo, background='#DD7FBA',  highlightthickness=0, activebackground="lightblue",command=mbti_selection)
    male_button.image = male_photo  # Keep a reference to avoid garbage collection
    
    # Place buttons on the screen
    female_button.pack(side=tk.LEFT, padx=50)
    female_button.place(x=700, y=600, anchor=tk.CENTER)
    male_button.pack(side=tk.RIGHT, padx=50)
    male_button.place(x=1200, y=600, anchor=tk.CENTER)
    add_to_counter()

# Function to handle MBTI selection slideshow
def mbti_selection():
    # Clear the current widgets
    for widget in root.winfo_children():
        widget.destroy()

    # List of MBTI types and their images
    mbti_types = ["INFJ", "ENFJ", "INFP", "ENFP", "INTJ", "ENTJ", "INTP", "ENTP", 
                  "ISFJ", "ESFJ", "ISTJ", "ESTJ", "ISFP", "ESFP", "ISTP", "ESTP"]
    images = [Image.open(os.path.join(script_dir, "Assets", "MBTI",f"{mbti}.png")) for mbti in mbti_types]
    photos = [ImageTk.PhotoImage(img) for img in images]

    # Index to track current MBTI type
    current_index = [0]

    global mbti_background_photo  # Keep a reference to avoid garbage collection
    mbti_image_path = os.path.join(script_dir, "Assets", "Background","mbti_background_photo.png")
    mbti_background_image = Image.open(mbti_image_path)
    mbti_background_photo = ImageTk.PhotoImage(mbti_background_image)
    
    mbti_background_label = tk.Label(root, image=mbti_background_photo)
    mbti_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def update_mbti(index):
        mbti_label.config(image=photos[index])
        mbti_label.image = photos[index]
        global input_selected_mbti
        input_selected_mbti = mbti_types[index]  # Update the global variable

    # Function to show the next MBTI type
    def next_mbti():
        current_index[0] = (current_index[0] + 1) % len(mbti_types)
        update_mbti(current_index[0])

    # Function to show the previous MBTI type
    def previous_mbti():
        current_index[0] = (current_index[0] - 1) % len(mbti_types)
        update_mbti(current_index[0])

    # Create MBTI display widgets
    mbti_label = tk.Label(root,background='#E085B8')
    mbti_label.place(x=960, y=530, anchor=tk.CENTER)

    # Load button images
    global prev_photo,next_photo, proceed_photo  # Keep a reference to avoid garbage collection
    prev_image_path = os.path.join(script_dir,"Assets", "Buttons", "previous_button.png")
    next_image_path = os.path.join(script_dir,"Assets", "Buttons", "next_button.png")
    proceed_image_path = os.path.join(script_dir, "Assets", "Buttons","proceed_button.png")
    
    prev_image = Image.open(prev_image_path)
    next_image = Image.open(next_image_path)
    proceed_image = Image.open(proceed_image_path)
    
    prev_photo = ImageTk.PhotoImage(prev_image)
    next_photo = ImageTk.PhotoImage(next_image)
    proceed_photo = ImageTk.PhotoImage(proceed_image)

    # Create navigation buttons
    prev_button = tk.Button(root, image=prev_photo, background='#E898AE', activebackground="lightpink", command=previous_mbti)
    next_button = tk.Button(root, image=next_photo, background='#D772C4', activebackground="lightpink", command=next_mbti)
    proceed_button = tk.Button(root, image=proceed_photo,command=loading_screen, background='#DD7FBA',activebackground="lightpink", highlightthickness=5, bd=0)

    prev_button.place(x=600, y=600, anchor=tk.CENTER)
    next_button.place(x=1320, y=600, anchor=tk.CENTER)
    proceed_button.place(x=960, y=940, anchor=tk.CENTER)

    # Initialize with the first MBTI type
    update_mbti(current_index[0])
    add_to_counter()

def loading_screen():
    # Clear the current widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Load background photo
    global loading_background_photo, gif_frames, gif_index  # Keep a reference to avoid garbage collection
    loading_image_path = os.path.join(script_dir, "Assets", "Background", "loading_screen_bg.png")
    loading_background_image = Image.open(loading_image_path)
    loading_background_photo = ImageTk.PhotoImage(loading_background_image)

    loading_background_label = tk.Label(root, image=loading_background_photo)
    loading_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Load the animated GIF
    loading_gif_path = os.path.join(script_dir,"Assets", "Buttons", "loading.gif")
    gif = Image.open(loading_gif_path)
    gif_frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]
    gif_index = 0

    loading_gif_label = tk.Label(root, bg="#DD7FBA")
    loading_gif_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    # Add the label for loading text
    global loading_text_label, dots
    dots = 0
    loading_text_label = tk.Label(root, text="Preparing personalized advice", font=("Comic Sans MS", 30), bg="#DD7FBA")
    loading_text_label.place(relx=0.5, y=150, anchor=tk.CENTER)
    animate_dots()
    
    # Add the label for tips
    global tips, tip_label, tip_index
    tips = [
        "Communication is key to a healthy relationship. Make sure to talk openly with your partner.",
        "'The greatest happiness of life is the conviction that we are loved.' – Victor Hugo",
        "“The best thing to hold onto in life is each other.” – Audrey Hepburn",
        "“To fall in love with yourself is the first secret to happiness.” – Robert Morley"
    ]
    tip_index = 0
    tip_label = tk.Label(root, text=tips[tip_index], font=("Helvetica", 20), fg="#E61F93", bg="#FFFEF4", wraplength=600)
    tip_label.place(relx=0.5, y=855, anchor=tk.CENTER)
    update_tip()

    # Start GIF animation
    update_gif(loading_gif_label)

    # Schedule transition to next page after 10 seconds (10000 milliseconds)
    add_to_counter()
    #TO CHANGE LOADING TIME
    if page_counter < 5:
        root.after(10, attachment_style)
    else:
        root.after(10, result)

    
def attachment_style():
    # Clear the current widgets
    for widget in root.winfo_children():
        widget.destroy()

    global user_attachment_style_background_photo, proceed_button_photo  # Keep a reference to avoid garbage collection
    user_attachment_style_image_path = os.path.join(script_dir, "Assets", "Background","attachment_style_bg.png")
    proceed_button_image_path = os.path.join(script_dir, "Assets", "Buttons","proceed_button.png")

    user_attachment_style_background_image = Image.open(user_attachment_style_image_path)
    proceed_button_image = Image.open(proceed_button_image_path)

    user_attachment_style_background_photo = ImageTk.PhotoImage(user_attachment_style_background_image)
    proceed_button_photo = ImageTk.PhotoImage(proceed_button_image)

    user_attachment_style_background_label = tk.Label(root, image=user_attachment_style_background_photo)
    user_attachment_style_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    proceed_button = tk.Button(root, image=proceed_button_photo, command=communication_style, background='#DD7FBA', activebackground="lightpink", highlightthickness=5, bd=0)
    proceed_button.place(x=1200, y=750, anchor=tk.CENTER)
    add_to_counter()

    #query Prolog
    advice = get_pl_attachment_style(input_selected_mbti.lower())
    show_pl_results(advice)


def communication_style():
    # Clear the current widgets
    for widget in root.winfo_children():
        widget.destroy()

    global user_communication_style_background_photo, proceed_button_photo  # Keep a reference to avoid garbage collection
    user_communication_style_image_path = os.path.join(script_dir,"Assets", "Background", "communicaton_style_bg.png")
    proceed_button_image_path = os.path.join(script_dir,"Assets", "Buttons", "proceed_button.png")

    user_communication_style_background_image = Image.open(user_communication_style_image_path)
    proceed_button_image = Image.open(proceed_button_image_path)

    user_communication_style_background_photo = ImageTk.PhotoImage(user_communication_style_background_image)
    proceed_button_photo = ImageTk.PhotoImage(proceed_button_image)

    user_communication_style_background_label = tk.Label(root, image=user_communication_style_background_photo)
    user_communication_style_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    proceed_button = tk.Button(root, image=proceed_button_photo, command=lovelanguage_selection, background='#DD7FBA', activebackground="lightpink", highlightthickness=5, bd=0)
    proceed_button.place(x=1200, y=750, anchor=tk.CENTER)
    add_to_counter()

    #query Prolog
    advice = get_pl_communication_style(input_selected_mbti.lower())
    show_pl_results(advice)


# Function to handle Love Language selection slideshow
def lovelanguage_selection():
    # Clear the current widgets
    for widget in root.winfo_children():
        widget.destroy()

    # List of Love Language types and their images
    love_language = ["words_of_affirmation", "quality_time", "acts_of_service", "physical_touch", "receiving_gifts"]
    images = [Image.open(os.path.join(script_dir, "Assets", "LoveLanguage",f"{love_language}.png")) for love_language in love_language]
    photos = [ImageTk.PhotoImage(img) for img in images]

    # Index to track current MBTI type
    current_index = [0]

    global love_language_background_photo  # Keep a reference to avoid garbage collection
    love_language_image_path = os.path.join(script_dir, "Assets", "Background","lovelanguage_background_photo.png")
    love_language_background_image = Image.open(love_language_image_path)
    love_language_background_photo = ImageTk.PhotoImage(love_language_background_image)
    
    love_language_background_label = tk.Label(root, image=love_language_background_photo)
    love_language_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def update_love_language(index):
        love_language_label.config(image=photos[index])
        love_language_label.image = photos[index]
        global input_love_language
        input_love_language = love_language[index]  
        

    # Function to show the next MBTI type
    def next_love_language():
        current_index[0] = (current_index[0] + 1) % len(love_language)
        update_love_language(current_index[0])

    # Function to show the previous MBTI type
    def previous_love_language():
        current_index[0] = (current_index[0] - 1) % len(love_language)
        update_love_language(current_index[0])

    # Create MBTI display widgets
    love_language_label = tk.Label(root,background='#E085B8')
    love_language_label.place(x=960, y=550, anchor=tk.CENTER)

    # Load button images
    global prev_photo,next_photo, proceed_photo  # Keep a reference to avoid garbage collection
    prev_image_path = os.path.join(script_dir, "Assets", "Buttons","previous_button.png")
    next_image_path = os.path.join(script_dir, "Assets", "Buttons","next_button.png")
    proceed_image_path = os.path.join(script_dir, "Assets", "Buttons","proceed_button.png")
    
    prev_image = Image.open(prev_image_path)
    next_image = Image.open(next_image_path)
    proceed_image = Image.open(proceed_image_path)
    
    prev_photo = ImageTk.PhotoImage(prev_image)
    next_photo = ImageTk.PhotoImage(next_image)
    proceed_photo = ImageTk.PhotoImage(proceed_image)

    # Create navigation buttons
    prev_button = tk.Button(root, image=prev_photo, background='#E898AE', activebackground="lightpink", command=previous_love_language)
    next_button = tk.Button(root, image=next_photo, background='#D772C4', activebackground="lightpink", command=next_love_language)
    proceed_button = tk.Button(root, image=proceed_photo,command=rank_values, background='#DD7FBA',activebackground="lightpink", highlightthickness=5, bd=0)

    prev_button.place(x=600, y=600, anchor=tk.CENTER)
    next_button.place(x=1320, y=600, anchor=tk.CENTER)
    proceed_button.place(x=960, y=940, anchor=tk.CENTER)

    # Initialize with the first love language
    update_love_language(current_index[0])
    add_to_counter()

    #query Prolog
    #advice = get_pl_love_language(input_selected_mbti.lower())
    #show_pl_results(advice)


def rank_values():
    # Clear the current widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Load and display the background image
    global values_background_photo, value_listbox, next_button_photo, up_photo, down_photo  # Keep a reference to avoid garbage collection
    values_image_path = os.path.join(script_dir,"Assets", "Background", "value_background_photo.png")
    up_image_path = os.path.join(script_dir, "Assets", "Buttons","up.png")
    down_image_path = os.path.join(script_dir, "Assets", "Buttons","down.png")

    values_background_image = Image.open(values_image_path)
    up_image = Image.open(up_image_path)
    down_image = Image.open(down_image_path)

    values_background_photo = ImageTk.PhotoImage(values_background_image)
    up_photo = ImageTk.PhotoImage(up_image)
    down_photo = ImageTk.PhotoImage(down_image)
      
    values_background_label = tk.Label(root, image=values_background_photo)
    values_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # List of items to rank
    value_items = ["Family", "Friends", "Career", "Personal Growth", "Community", "Independence"]

    # Listbox for displaying items
    value_listbox = tk.Listbox(root, font=("Helvetica", 42), bg="#FFCCFF", selectmode=tk.SINGLE, justify='center')
    for item in value_items:
        value_listbox.insert(tk.END, item)
    value_listbox.place(relx=0.5, rely=0.53, anchor=tk.CENTER, width=650, height=400)

    # Button to move selected item up
    up_button = tk.Button(root,image=up_photo, activebackground="lightpink", bg="#E999AB",command=move_up)
    up_button.place(relx=0.2, y=550, anchor=tk.CENTER)

    # Button to move selected item down
    down_button = tk.Button(root,image=down_photo,activebackground="lightpink", bg="#D770C6", command=move_down)
    down_button.place(relx=0.8, y=550, anchor=tk.CENTER)

    # Next button
    next_button_image_path = os.path.join(script_dir, "Assets", "Buttons","proceed_button.png")
    next_button_image = Image.open(next_button_image_path)
    next_button_photo = ImageTk.PhotoImage(next_button_image)
    next_button = tk.Button(root, image=next_button_photo, command=check_interests,
                            background='#DD7FBA', activebackground="lightpink", bd=0)
    next_button.place(relx=0.5, y=900, anchor=tk.CENTER)
    add_to_counter()

# Function to handle checking interests
def check_interests():
    # Clear the current widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Load and display the background image
    global interests_background_photo, next_button_photo, checked_image, unchecked_image  # Keep a reference to avoid garbage collection
    interests_image_path = os.path.join(script_dir, "Assets", "Background", "interest_background_photo.png")
    interests_background_image = Image.open(interests_image_path)
    interests_background_photo = ImageTk.PhotoImage(interests_background_image)
      
    interests_background_label = tk.Label(root, image=interests_background_photo)
    interests_background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Load checkbox images
    checked_image_path = os.path.join(script_dir,"Assets", "Buttons", "checked.png")
    unchecked_image_path = os.path.join(script_dir, "Assets", "Buttons","unchecked.png")
    try:
        checked_image = ImageTk.PhotoImage(Image.open(checked_image_path).resize((75, 75), Image.LANCZOS))
        unchecked_image = ImageTk.PhotoImage(Image.open(unchecked_image_path).resize((75, 75), Image.LANCZOS))
        print("Images loaded successfully")
    except Exception as e:
        print(f"Error loading images: {e}")
        return

    # Message label
    message_label = tk.Label(root, text="", font=("Helvetica", 16), fg="red", bg="#DD7FBA")
    message_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    # List of interests
    interests_left = ["Reading", "Traveling", "Music", "Sports", "Art"]
    interests_right = ["Cooking", "Writing", "Science", "Pet Care", "Gaming"]

    # Variables for checkboxes
    interest_vars = {interest: tk.IntVar() for interest in interests_left + interests_right}

    selected_count = tk.IntVar(value=0)

    # Function to toggle checkbox images and restrict selection to three
    def toggle_checkbox(var, btn, interest):
        if var.get():
            if selected_count.get() < 3:
                btn.config(image=checked_image)
                selected_count.set(selected_count.get() + 1)
                if interest not in input_selected_interests:  # Prevent duplicates
                    input_selected_interests.append(interest)
                message_label.config(text="")
            else:
                var.set(0)
                message_label.config(text="You can only select up to 3 interests.")
        else:
            btn.config(image=unchecked_image)
            selected_count.set(selected_count.get() - 1)
            if interest in input_selected_interests:
                input_selected_interests.remove(interest)
            message_label.config(text="")

    # Create checkboxes for left column
    for i, interest in enumerate(interests_left):
        var = interest_vars[interest]
        btn = tk.Checkbutton(root, text=interest, font=("Helvetica", 32), variable=var, padx=20,
                             bg="#FFCCFF", highlightthickness=0, bd=0, selectcolor="#FFCCFF",
                             image=unchecked_image, compound='left')
        btn.config(command=partial(toggle_checkbox, var, btn, interest))
        btn.image = unchecked_image  # Keep a reference to avoid garbage collection
        btn.selectimage = checked_image  # Keep a reference to avoid garbage collection
        btn.place(relx=0.20, rely=0.35 + i*0.096, anchor=tk.W)

    # Create checkboxes for right column
    for i, interest in enumerate(interests_right):
        var = interest_vars[interest]
        btn = tk.Checkbutton(root, text=interest, font=("Helvetica", 32), variable=var, 
                             bg="#FFCCFF", highlightthickness=0, bd=0, selectcolor="#FFCCFF", padx=20, 
                             image=unchecked_image, compound='left')
        btn.config(command=partial(toggle_checkbox, var, btn, interest))
        btn.image = unchecked_image  # Keep a reference to avoid garbage collection
        btn.selectimage = checked_image  # Keep a reference to avoid garbage collection
        btn.place(relx=0.58, rely=0.35 + i*0.096, anchor=tk.W)

    # Load the Next button image
    next_button_image_path = os.path.join(script_dir, "Assets", "Buttons","proceed_button.png")
    try:
        next_button_image = Image.open(next_button_image_path)
        next_button_photo = ImageTk.PhotoImage(next_button_image)
        print("Next button image loaded successfully")
    except Exception as e:
        print(f"Error loading next button image: {e}")
        return

    # Create the Next button
    next_button = tk.Button(root, image=next_button_photo, command=loading_screen,
                            background='#DD7FBA', activebackground="lightpink", bd=0)
    next_button.image = next_button_photo  # Keep a reference to avoid garbage collection
    next_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
    add_to_counter()



def result():
    # Clear the current widgets
    for widget in root.winfo_children():
        widget.destroy()

    global result_background_photo, done_button_photo  # Keep a reference to avoid garbage collection
    result_image_path = os.path.join(script_dir, "Assets", "Background", "result_background.png")
    done_image_path = os.path.join(script_dir, "Assets", "Buttons", "done_button.png")

    result_background_image = Image.open(result_image_path)
    done_button_image = Image.open(done_image_path)

    result_background_photo = ImageTk.PhotoImage(result_background_image)
    done_button_photo = ImageTk.PhotoImage(done_button_image)

    result_background_label = tk.Label(root, image=result_background_photo)
    result_background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    done_button = tk.Button(root, image=done_button_photo, command=close_window,
                            background='#DD7FBA', activebackground="lightpink", bd=0)
    done_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    print_inputs()
    add_to_counter()

    # Query Prolog
    partner_mbti = get_pl_partner_match(input_selected_mbti.lower())
    partner_love_language = get_pl_partner_love_language(input_love_language)
    partner_interests = get_pl_partner_interests(input_selected_interests)  # list of 3 strings
    partner_values = get_pl_partner_values(input_ranked_values)  # list of 6 strings
    
    print("Partner MBTI: ", partner_mbti)
    print("Partner Love Language: ", partner_love_language)
    print("Partner Interests: ", partner_interests)
    print("Partner Values Ranking: ", partner_values)

    print("MBTI desc: ", data['mbti_types'][partner_mbti])
    
    bg_color = "#e188b4"
    #show_pl_results(partner_mbti)

    title_font = tkfont.Font(family="Helvetica", size=30, weight="bold")
    body_font = tkfont.Font(family="Helvetica", size=15)

    # Partner MBTI
    mbti_title = tk.Label(root, text="Partner MBTI", bg=bg_color, font=title_font)
    mbti_title.place(relx=0.5, y=200, anchor=tk.CENTER)  # Adjust y as needed
    mbti_body1 = tk.Label(root, text=f"{partner_mbti.upper()}", bg=bg_color, font=body_font)
    mbti_body1.place(relx=0.5, y=240, anchor=tk.CENTER)  # Adjust y as needed
    mbti_body2 = tk.Label(root, text=f"{data['mbti_types'][partner_mbti]}", bg=bg_color, font=body_font)
    mbti_body2.place(relx=0.5, y=280, anchor=tk.CENTER)  # Adjust y as needed

    #Partner Love Language
    ll_title = tk.Label(root, text="Partner Love Language", bg=bg_color, font=title_font)
    ll_title.place(relx=0.5, y=360, anchor=tk.CENTER)  # Adjust y as needed
    ll_body = tk.Label(root, text=f"{partner_love_language.replace("_", " ")}", bg=bg_color, font=body_font)
    ll_body.place(relx=0.5, y=400, anchor=tk.CENTER)  # Adjust y as needed
    ll_body = tk.Label(root, text=f"{data['love_languages'][partner_love_language]}", bg=bg_color, font=body_font)
    ll_body.place(relx=0.5, y=440, anchor=tk.CENTER)  # Adjust y as needed

    #Partner Interests
    interests_title = tk.Label(root, text="Partner Interests", bg=bg_color, font=title_font)
    interests_title.place(relx=0.5, y=520, anchor=tk.CENTER)  
    interests_string = ', '.join(partner_interests)
    body1 = tk.Label(root, text=f"{interests_string}", bg=bg_color, font=body_font)
    body1.place(relx=0.5, y=560, anchor=tk.CENTER)  
    body2 = tk.Label(root, text=f"{data['interests'][partner_interests[0]]}", bg=bg_color, font=body_font)
    body2.place(relx=0.5, y=600, anchor=tk.CENTER)  

    #Partner Values
    values_title = tk.Label(root, text="Partner Values", bg=bg_color, font=title_font)
    values_title.place(relx=0.5, y=680, anchor=tk.CENTER)  
    values_string = ', '.join(partner_values)
    body1 = tk.Label(root, text=f"{values_string}", bg=bg_color, font=body_font)
    body1.place(relx=0.5, y=720, anchor=tk.CENTER)  
    body2 = tk.Label(root, text=f"{data['values'][partner_values[0]]}", bg=bg_color, font=body_font)
    body2.place(relx=0.5, y=760, anchor=tk.CENTER)  

def print_inputs():
    print("Selected MBTI:", input_selected_mbti)
    print("Selected Love Language:", input_love_language)
    print("Ranked Values:", input_ranked_values)
    print("Selected Interests:", input_selected_interests)





# Function to close the window
def close_window():
    root.destroy()



def move_up():
    selected_index = value_listbox.curselection()
    if not selected_index:
        return
    selected_index = selected_index[0]
    if selected_index == 0:
        return
    item = value_listbox.get(selected_index)
    value_listbox.delete(selected_index)
    value_listbox.insert(selected_index - 1, item)
    value_listbox.select_set(selected_index - 1)
    update_ranked_values()

def move_down():
    selected_index = value_listbox.curselection()
    if not selected_index:
        return
    selected_index = selected_index[0]
    if selected_index == value_listbox.size() - 1:
        return
    item = value_listbox.get(selected_index)
    value_listbox.delete(selected_index)
    value_listbox.insert(selected_index + 1, item)
    value_listbox.select_set(selected_index + 1)
    update_ranked_values()

def update_ranked_values():
    global input_ranked_values
    input_ranked_values = [value_listbox.get(i) for i in range(value_listbox.size())]

def update_tip():
    global tip_index
    tip_index = (tip_index + 1) % len(tips)
    tip_label.config(text=tips[tip_index])
    root.after(5000, update_tip)  # Update tip every 3 seconds

def update_gif(label):
    global gif_index
    gif_index = (gif_index + 1) % len(gif_frames)
    label.config(image=gif_frames[gif_index])
    root.after(100, update_gif, label)  # Adjust the delay as needed

def animate_dots():
    global dots
    dots = (dots + 1) % 4
    loading_text_label.config(text="Preparing personalized advice" + "." * dots)
    root.after(500, animate_dots)



# Add the START button
start_button = tk.Button(root, command=open_gender_selection, background='#DD7FBA',activebackground="lightpink", highlightthickness=5, bd=0)
start_button.place(x=960, y=850, anchor=tk.CENTER)

# Start the animation

update_frame(0)

# Run the application
root.mainloop()
