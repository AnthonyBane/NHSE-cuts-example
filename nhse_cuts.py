from PIL import Image, ImageDraw

BLUE = (0, 102, 204)  # Remaining staff
ORANGE = (255, 140, 0)  # Lost in 2023
RED = (204, 0, 0)  # To leave by 2027

dot_size = 6
dots_per_row = 150

# Workforce numbers. Source: https://assets.publishing.service.gov.uk/media/6852d972ff16d05c5e6aa6ce/dhsc-workforce-management-information-march-2025-updated.csv
current_nhse = 16138
current_dhsc = 3708

# Estimating pre-merger NHSE workforce
# Source: https://assets.publishing.service.gov.uk/media/6709344a92bb81fcdbe7b728/nhs-england-annual-report-and-accounts-2023-to-2024.pdf?utm_source=chatgpt.com
estimated_pre_2023_merger = int(current_nhse / 0.64)

# Step 1: Staff remaining after first cut (pre-merger to current NHSE)
lost_2023 = estimated_pre_2023_merger - current_nhse

# Step 2: Staff remaining after further 50% cut (NHSE + DHSC)
total_post_merge = current_nhse + current_dhsc
remaining_2027 = planned_reduction = total_post_merge // 2


def create_dot_image(dot_colors, filename, legend_items):
    total_dots = len(dot_colors)
    rows_needed = (total_dots + dots_per_row - 1) // dots_per_row
    legend_height = 40 if legend_items else 0
    img_width = dots_per_row * dot_size
    img_height = rows_needed * dot_size + legend_height

    image = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(image)

    for idx, color in enumerate(dot_colors):
        row = idx // dots_per_row
        col = idx % dots_per_row
        x0 = col * dot_size
        y0 = row * dot_size + legend_height
        x1 = x0 + dot_size
        y1 = y0 + dot_size
        draw.ellipse([x0, y0, x1, y1], fill=color)

    if legend_items:
        padding = 10
        box_size = 12
        x = padding
        y = 10
        for color, label in legend_items:
            draw.rectangle([x, y, x + box_size, y + box_size], fill=color)
            draw.text((x + box_size + 5, y - 2), label, fill=(0, 0, 0))
            x += 180

    image.save(filename)
    print(f"Saved {filename}")


# ----- Step 3: total staff remaining vs total cuts -----
dots_step = [BLUE] * remaining_2027 + [ORANGE] * lost_2023 + [RED] * planned_reduction
legend_step = [(BLUE, "Remaining Staff"), (ORANGE, "Lost in 2023"), (RED, "Planned Reductions 2027")]
create_dot_image(dots_step, "nhse_dhsc_cuts.png", legend_step)
