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

# Create the contour effect by expanding the mask
contour_mask = expanded_mask
contour_mask = Image.composite(mask, contour_mask, mask)
contour_mask = ImageOps.expand(contour_mask, border=border_width, fill=255)

# Create an image for the border
border = Image.new("RGBA", contour_mask.size, (255, 255, 255, 255))
border.putalpha(contour_mask)

# Create a new image to place the border and the original image
final_border_image = Image.new("RGBA", border.size, (255, 255, 255, 0))
final_border_image.paste(border, (-border_width, -border_width))
final_border_image.paste(expanded_image, (0, 0), mask)

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
