from __future__ import annotations

import aiohttp
import io
from PIL import Image

COLORS = [
    ((0, 0, 0), "⬛"),       # Black
    ((0, 0, 255), "🟦"),    # Blue
    ((255, 0, 0), "🟥"),    # Red
    ((255, 255, 0), "🟨"),  # Yellow
    ((255, 165, 0), "🟧"),  # Orange
    ((255, 255, 255), "⬜"), # White
    ((0, 255, 0), "🟩"),    # Green
]



async def fetch_image(url):
    async with aiohttp.ClientSession() as session: 
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()
                return image_data
            else:
                return None

async def convert_into_image(image_data):
  return Image.open(io.BytesIO(image_data)).convert("RGB")

def euclidean_distance(color1, color2):
    # Calculate the Euclidean distance between two colors

    # Unpack the RGB values for each color: red, green, blue
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    # Calculate the differences in RGB values
    delta_r = r2 - r1
    delta_g = g2 - g1
    delta_b = b2 - b1

    # Compute the squared differences and sum them up
    squared_distance = delta_r ** 2 + delta_g ** 2 + delta_b ** 2

    # Calculate the square root of the summed squares to get the distance
    distance = squared_distance ** 0.5

    return distance

def find_closest_emoji(target_color):
    # Find the closest emoji representation for a given color
    distances = [euclidean_distance(target_color, color[0]) for color in COLORS]

    # Find the index of the closest color
    closest_color_index = distances.index(min(distances))

    # Get the closest emoji
    closest_emoji = COLORS[closest_color_index][1]

    return closest_emoji

def emojify_image(img, size):
    # Resize image
    small_img = img.resize((size, size), Image.NEAREST)

    # Load pixels of image
    pixels = small_img.load()

    # Loop through each row (y-axis)
    # for y in range(size):
        # Loop through each column (x-axis)
        # for x in range(size):
            # Find the closest emoji representation for the current pixel
            # emoji = find_closest_emoji(pixels[x, y])
            # Append the emoji representation to the current row
            # emoji_row += emoji
        # Add a newline after each row is completed to start a new row
        # emoji_grid += emoji_row + '\n'
    
    # Return the final string containing the emoji grid representing the image
    emoji = '\n'.join(''.join(find_closest_emoji(pixels[x, y]) for x in range(size)) for y in range(size))
    
    return emoji
