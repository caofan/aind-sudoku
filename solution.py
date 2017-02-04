assignments = []

def cross(a, b):
    return [s+t for s in a for t in b]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Add in the diagnal units.
diag_units = [[s+t for s,t in zip(r, cols)] for r in (rows, reversed(rows))]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Process naked-twins for each unit.
    for unit in unitlist:
        # Use a dictionary to store the possible twin pairs.
        twos = {}
        for s in unit:
            if len(values[s]) == 2:
                if values[s] not in twos:
                    twos[values[s]] = []
                twos[values[s]].append(s)
        # Find the values for the naked twins
        twin_values = []
        for v in twos:
            if len(twos[v]) == 2:
                twin_values.append(v)
        # Eliminate the naked twins as possibilities for their peers
        for s in unit:
            for v in twin_values:
                if values[s] != v:
                    new_value = values[s]
                    for d in v:
                        new_value = new_value.replace(d, "")
                    values = assign_value(values, s, new_value)

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    for v in grid:
        if v == '.':
            v = '123456789'
        chars.append(v)
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for s in boxes:
        # Eliminate the current value as possibilities from peers when it is set.
        if len(values[s]) == 1:
            for p in peers[s]:
                values = assign_value(values, p, values[p].replace(values[s], ''))
    return values

def only_choice(values):
    for unit in unitlist:
        # Count the occurrences of each digit
        for d in '123456789':
            place = [s for s in unit if d in values[s]]
            # If there is only 1 choice, remove the other possibilities from the square
            if len(place) == 1 and len(values[place[0]]) > 1:
                values = assign_value(values, place[0], d)
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Perform elimination
        values = eliminate(values)
        # Perform only choice strategy
        values = only_choice(values)
        # Use naked twins strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    # Return if all values are set.
    if all(len(values[s])==1 for s in boxes):
        return values
    # Find the square with least possibilities
    n,s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)
    
    # Carry out depth-first search
    for v in values[s]:
        temp = values.copy()
        temp = assign_value(temp, s, v)
        attempt = search(temp)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)




if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
