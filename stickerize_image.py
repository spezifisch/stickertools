from PIL import Image, ImageOps
import sys

# Load the auto-cropped image
image_path = sys.argv[1]
image = Image.open(image_path).convert("RGBA")

# Define the width of the white border
border_width = 10
additional_border = 50

# Resize the image by adding a 50px border around it
expanded_image = ImageOps.expand(
    image, border=additional_border, fill=(255, 255, 255, 0)
)

# Create a mask from the expanded image alpha channel
mask = expanded_image.split()[3]

# Expand the mask to create the border effect
expanded_mask = ImageOps.expand(mask, border=border_width, fill=255)

# Ensure the expanded mask and expanded image sizes match
assert (
    expanded_mask.size == expanded_image.size
), "Expanded mask size and expanded image size do not match"

# Create an image for the border with the same size as the expanded image
border_size = expanded_image.size
border = Image.new("RGBA", border_size, (255, 255, 255, 0))
border.putalpha(expanded_mask)

# Ensure the border and expanded image sizes match
assert (
    border.size == expanded_image.size
), "Border size and expanded image size do not match"

# Composite the expanded image with the border
final_border_image = Image.alpha_composite(border, expanded_image)

# Ensure the final composite size matches
assert (
    final_border_image.size == expanded_image.size
), "Final composite size and expanded image size do not match"

# Crop the image to remove the additional border
cropped_final_border_image = final_border_image.crop(
    (
        additional_border,
        additional_border,
        final_border_image.width - additional_border,
        final_border_image.height - additional_border,
    )
)

# Save the new image with the white border
final_sticker_path_with_contour_border_corrected = f"{image_path}_stickerized.png"
cropped_final_border_image.save(final_sticker_path_with_contour_border_corrected)

print(final_sticker_path_with_contour_border_corrected)
