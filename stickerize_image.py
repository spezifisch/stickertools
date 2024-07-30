from PIL import Image, ImageOps, ImageFilter
import sys

# Load the auto-cropped image
image_path = sys.argv[1]
image = Image.open(image_path).convert("RGBA")

# Define the width of the white border
outline_kernel_size = 5
temporary_additional_border = 50

# Resize the image by adding a 50px border around it
expanded_image = ImageOps.expand(
    image, border=temporary_additional_border, fill=(255, 255, 255, 0)
)

print(f"Original image size: {image.size}")
print(f"Expanded image size: {expanded_image.size}")

# Create a mask from the expanded image alpha channel; this is like a selection
mask = expanded_image.split()[3]
print(f"Initial mask size: {mask.size}")

# Grow the mask to create the border effect
grown_mask = mask.filter(ImageFilter.MaxFilter(outline_kernel_size))
print(f"Grown mask size: {grown_mask.size}")

# Create an image for the border
border = Image.new("RGBA", expanded_image.size, (255, 255, 255, 255))
border.putalpha(grown_mask)
print(f"Border size: {border.size}")

# Create a new image to place the border and the original image
final_border_image = Image.new("RGBA", expanded_image.size, (255, 255, 255, 0))
final_border_image.paste(border, (0, 0))
final_border_image.paste(expanded_image, (0, 0), mask)

# Crop the image to remove the additional border
space_around = outline_kernel_size
cropped_final_border_image = final_border_image.crop(
    (
        temporary_additional_border - space_around,
        temporary_additional_border - space_around,
        final_border_image.width - temporary_additional_border + space_around,
        final_border_image.height - temporary_additional_border + space_around,
    )
)

# Save the new image with the white border
final_sticker_path_with_contour_border_corrected = f"{image_path}_stickerized.png"
cropped_final_border_image.save(final_sticker_path_with_contour_border_corrected)

print(final_sticker_path_with_contour_border_corrected)
