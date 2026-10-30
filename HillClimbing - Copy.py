import random
import copy
import time
from tkinter import *
from tkinter import ttk

# =====================================================================
# GUI Initialization
# =====================================================================
root = Tk()
root.title("Sudoku Solver - Hill Climbing")
root.geometry("600x750")

# =====================================================================
# Colors
# =====================================================================
DEFAULT_BG = "white"
LIGHT_GREEN = "#ccffcc"
LIGHT_RED = "#ffcccc"
LIGHT_BLUE = "#cce5ff"


# =====================================================================
# 10 Test Datasets (Start States)
# =====================================================================

PUZZLE_1 = [
    [9, 0, 0, 5, 0, 8, 0, 0, 7],
    [0, 8, 0, 3, 0, 2, 9, 0, 5],
    [0, 5, 4, 0, 0, 0, 0, 8, 0],
    [0, 7, 0, 6, 8, 0, 0, 3, 2],
    [1, 0, 0, 0, 0, 4, 0, 0, 8],
    [5, 0, 0, 2, 1, 9, 0, 6, 0],
    [0, 0, 0, 9, 0, 6, 0, 0, 1],
    [7, 2, 6, 0, 0, 1, 0, 4, 0],
    [0, 0, 1, 4, 7, 0, 0, 5, 6]
]

PUZZLE_2 = [
    [0, 0, 4, 3, 0, 0, 0, 0, 1],
    [0, 0, 7, 0, 9, 1, 2, 4, 0],
    [1, 9, 0, 0, 4, 0, 8, 0, 0],
    [7, 0, 9, 2, 0, 0, 5, 0, 6],
    [0, 0, 2, 0, 5, 0, 0, 3, 0],
    [0, 0, 0, 0, 7, 6, 9, 1, 2],
    [4, 0, 5, 0, 8, 0, 0, 0, 0],
    [2, 7, 0, 0, 0, 0, 1, 5, 8],
    [0, 0, 0, 6, 2, 5, 3, 7, 0]
]

PUZZLE_3 = [
    [1, 0, 0, 5, 0, 0, 0, 4, 3],
    [4, 7, 0, 1, 0, 2, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 2, 9, 1],
    [9, 0, 3, 4, 0, 0, 5, 8, 6],
    [6, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 5, 0, 0, 0, 0, 1, 7, 0],
    [3, 0, 5, 8, 0, 0, 9, 6, 2],
    [0, 2, 6, 3, 0, 9, 8, 0, 5],
    [8, 0, 0, 0, 5, 0, 0, 0, 0]
]

PUZZLE_4 = [
    [0, 2, 0, 0, 4, 0, 8, 0, 0],
    [0, 0, 3, 0, 0, 1, 0, 5, 0],
    [8, 0, 1, 7, 0, 6, 3, 4, 9],
    [0, 0, 5, 0, 0, 9, 1, 0, 2],
    [2, 1, 0, 0, 0, 8, 0, 6, 4],
    [0, 0, 0, 0, 6, 0, 5, 0, 0],
    [5, 6, 0, 9, 1, 3, 4, 0, 0],
    [0, 4, 2, 6, 0, 0, 0, 1, 0],
    [1, 0, 7, 0, 0, 0, 6, 0, 3]
]

PUZZLE_5 = [
    [0, 0, 6, 0, 0, 0, 8, 0, 2],
    [7, 0, 0, 4, 2, 8, 0, 9, 6],
    [2, 1, 0, 0, 3, 0, 7, 0, 5],
    [0, 3, 1, 0, 0, 0, 9, 8, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 7],
    [8, 2, 0, 9, 5, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 2, 0, 6, 0],
    [0, 8, 5, 0, 7, 6, 0, 0, 0],
    [9, 0, 2, 5, 0, 1, 3, 0, 8]
]

PUZZLE_6 = [
    [8, 0, 7, 0, 0, 0, 0, 0, 0],
    [0, 3, 1, 0, 0, 2, 4, 0, 0],
    [0, 4, 0, 0, 0, 0, 0, 5, 2],
    [9, 6, 0, 4, 1, 0, 8, 7, 0],
    [1, 0, 0, 7, 0, 3, 9, 2, 0],
    [0, 0, 4, 9, 0, 8, 1, 0, 0],
    [4, 0, 6, 1, 0, 7, 2, 3, 0],
    [7, 5, 3, 0, 0, 0, 0, 9, 1],
    [0, 1, 0, 0, 0, 6, 5, 0, 0]
]

PUZZLE_7 = [
    [0, 5, 8, 0, 3, 0, 0, 2, 0],
    [4, 0, 2, 0, 0, 0, 9, 0, 5],
    [0, 0, 7, 0, 0, 0, 6, 8, 0],
    [2, 9, 0, 0, 5, 4, 0, 7, 0],
    [5, 0, 0, 0, 6, 2, 0, 0, 0],
    [0, 0, 3, 8, 1, 0, 2, 5, 0],
    [1, 0, 9, 0, 0, 3, 0, 6, 4],
    [8, 6, 5, 4, 9, 0, 1, 3, 0],
    [0, 7, 0, 0, 0, 6, 0, 0, 0]
]

PUZZLE_8 = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

PUZZLE_9 = [
    [0, 6, 0, 3, 0, 8, 1, 0, 0],
    [5, 8, 1, 0, 0, 9, 6, 0, 0],
    [0, 0, 3, 5, 0, 0, 0, 0, 0],
    [0, 9, 0, 8, 0, 2, 0, 0, 0],
    [0, 0, 0, 7, 4, 5, 9, 3, 6],
    [3, 5, 0, 0, 0, 6, 8, 0, 4],
    [1, 3, 5, 0, 0, 0, 0, 0, 0],
    [7, 0, 8, 6, 1, 3, 4, 0, 0],
    [9, 4, 0, 0, 0, 7, 3, 0, 0]
]

PUZZLE_10 = [
    [6, 0, 0, 1, 0, 0, 0, 0, 2],
    [8, 0, 1, 0, 9, 0, 0, 0, 0],
    [0, 7, 5, 0, 8, 4, 0, 0, 0],
    [4, 3, 0, 0, 2, 0, 5, 6, 1],
    [5, 1, 8, 7, 0, 0, 4, 0, 9],
    [0, 9, 6, 4, 1, 0, 3, 0, 0],
    [0, 0, 0, 0, 7, 0, 0, 0, 0],
    [0, 6, 0, 0, 3, 1, 0, 5, 0],
    [7, 0, 2, 5, 4, 0, 6, 0, 3]
]

PUZZLES = [None, PUZZLE_1, PUZZLE_2, PUZZLE_3, PUZZLE_4, PUZZLE_5,
           PUZZLE_6, PUZZLE_7, PUZZLE_8, PUZZLE_9, PUZZLE_10]

sudoku_grid = [row[:] for row in PUZZLE_1]
cell_labels = {}
cell_frames = {}


# Core Functions

def find_conflicts(grid):
    """Find all conflicting cell positions."""
    conflicts = set()
    
    for r in range(9):
        seen = {}
        for c in range(9):
            val = grid[r][c]
            if val != 0:
                if val in seen:
                    conflicts.add((r, c))
                    conflicts.add(seen[val])
                else:
                    seen[val] = (r, c)
    
    for c in range(9):
        seen = {}
        for r in range(9):
            val = grid[r][c]
            if val != 0:
                if val in seen:
                    conflicts.add((r, c))
                    conflicts.add(seen[val])
                else:
                    seen[val] = (r, c)
    
    for box_r in range(3):
        for box_c in range(3):
            seen = {}
            for r in range(box_r * 3, box_r * 3 + 3):
                for c in range(box_c * 3, box_c * 3 + 3):
                    val = grid[r][c]
                    if val != 0:
                        if val in seen:
                            conflicts.add((r, c))
                            conflicts.add(seen[val])
                        else:
                            seen[val] = (r, c)
    
    return conflicts


def count_conflicts(grid):
    """Count total conflicting cells."""
    return len(find_conflicts(grid))


def count_empty(grid):
    """Count empty cells"""
    return sum(1 for r in range(9) for c in range(9) if grid[r][c] == 0)


# Goal State

def is_goal_state(grid):
    """
    Check if the current state is a goal state
    """
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return False
    return count_conflicts(grid) == 0


def calculate_fitness(grid):
    conflicts = count_conflicts(grid)
    fitness = max(0, 100 - (conflicts / 81) * 100)
    return min(100, fitness)


# Hill Climbing Algorithm

def get_fixed_cells(grid):
    return [[grid[r][c] != 0 for c in range(9)] for r in range(9)]


def generate_initial_solution(grid, is_fixed):
    current_grid = copy.deepcopy(grid)
    for r in range(9):
        existing = {current_grid[r][c] for c in range(9) if is_fixed[r][c]}
        missing = [num for num in range(1, 10) if num not in existing]
        random.shuffle(missing)
        for c in range(9):
            if not is_fixed[r][c]:
                current_grid[r][c] = missing.pop()
    return current_grid


def hill_climbing_sudoku(grid, max_iterations=200, max_restarts=50, update_callback=None, silent=False):
    """
    Hill Climbing with Random Restarts.
    """
    initial_fixed_mask = get_fixed_cells(grid)
    best_overall_grid = None
    best_overall_conflicts = float('inf')
    total_iterations = 0
    
    if not silent:
        print("\nHill Climbing Started")
        print(f"Max restarts: {max_restarts}, Max iterations: {max_iterations}")
    
    for restart in range(max_restarts):
        current_grid = generate_initial_solution(grid, initial_fixed_mask)
        current_conflicts = count_conflicts(current_grid)
        
        for i in range(max_iterations):
            total_iterations += 1
            
            if is_goal_state(current_grid):
                if not silent:
                    print(f" Found at Restart {restart+1}, Iteration {i+1}!")
                for r in range(9):
                    for c in range(9):
                        grid[r][c] = current_grid[r][c]
                if update_callback:
                    update_callback(grid, 0, True, initial_fixed_mask)
                return current_grid, 0, total_iterations, restart + 1, True

            # Find the best neighbor
            best_neighbor = None
            best_neighbor_conflicts = current_conflicts

            for r in range(9):
                movable_cols = [c for c in range(9) if not initial_fixed_mask[r][c]]
                for idx1 in range(len(movable_cols)):
                    for idx2 in range(idx1 + 1, len(movable_cols)):
                        c1, c2 = movable_cols[idx1], movable_cols[idx2]
                        
                        current_grid[r][c1], current_grid[r][c2] = current_grid[r][c2], current_grid[r][c1]
                        neighbor_conflicts = count_conflicts(current_grid)
                        
                        if neighbor_conflicts < best_neighbor_conflicts:
                            best_neighbor_conflicts = neighbor_conflicts
                            best_neighbor = (r, c1, c2)
                        
                        current_grid[r][c1], current_grid[r][c2] = current_grid[r][c2], current_grid[r][c1]

            # no better neighbor found → restart
            if best_neighbor is None:
                break
            
            r, c1, c2 = best_neighbor
            current_grid[r][c1], current_grid[r][c2] = current_grid[r][c2], current_grid[r][c1]
            current_conflicts = best_neighbor_conflicts

            if update_callback and not silent:
                for row_idx in range(9):
                    for col_idx in range(9):
                        grid[row_idx][col_idx] = current_grid[row_idx][col_idx]
                update_callback(grid, current_conflicts, False, initial_fixed_mask)
                time.sleep(0.01)

        if current_conflicts < best_overall_conflicts:
            best_overall_conflicts = current_conflicts
            best_overall_grid = copy.deepcopy(current_grid)

    if best_overall_grid:
        for r in range(9):
            for c in range(9):
                grid[r][c] = best_overall_grid[r][c]
        if update_callback:
            update_callback(grid, best_overall_conflicts, False, initial_fixed_mask)
    
    if not silent:
        print(f" Completed. Best conflicts: {best_overall_conflicts}")
    
    return best_overall_grid, best_overall_conflicts, total_iterations, restart + 1, False


# Experiment Framework

def run_experiment():
    print("\n" + "=" * 80)
    print(" EXPERIMENT: Hill Climbing on 10 Sudoku Puzzles")
    print("=" * 80)
    
    results = []
    total_time = 0
    solved_count = 0
    
    for i in range(1, 11):
        print(f"\n Testing Puzzle {i}...")
        
        grid = [row[:] for row in PUZZLES[i]]
        
        start_time = time.time()
        solution, conflicts, iterations, restarts, solved = hill_climbing_sudoku(
            grid,
            max_iterations=200,
            max_restarts=50,
            silent=True
        )
        elapsed = time.time() - start_time
        total_time += elapsed
        
        fitness = calculate_fitness(grid)
        
        results.append({
            'puzzle': i,
            'solved': solved,
            'conflicts': conflicts,
            'fitness': fitness,
            'iterations': iterations,
            'restarts': restarts,
            'time': elapsed
        })
        
        if solved:
            solved_count += 1
            print(f"  Solved! (Time: {elapsed:.3f}s, Iterations: {iterations}, Fitness: {fitness:.1f}%)")
        else:
            print(f"  ❌ Not solved. Best conflicts: {conflicts} (Fitness: {fitness:.1f}%, Time: {elapsed:.3f}s)")
    
    # Summary table
    print("\n" + "=" * 80)
    print(" EXPERIMENT SUMMARY")
    print("=" * 80)
    print(f"{'Puzzle':<10} {'Solved':<12} {'Conflicts':<12} {'Fitness':<10} {'Iterations':<14} {'Restarts':<12} {'Time(s)':<10}")
    print("-" * 80)
    
    for r in results:
        status = f"{'YES' if r['solved'] else '❌ NO'}"
        print(f"{r['puzzle']:<10} {status:<12} {r['conflicts']:<12} "
              f"{r['fitness']:<10.1f} {r['iterations']:<14} {r['restarts']:<12} {r['time']:<10.3f}")
    
    avg_time = total_time / len(results)
    avg_iterations = sum(r['iterations'] for r in results) / len(results)
    avg_restarts = sum(r['restarts'] for r in results) / len(results)
    avg_fitness = sum(r['fitness'] for r in results) / len(results)
    
    print("-" * 80)
    print(f" Success Rate: {solved_count}/{len(results)} ({solved_count/len(results)*100:.1f}%)")
    print(f" Average Time: {avg_time:.3f}s")
    print(f" Average Iterations: {avg_iterations:.1f}")
    print(f" Average Restarts: {avg_restarts:.1f}")
    print(f" Average Fitness: {avg_fitness:.1f}%")
    print("=" * 80)
    
    return results


# GUI Colour Functions

def set_cell_color(row, col, color):
    if (row, col) in cell_labels:
        try:
            cell_labels[(row, col)].config(bg=color)
            if (row, col) in cell_frames:
                cell_frames[(row, col)].config(bg=color)
        except:
            pass


def set_cell_value(row, col, value):
    if (row, col) in cell_labels:
        try:
            text = str(value) if value != 0 else ""
            cell_labels[(row, col)].config(text=text)
        except:
            pass


def reset_cell_colors():
    for r in range(9):
        for c in range(9):
            set_cell_color(r, c, DEFAULT_BG)


def update_board_display():
    for row in range(9):
        for col in range(9):
            set_cell_value(row, col, sudoku_grid[row][col])


def highlight_conflicts(grid, is_fixed=None):
    """
    - Fixed cells: blue
    - Conflicting cells: red
    - Correct non-fixed cells: green
    - Empty cells: white
    """
    if is_fixed is None:
        is_fixed = get_fixed_cells(grid)
    conflict_positions = find_conflicts(grid)
    
    for r in range(9):
        for c in range(9):
            val = grid[r][c]
            
            if val == 0:
                set_cell_color(r, c, DEFAULT_BG)
            elif is_fixed[r][c]:
                set_cell_color(r, c, LIGHT_BLUE)
            elif (r, c) in conflict_positions:
                set_cell_color(r, c, LIGHT_RED)
            else:
                set_cell_color(r, c, LIGHT_GREEN)


def mark_board_solved():
    """Turn all cells green when solved."""
    for r in range(9):
        for c in range(9):
            set_cell_color(r, c, LIGHT_GREEN)


def update_gui(grid, conflicts, solved=False, is_fixed=None):
    """Update the GUI with current grid state."""
    for row in range(9):
        for col in range(9):
            set_cell_value(row, col, grid[row][col])
    
    fitness = calculate_fitness(grid)
    
    if solved:
        mark_board_solved()
        status_label.config(text=f"SOLVED! Fitness: 100%", fg="green")
        progress_bar['value'] = 100
    else:
        highlight_conflicts(grid, is_fixed)
        status_label.config(
            text=f"Conflicts: {conflicts} | Fitness: {fitness:.1f}%",
            fg="blue"
        )
        progress_bar['value'] = fitness
    
    root.update()


# Load Puzzle

def load_puzzle(puzzle_num):
    global sudoku_grid
    sudoku_grid = [row[:] for row in PUZZLES[puzzle_num]]
    reset_cell_colors()
    update_board_display()
    
    fixed_mask = get_fixed_cells(sudoku_grid)
    highlight_conflicts(sudoku_grid, fixed_mask)
    
    status_label.config(text=f" Puzzle {puzzle_num} loaded", fg="black")
    progress_bar['value'] = calculate_fitness(sudoku_grid)
    print(f" Loaded Puzzle {puzzle_num}")


# Button Functions

def solve_button():
    """Solve the current puzzle using Hill Climbing"""
    solve_btn.config(state=DISABLED)
    for btn in puzzle_btns:
        btn.config(state=DISABLED)
    
    fixed_mask = get_fixed_cells(sudoku_grid)
    
    status_label.config(text=" Solving...", fg="blue")
    progress_bar['value'] = 0
    root.update()
    
    start_time = time.time()
    
    solution, conflicts, iterations, restarts, solved = hill_climbing_sudoku(
        sudoku_grid,
        max_iterations=200,
        max_restarts=50,
        update_callback=update_gui
    )
    
    elapsed_time = time.time() - start_time
    
    if solved:
        mark_board_solved()
        status_label.config(
            text=f"SOLVED! ({iterations} steps, {elapsed_time:.2f}s)",
            fg="green"
        )
        progress_bar['value'] = 100
        print(f"Solved! Iterations: {iterations}, Restarts: {restarts}, Time: {elapsed_time:.2f}s")
    else:
        highlight_conflicts(sudoku_grid, fixed_mask)
        fitness = calculate_fitness(sudoku_grid)
        status_label.config(
            text=f"Best: {conflicts} conflicts | Fitness: {fitness:.1f}% | {elapsed_time:.2f}s",
            fg="red"
        )
        progress_bar['value'] = fitness
        print(f"Not solved. Best conflicts: {conflicts}, Time: {elapsed_time:.2f}s")
    
    solve_btn.config(state=NORMAL)
    for btn in puzzle_btns:
        btn.config(state=NORMAL)
    root.update()


# Draw GUI

def draw_board():
    global status_label, solve_btn, progress_bar, puzzle_btns
    
    # Draw 9x9 grid
    for x in range(3):
        for y in range(3):
            tile = ttk.Frame(root, width=150, height=150,
                             borderwidth=4, relief='solid')
            tile.grid(row=x, column=y)
            tile.grid_propagate(False)

            for i in range(3):
                for j in range(3):
                    box = Frame(tile, width=50, height=50,
                                bg=DEFAULT_BG, borderwidth=2, relief='solid')
                    box.grid(row=i, column=j)
                    box.grid_propagate(False)

                    row = x * 3 + i
                    col = y * 3 + j
                    value = sudoku_grid[row][col]
                    text = str(value) if value != 0 else ""

                    label = Label(box, text=text, font=('Arial', 14),
                                  bg=DEFAULT_BG, fg="black")
                    label.place(relx=0.5, rely=0.5, anchor='center')
                    cell_labels[(row, col)] = label
                    cell_frames[(row, col)] = box

    # Solve button
    solve_btn = ttk.Button(root, text=" Solve (Hill Climbing)", 
                           command=solve_button)
    solve_btn.grid(row=3, column=0, columnspan=3, pady=10)

    # 10 Puzzle buttons
    puzzle_frame = ttk.Frame(root)
    puzzle_frame.grid(row=4, column=0, columnspan=3, pady=5)

    puzzle_btns = []
    for i in range(1, 11):
        btn = ttk.Button(puzzle_frame, text=f"P{i}", 
                         command=lambda n=i: load_puzzle(n), width=4)
        btn.grid(row=(i-1)//5, column=(i-1)%5, padx=3, pady=2)
        puzzle_btns.append(btn)

    # Status label + Progress bar
    status_label = Label(root, text="Ready", font=('Arial', 10))
    status_label.grid(row=5, column=0, columnspan=3, pady=5)

    progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
    progress_bar.grid(row=6, column=0, columnspan=3, pady=5)

    highlight_conflicts(sudoku_grid)


# Main Entry Point

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--experiment":
        run_experiment()
    else:
        draw_board()
        root.mainloop()