from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json

def draw_x_sudoku_grid(c, grid, page_width, page_height, cell_size=30):
    grid_width = 9 * cell_size
    grid_height = 9 * cell_size
    x_start = (page_width - grid_width) / 2
    y_start = (page_height + grid_height) / 2

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
    
    # Add numbers to cells
    for row_idx, row in enumerate(grid):
        for col_idx, num in enumerate(row):
            if num != 0:  # Skip empty cells
                x = x_start + col_idx * cell_size + 11  # Offset for text centering
                y = y_start - row_idx * cell_size - 20  # Offset for text centering
                c.drawString(x, y, str(num))

def draw_x_sudoku_grid_solution(c, grid, page_width, page_height, cell_size=30):
    grid_width = 9 * cell_size
    grid_height = 9 * cell_size
    x_start = (page_width - grid_width) / 2
    y_start = (page_height + grid_height) / 2

    # Shade the diagonal cells
    for i in range(9):
        # Top-left to bottom-right diagonal
        x = x_start + i * cell_size
        y = y_start - i * cell_size
        c.setFillGray(0.825)  # Light gray shade
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
    
    # Add numbers to cells
    for row_idx, row in enumerate(grid):
        for col_idx, num in enumerate(row):
            if num != 0:  # Skip empty cells
                x = x_start + col_idx * cell_size + 11  # Offset for text centering
                y = y_start - row_idx * cell_size - 20  # Offset for text centering
                c.drawString(x, y, str(num))

with open("/content/goodSudoku.json", "r") as f:
    puzzles = json.load(f)

max = 5

c = canvas.Canvas("/content/x_sudoku_sample.pdf", pagesize=letter)
page_width, page_height = letter

for puzzle in puzzles:
    # Generate the X-Sudoku PDF
    draw_x_sudoku_grid(c, puzzle, page_width, page_height)
    c.showPage()

with open("/content/goodSudokuSolution.json", "r") as f:
    puzzless = json.load(f)

cs = canvas.Canvas("/content/x_sudoku_sample_solution.pdf", pagesize=letter)
page_width, page_height = letter

for puzzle in puzzless:
    # Generate the X-Sudoku PDF
    draw_x_sudoku_grid_solution(cs, puzzle, page_width, page_height)
    cs.showPage()

c.save()
cs.save()