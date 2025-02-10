

# prints the matrix as it's stored, as a 2d array
def printMatrixArray(matrix):
    for row in range(len(matrix)):
        print(matrix[row])

# prints the matrix without a grid
def printMatrix(matrix, withDiags):
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            value = matrix[row][col]
            if (value == '•' and withDiags):
                value = '\\'
            # The spaces are very important for lining up the columns with their dots
            if (value == 0):
                if(row != 0 and col != 0):
                    print(" ", end='')
                else:
                    print("   ", end='')
            else:
                print(value, " ", end='')
        print("")
        
def printMatrixWithSquares(matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            value = matrix[row][col]
            if (value == '•'):
                value = '|||'
            # The spaces are very important for lining up the columns with their squares
            if (value == 0):
                if(row != 0 and col != 0):
                    print("   ", end='')
                else:
                    print("   ", end='')
            else:
                if (value != "|||"):
                    if (col == 0):
                        print(value, "", end='')
                    else:
                        print(value, " ", end='')
                else:
                    print(value, end='')
        print("")
        
# prints the matrix with a grid
def printMatrixGrid(matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            value = matrix[row][col]
            # The spaces are very important for lining up the grid's columns
            if (value == 0): # Only a value of 0 in the top left corner
                print("  | ", end='')
            else:
                print(value, " | ", sep='', end='')
        # newline for the row separators to be printed on
        print("")
        if row < len(matrix) - 1:
            for i in range(len(matrix[row])):
                print("----", end='')
        print("")
        
# fills the matrix with empty spots to later be filled with dots
def clearMatrix(matrix, seqX, seqY):
    for nucleotideIndexX in range(len(seqX)):
        matrix[0][nucleotideIndexX + 1] = seqX[nucleotideIndexX] # set the first row (offset by one from the left) to be the value of each nucleotide for the x sequence
        for rowIndex in range(1, len(seqY) + 1): # set each value in the current column (since the x sequence stores a nucleotide in each column) to be blank
            matrix[rowIndex][nucleotideIndexX + 1] = ' '
    for nucleotideIndexY in range(len(seqY)):
        matrix[nucleotideIndexY + 1][0] = seqY[nucleotideIndexY] # sets the first column (offset by 1 from the top) to be the value of each nucleotide for the y sequence
    
#TODO fix this
def checkWindow(matrix, windowSize, mismatchLimit, row, col):
    buffer = windowSize // 2
    mismatches = 0
    colI = col - buffer # The column index of the respective pair that fits along the diagonal with the current row index within the specified window
    for rowI in range(row - buffer, row + buffer + 1):
        if (matrix[rowI][0] != matrix[0][colI]): 
            mismatches += 1
            if (mismatches > mismatchLimit):
                return ' '
        colI += 1 # Iterate the column index by 1 to move along the diagonal horizontally, as the row index increases by 1 to move along the diagonal vertically
    return '•'
    
    
# If the first sequence inputted goes on the x axis
SEQ1_IS_X = True 
# If a window is used to limit noise
WINDOW = True 

print
print("Please enter sequence 1") #CCATCGCCATCGCATTCGGAGTAG (example)
seq1 = input()
print("Please enter sequence 2") #GCATCGGCGCATCGCTTCTGAG (example)
seq2 = input()

# Makes sure the matrix axis are correct based off which sequence goes where
if (SEQ1_IS_X):
    cols = len(seq1)
    rows = len(seq2)
else:
    rows = len(seq1)
    cols = len(seq2)
    
matrix = [[0 for i in range(cols + 1)] for j in range(rows + 1)] # create a 2d matrix of the proper dimensions

if (SEQ1_IS_X): # put the first sequence on the correct axis
    clearMatrix(matrix, seq1, seq2)
else:
    clearMatrix(matrix, seq2, seq1)


if (WINDOW == False):
    for row in range(1, len(matrix)): # to offset the label column
        for col in range(1, len(matrix[row])): # to offset the label row
            if matrix[0][col] == matrix[row][0]: # matching nucleotides receive a dot in their respective location on the matrix
                matrix[row][col] = '•'
else:
    mismatchLimit = ''
    windowSize = ''
    stringency = ''
    notEnterParams = True # loops until the user enters accurate parameters
    while(notEnterParams):
        errored = False
        print("Please input window size, stringency, and mismatch limit. Please enter numbers for 2 of the 3 values.")
        print("Windows size: ", end='')
        windowSize = input()
        print("Stringency: ", end='')
        stringency = input()
        if (not windowSize.isdigit or not stringency.isdigit):
            print("Mismatch limit: ", end='')
            mismatchLimit = input()
            if (not mismatchLimit.isdigit):
                print("Error: You must specify at least 3 of the 3 values. Please try again.")
                errored = True
            if (windowSize == ''):
                windowSize = int(mismatchLimit) + int(stringency)
            elif (stringency == ''):
                stringency = int(windowSize) - int(mismatchLimit)
        else:
            mismatchLimit = int(windowSize) - int(stringency)
            print("Mismatch limit:", mismatchLimit)
        stringency = int(stringency)
        mismatchLimit =int(mismatchLimit)
        windowSize =int(windowSize)
        if (windowSize < stringency or windowSize < mismatchLimit):
            print("Error: Window Size must be greater than or equal to both the Stringency and Mismatch Limit")
            errored = True
        elif(mismatchLimit != windowSize - stringency):
            print("Error: Mismatch Limit must be equal to the Window Size - Stringency")
            errored = True
        elif(windowSize > min(len(seq1), len(seq2))):
            print("Error: Windows Size must be less than or equal to the length of the shorter of the two entered sequences")
            errored = True
        elif(windowSize % 2 == 0):
            print("Error: Unfortunately this program only supports odd window sizes at the moment. Please input one as such.")
            errored = True
        print("") # newline
        if (not errored):
            notEnterParams = False
    buffer = windowSize // 2
    for row in range(1 + buffer, len(matrix) - buffer): # to offset the label column, and only check values that can fit the full window around them.
        for col in range(1 + buffer, len(matrix[row]) - buffer): # to offset the label row, and only check values that can fit the full window around them.
            matrix[row][col] = checkWindow(matrix, windowSize, mismatchLimit, row, col)
    
    
print("Would you like the matrix to be displayed with a grid with dots (1), with diagonals with no grid (2), with dots with no grid (3), or with filled-in squares(4)? Please enter the respective number: ", end='')
printStyle = int(input())
print() # newline
match printStyle:
    case 1:
        printMatrixGrid(matrix)
    case 2:
        printMatrix(matrix, True)
    case 3:
        printMatrix(matrix, False)       
    case 4:
        printMatrixWithSquares(matrix)
    case _:
        print("Non-valid input entered, using default \"Filled in Squares\"")
        printMatrixWithSquares(matrix)
