assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

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

    # Find all instances of naked twins
    
    for units in unitlist:

       #One set of doubledigits for each units
        doubledigits = {}
        for unit in units:
            if len(values[unit]) == 2:
                doubledigits.setdefault(values[unit],[]).append(unit)
            
        #Check if there are naked twins in unit
        naked_twins = { d: boxes for d,boxes in doubledigits.items() if doubledigits if len(boxes) == 2} 
        for digits, twins in naked_twins.items():
            
            #remove the twin boxes from the units list
            peers = { unit for unit in units if unit not in twins }
            #for each peer, remove each digit in it
            for peer in peers:
                for digit in digits:
                    values = removeDigitFromBox(values,peer,digit)

    return values

def removeDigitFromBox(values,box,digitToRemove):
    current_box_value = values[box]
    #Remove digit
    current_box_value = current_box_value.replace(digitToRemove,'')
    #replace box value
    values = assign_value(values,box,current_box_value)
    return values

def cross(A, B):
    return [r + c for r in A for c in B]

def times(inp):
    rows,cols = inp
    return [a + b for a,b in zip(rows,cols)]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [ times(x) for x in [(rows,cols),(rows[::-1],cols)] ]

unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


#print("units",units)

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
    return { i: j if j != '.' else '123456789' for i,j in zip(boxes,grid) }

def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    completed_keys = [ key for key,val in values.items() if len(val) == 1 ] 
    for key in completed_keys:
        digit = values[key]
        #peer = peers[key]
        for peer in peers[key]:
            #print('peer for ',key,peer)
            current_box_value = values[peer]
            current_box_value = current_box_value.replace(digit,'')
            assign_value(values,peer,current_box_value)
            #values[peer] = values[peer].replace(digit,'')
    
    return values

def only_choice(values):
    for idx, units in enumerate(unitlist):
        for i in '123456789':
           # print("number",i)
            digits_in_boxes = []
            for box in units:
                #print("box : ",box)
                if i in values[box]:
                    digits_in_boxes.append(box)
            #print("{0} found in boxes: {1}".format(i,digits_in_boxes))
            if len(digits_in_boxes) == 1:
                #This digit can only be in this box, set box value to that digit
                assign_value(values,digits_in_boxes[0],i)
#                values[digits_in_boxes[0]] = i
            

            
    return values

def reduce_puzzle(values):
    
    stalled = False
    while not stalled:
        #keep track of number of solved boxes for an exist loop criteria
        num_solved_boxes_before = len([ box for box in values if len(values[box]) == 1])
        
#        print("num solved boxes before:", num_solved_boxes_before)
        
        #1st step eliminate
        values = eliminate(values)
        
#        print("Eliminate step completed")
        #2nd step run only_choice on values
        values = only_choice(values)
        #print("values after eliminate", values)
#        print("Only choice step completed")


        #implement naked twins
        values = naked_twins(values)
        
        num_solved_boxes_after = len([ box for box in values if len(values[box]) == 1])
#        print("Num solved boxes after:", num_solved_boxes_after)
        
        stalled = num_solved_boxes_before == num_solved_boxes_after 
    
        #Check for failed game
        if len([ box for box in values if len(values[box]) == 0 ]):
            #Failed solving puzzle, show puzzle
            print("Failed to solve puzzle in this attempt : ")
            display(values)
            return False
    
    return values

def search(values):
    
    #this function returns *ONLY* when it failed, or when the puzzle is solved (returns the dic of the solved puzzle)
    #It never returns when the puzzle have not been solved, but not failed yet
    #The recursive function below goes depth-first into all search trees, and only returns back up the bubble when 
    #the solution is found. Otherwise, it will move on to the next leaf (and not returning anything)
    
    
    #Values structure
    # { A1: '123',
#       A2: '234',
#       A3: '1276' .... }
#    
    
    values = reduce_puzzle(values)
    if not values:
        #puzzle Failed
#        print("Puzzle Failed")
        
        return False
    
    #Check if all boxes have only 1 value, if true, puzzle is solved
    #This is the exit criteria if successful!
    if (all([ len(values[box]) == 1 for box in values])):
        print("Puzzle solved!")
        return values
    
    
    
#    print("Puzzle still not yet solved")
#    print("Number of unsolved boxes:", len([ box for box in values if len(values[box]) != 1 ]))

    
    #implement depth-first-search if puzzle is still not solved
    #select the box with the smallest possibilities first
    m,b = min(((len(values[box]),box) for box in values if len(values[box]) > 1 ))
#    print("box with smallest number of possibilities m:", m,"| b:",b)    
    
    #For each possibility in m, create a new sub-puzzle and try to solve it
    for guess in values[b]:
        sub_sudoku = values.copy()
        
        #assign guess to new sudoku
        sub_sudoku[b] = guess
        
        
        
        print("Attempting to solve sub_sudoku puzzle by using ",guess, " in ", b)
        display(sub_sudoku)
        attempt = search(sub_sudoku)
        
#        print("Attempt ",guess, attempt)

        
        #Do not really understand this part. Seems like a recursive call but I'm getting confused trying to trace the flow
        #Can someone please describe what is happening here?
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
    values = search(values)
    
    
    
    
    return values

if __name__ == '__main__':
    
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
#    diag_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
