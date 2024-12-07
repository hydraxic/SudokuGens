from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def draw_x_sudoku_grid(c, grid, page_width, page_height, count, cell_size=30):
    grid_width = 9 * cell_size
    grid_height = 9 * cell_size

    # Determine the vertical position based on count
    if count % 2 == 0:  # Even count: top of the page
        y_start = grid_height + (grid_height / 4)
    else:  # Odd count: bottom of the page
        y_start = page_height - (grid_height / 4)

    x_start = (page_width - grid_width) / 2

    # Shade the diagonal cells
    for i in range(9):
        # Top-left to bottom-right diagonal
        x = x_start + i * cell_size
        y = y_start - i * cell_size
        c.setFillGray(0.9)  # Light gray shade
        c.rect(x, y - cell_size, cell_size, cell_size, fill=1, stroke=0)

        # Top-right to bottom-left diagonal
        x = x_start + (8 - i) * cell_size
        y = y_start - i * cell_size
        c.rect(x, y - cell_size, cell_size, cell_size, fill=1, stroke=0)

    c.setStrokeColorRGB(0, 0, 0)  # Set line color to black
    c.setFillColorRGB(0, 0, 0)  # Set text color to black

    # Draw the main grid
    for i in range(10):  # Includes outer border
        line_width = 2 if i % 3 == 0 else 0.5
        c.setLineWidth(line_width)

        # Vertical lines
        c.line(x_start + i * cell_size, y_start, x_start + i * cell_size, y_start - 9 * cell_size)
        # Horizontal lines
        c.line(x_start, y_start - i * cell_size, x_start + 9 * cell_size, y_start - i * cell_size)

    # Draw the count number above the grid
    count_x = x_start + grid_width / 2 - 10
    count_y = y_start + 20
    c.setFont("HanumanRegular", 12)
    c.drawString(count_x, count_y, f"{count + 1}")

    watermark_x = page_width - 100
    watermark_y = 30
    c.setFont("HanumanRegular", 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)  # Light gray color for watermark
    c.drawString(watermark_x, watermark_y, "Made by HydroPuzzles")
    c.setFillColorRGB(0, 0, 0)  # Reset to black for further drawings

    # Add numbers to cells
    for row_idx, row in enumerate(grid):
        for col_idx, num in enumerate(row):
            if num != 0:  # Skip empty cells
                x = x_start + col_idx * cell_size + 11  # Offset for text centering
                y = y_start - row_idx * cell_size - 20  # Offset for text centering
                c.drawString(x, y, str(num))

pdfmetrics.registerFont(TTFont('HanumanRegular', 'Hanuman-Regular.ttf'))

with open("/content/goodSudoku.json", "r") as f:
    puzzles = json.load(f)

max = 5
count = 0

c = canvas.Canvas("/content/x_sudoku_sample.pdf", pagesize=letter)
page_width, page_height = letter

for puzzle in puzzles:
    # Generate the X-Sudoku PDF
    if count <= max:
        if count % 2 == 0 and count != 0:
            c.showPage()
        draw_x_sudoku_grid(c, puzzle, page_width, page_height, count)
    count += 1

with open("/content/goodSudokuSolution.json", "r") as f:
    puzzless = json.load(f)

count = 0

cs = canvas.Canvas("/content/x_sudoku_sample_solution.pdf", pagesize=letter)
page_width, page_height = letter

for puzzle in puzzless:
    # Generate the X-Sudoku PDF
    if count <= max:
        if count % 2 == 0 and count != 0:
            cs.showPage()
        draw_x_sudoku_grid(cs, puzzle, page_width, page_height, count)
    count += 1
c.save()
cs.save()