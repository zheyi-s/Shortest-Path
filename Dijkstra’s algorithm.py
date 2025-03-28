import heapq

# Create a grid and set up obstacles
def create_grid_with_obstacle(size=100):
    # Initialize the grid, all positions default to 0 (passable)
    grid = [[0 for _ in range(size)] for _ in range(size)]

    while True:
        # Prompt user to input obstacle position and size
        print("Please enter the starting coordinates and size of the obstacle:")
        try:
            obstacle_x_start = int(input(f"Obstacle starting x coordinate (0-{size - 1}): "))  # Top-left x coordinate
            obstacle_y_start = int(input(f"Obstacle starting y coordinate (0-{size - 1}): "))  # Top-left y coordinate
            obstacle_width = int(input("Obstacle width (1-remaining space): "))  # Obstacle width
            obstacle_height = int(input("Obstacle height (1-remaining space): "))  # Obstacle height

            # Validate if the obstacle fits within the grid and has a reasonable size
            if (obstacle_x_start < 0 or obstacle_y_start < 0 or
                    obstacle_x_start + obstacle_width > size or
                    obstacle_y_start + obstacle_height > size or
                    obstacle_width <= 0 or obstacle_height <= 0):
                print(
                    f"Obstacle coordinates or size invalid! Ensure coordinates are between 0-{size - 1}, and width/height are greater than 0 and fit within the remaining space.")
                continue  # Invalid input, loop back to re-prompt
            else:
                break  # Valid input, exit the loop
        except ValueError:
            print("Invalid input! Please enter valid integers.")
            continue  # Non-integer input, loop back to re-prompt

    # Mark the obstacle area in the grid as 1
    for i in range(obstacle_y_start, obstacle_y_start + obstacle_height):
        for j in range(obstacle_x_start, obstacle_x_start + obstacle_width):
            grid[i][j] = 1

    return grid


# Get neighboring nodes (up, down, left, right)
def get_neighbors(node, grid):
    x, y = node  # Unpack the x and y coordinates of the current node
    size = len(grid)  # Grid size
    neighbors = []  # Store neighbor nodes

    # Define four movement directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy  # Calculate new coordinates
        # Check if the new coordinates are within the grid and not an obstacle
        if (0 <= new_x < size and 0 <= new_y < size and grid[new_x][new_y] != 1):
            neighbors.append((new_x, new_y))

    return neighbors


# Dijkstra's algorithm to compute the shortest path
def dijkstra(grid, start, goal):
    size = len(grid)
    # Initialize distances to all nodes as infinity
    distances = {(i, j): float('inf') for i in range(size) for j in range(size)}
    distances[start] = 0  # Distance to start is 0
    previous = {}  # Store the previous node for path reconstruction
    pq = [(0, start)]  # Priority queue storing (distance, node), initialized with start
    visited = set()  # Set of visited nodes

    while pq:  # Continue while the queue is not empty
        current_distance, current = heapq.heappop(pq)  # Pop the node with the smallest distance

        if current in visited:  # Skip if already visited
            continue

        visited.add(current)  # Mark as visited

        if current == goal:  # Reached the goal, stop
            break

        # Check all neighbors of the current node
        for neighbor in get_neighbors(current, grid):
            if neighbor in visited:  # Skip visited neighbors
                continue

            distance = current_distance + 1

            if distance < distances[neighbor]:  # If a shorter path is found
                distances[neighbor] = distance  # Update distance
                previous[neighbor] = current  # Record predecessor
                heapq.heappush(pq, (distance, neighbor))  # Add to queue

    # Reconstruct the path
    path = []
    current = goal
    while current in previous:  # Backtrack from goal to start
        path.append(current)
        current = previous[current]
    path.append(start)  # Add the start node
    return path[::-1]  # Reverse path to go from start to goal


# Print the grid
def print_grid_and_path(grid, path, start, goal):
    size = len(grid)
    # Create a display grid, initially all '.' (empty space)
    display_grid = [['.' for _ in range(size)] for _ in range(size)]

    # Mark obstacles as '#'
    for i in range(size):
        for j in range(size):
            if grid[i][j] == 1:
                display_grid[i][j] = '#'

    # Mark the path as '*'
    for x, y in path:
        display_grid[x][y] = '*'

    # Mark start as 'S' and goal as 'G'
    display_grid[start[0]][start[1]] = 'S'
    display_grid[goal[0]][goal[1]] = 'G'

    # Print the grid
    print("Grid and path representation (S=Start, G=Goal, *=Path, #=Obstacle, .=Empty):")
    for row in display_grid:
        print(' '.join(row))

    # Print path details
    if path:
        print(f"\nPath length: {len(path) - 1}")  # Path length is number of nodes minus 1
    else:
        print("\nNo path found!")


# Get user input for coordinates
def get_user_input(size, prompt):
    while True:
        try:
            x = int(input(f"{prompt} x coordinate (0-{size - 1}): "))
            y = int(input(f"{prompt} y coordinate (0-{size - 1}): "))
            if 0 <= x < size and 0 <= y < size:
                return (y, x)
            else:
                print(f"Coordinates must be between 0 and {size - 1}, please try again!")
        except ValueError:
            print("Please enter valid integers!")


# Main program
def main():
    size = 100  # The default grid size is 100*100
    grid = create_grid_with_obstacle(size)  # Create grid with obstacles

    # Get start and goal coordinates
    print("\nPlease enter the start coordinates:")
    start = get_user_input(size, "Start")
    print("Please enter the goal coordinates:")
    goal = get_user_input(size, "Goal")

    # Check if start or goal is on an obstacle
    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
        print("Start or goal is on an obstacle, please choose different coordinates!")
        return

    # Compute and display the shortest path
    path = dijkstra(grid, start, goal)
    print_grid_and_path(grid, path, start, goal)


if __name__ == "__main__":
    main()  # Program entry point