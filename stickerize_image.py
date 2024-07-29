from PIL import Image, ImageOps, ImageFilter
import sys

# Load the auto-cropped image
image_path = sys.argv[1]
image = Image.open(image_path).convert("RGBA")

# Define the width of the white border
border_width = 10

# Create a mask from the image alpha channel
mask = image.split()[3]

# Increase the size of the mask to create the border effect
expanded_mask = ImageOps.expand(mask, border=border_width, fill=255)
expanded_mask = expanded_mask.filter(ImageFilter.GaussianBlur(border_width // 2))

# Create an image for the border
border = Image.new("RGBA", expanded_mask.size, (255, 255, 255, 255))
border.putalpha(expanded_mask)

# Create a new image to place the border and the original image
final_border_image = Image.new("RGBA", border.size, (255, 255, 255, 0))
final_border_image.paste(border, (0, 0))
final_border_image.paste(image, (border_width, border_width), mask)

# Save the new image with the white border
final_sticker_path_with_contour_border_corrected = f"{image_path}_stickerized.png"
final_border_image.save(final_sticker_path_with_contour_border_corrected)

print(final_sticker_path_with_contour_border_corrected)

