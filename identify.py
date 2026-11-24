# ============================================================
# FILE: identify.py
# LESSON: Asking an AI to look at a photo and tell you what's in it
# ============================================================
#
# We send each fish photo to the Anthropic API.
# The API runs Claude, which looks at the image and tells us
# what species of fish it sees.
#
# The flow is:
#   1. Load the image file from disk
#   2. Convert it to base64 (a text-safe encoding for binary files)
#   3. Send it to the Anthropic API with a question
#   4. Read the response and extract the species name
# ============================================================

import os       # For reading environment variables and file paths
import base64   # For converting image bytes to text (built into Python)
import json     # For reading the structured response from the AI (built into Python)
import anthropic


def load_image(image_path):
    """
    Read an image file from disk and return it as a base64 string.

    Why base64? Images are binary files (raw bytes).
    The Anthropic API communicates via text (JSON).
    Base64 converts binary bytes into safe text characters,
    so we can include the image inside a text request.

    Returns the base64 string, or None if the file can't be read.
    """

    # --------------------------------------------------------
    # LESSON: try / except
    # --------------------------------------------------------
    # Some operations can fail — like opening a file that
    # doesn't exist or that you don't have permission to read.
    #
    # Without try/except, a failure CRASHES your program.
    # With try/except, you catch the error and handle it nicely.
    # --------------------------------------------------------
    try:
        # "rb" = "read binary" — images are binary files, not text
        with open(image_path, "rb") as f:
            raw_bytes = f.read()

        # base64.b64encode() converts bytes → base64 bytes
        # .decode("utf-8") converts base64 bytes → a regular string
        return base64.b64encode(raw_bytes).decode("utf-8")

    except FileNotFoundError:
        print("  Error: File not found:", image_path)
        return None


def get_media_type(image_path):
    """
    Return the image format string the API needs.

    The API needs to know whether we're sending a JPEG, PNG, etc.
    We figure this out from the file extension.
    """

    # os.path.splitext("nemo.jpg") returns ("nemo", ".jpg")
    # [1] grabs the second item — the extension
    # .lower() converts ".JPG" to ".jpg" so comparisons work
    extension = os.path.splitext(image_path)[1].lower()

    # A dictionary maps keys to values — like a lookup table
    formats = {
        ".jpg":  "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png":  "image/png",
        ".webp": "image/webp",
    }

    # .get(key, default) looks up the key, and if it's not found
    # returns the default value ("image/jpeg" here)
    return formats.get(extension, "image/jpeg")


def identify_fish(image_path):
    """
    Send an image to the Anthropic API and identify the fish species.

    Returns a tuple: (species_name, confidence_score)
    For example: ("Clownfish", 0.95)

    If identification fails, returns: ("Unknown", 0.0)
    """

    print("  Analysing:", os.path.basename(image_path))

    # Step 1: Load the image
    image_data = load_image(image_path)
    if image_data is None:
        return ("Unknown", 0.0)

    # Step 2: Create the Anthropic client
    # It automatically reads ANTHROPIC_API_KEY from your environment
    client = anthropic.Anthropic()

    # Step 3: Send the request
    # We ask Claude to respond ONLY in JSON so it's easy to parse
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": get_media_type(image_path),
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "You are a marine biologist. Identify the fish species in this photo.\n"
                                "Reply ONLY with valid JSON in this exact format, nothing else:\n"
                                '{"species": "Common name", "confidence": 0.95}\n'
                                "If no fish is visible, use: "
                                '{"species": "No fish detected", "confidence": 1.0}'
                            )
                        }
                    ],
                }
            ],
        )

        # Step 4: Parse the JSON response
        # response.content is a list — we want the text of the first item
        raw_text = response.content[0].text.strip()

        # json.loads() converts a JSON string into a Python dictionary
        result = json.loads(raw_text)

        species    = result["species"]
        confidence = float(result["confidence"])

        print("  Identified:", species, f"({confidence:.0%} confident)")
        return (species, confidence)

    except json.JSONDecodeError:
        print("  Could not parse the AI response. Skipping.")
        return ("Unknown", 0.0)

    except Exception as error:
        print("  Error during identification:", error)
        return ("Unknown", 0.0)
