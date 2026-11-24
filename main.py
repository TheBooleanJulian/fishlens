# ============================================================
# FILE: main.py
# LESSON: How to tie a whole project together
# ============================================================
#
# This is the file you run. It:
#   1. Asks the user what they want to do
#   2. Scans a folder of fish photos (using identify.py)
#   3. Saves results to the database (using database.py)
#   4. Prints a report of everything saved so far
#
# HOW TO RUN:
#   1. Install the one required package:
#      pip install anthropic
#
#   2. Set your Anthropic API key in the terminal:
#      Mac/Linux:  export ANTHROPIC_API_KEY="your-key-here"
#      Windows:    set ANTHROPIC_API_KEY=your-key-here
#
#   3. Run:
#      python main.py
# ============================================================

import os                        # Built in — file and folder tools
from datetime import datetime    # Built in — for recording the current time

from dotenv import load_dotenv   # Loads variables from .env into os.environ
load_dotenv()

import database   # Our own file: database.py
import identify   # Our own file: identify.py


# ============================================================
# The image formats we support
# ============================================================
SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]


def scan_folder(folder):
    """
    Look at every image in a folder, identify the fish,
    and save each result to the database.

    Parameters:
        folder - path to the folder as a string, e.g. "./my_photos"
    """

    # --------------------------------------------------------
    # LESSON: Checking if a folder exists before using it
    # --------------------------------------------------------
    if not os.path.exists(folder):
        print("Folder not found:", folder)
        return

    # os.listdir() returns a list of all filenames in a folder
    all_files = os.listdir(folder)

    # --------------------------------------------------------
    # LESSON: Filtering a list with a loop
    # --------------------------------------------------------
    # We go through every file and keep only the ones that
    # have an image extension we support.
    image_files = []

    for filename in all_files:
        # os.path.splitext("nemo.jpg") → ("nemo", ".jpg")
        extension = os.path.splitext(filename)[1].lower()

        if extension in SUPPORTED_EXTENSIONS:
            image_files.append(filename)

    # sorted() puts the filenames in alphabetical order
    image_files = sorted(image_files)

    if len(image_files) == 0:
        print("No images found in:", folder)
        return

    print(f"\nFound {len(image_files)} image(s). Starting scan...\n")

    # --------------------------------------------------------
    # LESSON: enumerate() — looping with a counter
    # --------------------------------------------------------
    # enumerate() gives you both the index and the value:
    #   for i, item in enumerate(my_list, start=1):
    #       print(i, item)   →   1 apple
    #                             2 banana
    # --------------------------------------------------------
    for i, filename in enumerate(image_files, start=1):
        print(f"[{i}/{len(image_files)}] {filename}")

        full_path = os.path.join(folder, filename)

        # identify_fish() returns a tuple: (species, confidence)
        # We "unpack" the tuple into two separate variables
        species, confidence = identify.identify_fish(full_path)

        # Skip if the AI couldn't figure it out
        if species == "Unknown":
            print("  Skipping.\n")
            continue   # 'continue' jumps to the next loop iteration

        # datetime.now() captures the current date and time
        # .isoformat() converts it to a readable string like "2025-06-09T14:32:00"
        scanned_at = datetime.now().isoformat()

        # Save this result to the database
        database.save_sighting(filename, species, confidence, scanned_at)
        print("  Saved.\n")

    print("Scan complete!")


def show_report():
    """
    Print a summary of all fish sightings saved in the database.
    """

    print("\n" + "=" * 50)
    print("  FISHLENS — RESULTS REPORT")
    print("=" * 50)

    # --------------------------------------------------------
    # LESSON: Getting data back from the database
    # --------------------------------------------------------
    species_counts = database.get_species_counts()
    all_sightings  = database.get_all_sightings()

    if len(all_sightings) == 0:
        print("\n  No sightings recorded yet.")
        print("  Scan some fish photos first!\n")
        return

    # --- Species breakdown ---
    print(f"\n  Total photos scanned: {len(all_sightings)}")
    print(f"\n  {'SPECIES':<30}  COUNT")
    print("  " + "-" * 38)

    for species, count in species_counts:
        # "█" * count draws a simple bar, capped at 15 characters
        bar = "█" * min(count, 15)
        print(f"  {species:<30}  {count}x  {bar}")

    # --- Recent scans ---
    print(f"\n  {'FILENAME':<25}  {'SPECIES':<22}  CONFIDENCE")
    print("  " + "-" * 55)

    # --------------------------------------------------------
    # LESSON: List slicing
    # --------------------------------------------------------
    # all_sightings[:10] gives us only the first 10 items.
    # Since they're sorted newest-first, this = the 10 most recent.
    # --------------------------------------------------------
    for row in all_sightings[:10]:
        filename, species, confidence, scanned_at = row   # unpack the tuple

        # Truncate long names so the columns stay tidy
        if len(filename) > 23:
            filename = filename[:20] + "..."
        if len(species) > 20:
            species = species[:17] + "..."

        # f"{confidence:.0%}" formats 0.95 as "95%"
        print(f"  {filename:<25}  {species:<22}  {confidence:.0%}")

    print()


def main():
    """
    Show a simple menu and let the user choose what to do.
    """

    # --------------------------------------------------------
    # LESSON: Environment variables for secrets
    # --------------------------------------------------------
    # We never put our API key directly in the code.
    # Instead it lives in an "environment variable" on your computer.
    # os.environ.get() reads it — returns None if it's not set.
    # --------------------------------------------------------
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        print("\nError: ANTHROPIC_API_KEY is not set.")
        print("Set it in your terminal first:")
        print("  Mac/Linux:  export ANTHROPIC_API_KEY='your-key-here'")
        print("  Windows:    set ANTHROPIC_API_KEY=your-key-here")
        print("\nGet a key at: https://console.anthropic.com\n")
        return

    # Set up the database on first run (safe to call every time)
    database.setup_database()

    # --------------------------------------------------------
    # LESSON: A simple interactive menu with a while loop
    # --------------------------------------------------------
    # 'while True' runs forever until we hit 'break' or 'return'.
    # This keeps the menu showing after each action.
    # --------------------------------------------------------
    while True:
        print("\n--- FishLens ---")
        print("1. Scan a folder of fish photos")
        print("2. View results report")
        print("3. Quit")

        # input() pauses the program and waits for the user to type
        # .strip() removes any accidental spaces or newlines
        choice = input("\nEnter 1, 2, or 3: ").strip()

        if choice == "1":
            folder = input("Enter folder path (e.g. ./photos): ").strip()
            scan_folder(folder)

        elif choice == "2":
            show_report()

        elif choice == "3":
            print("Goodbye!")
            break   # Exit the while loop, ending the program

        else:
            print("Please enter 1, 2, or 3.")


# ============================================================
# LESSON: if __name__ == "__main__"
# ============================================================
# When Python runs THIS file directly, __name__ equals "__main__".
# When another file imports this file, __name__ equals "main".
#
# This check means main() only runs when you execute the file
# directly — not when it's imported by something else.
# It's standard practice in every Python project.
# ============================================================
if __name__ == "__main__":
    main()
