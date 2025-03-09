.data
    # The array to be sorted (6 elements).
base:   .word 3 2 4 6 9 8

.text
    # Initialize constant N = 6 in X13 and outer loop index (X4 = 0)
    ADDI X13 X0 6       # X13 = number of elements (N)
    ADDI X4 X0 0        # X4 = outer loop index = 0

OUTER_LOOP:
    # Outer loop runs while X4 <= (N - 2)
    ADDI X11 X13 -2     # X11 = N - 2
    BLT X4 X11 INNER_LOOP_START   # if X4 <= (N-2) then do inner loop
    J DONE              # Otherwise, sorting is complete

INNER_LOOP_START:
    # Set up inner loop
    ADDI X5 X0 0        # X5 = inner loop counter j = 0
    ADDI X7 X0 0        # X7 = base pointer for the array (assumed at address 0)
    ADDI X8 X7 0        # X8 = pointer used for inner loop iteration
    # Compute inner loop limit: inner iterations = (N - outer - 1)
    # To get a strict inequality with BLT (which branches when <=),
    # we compute: limit = (N - outer - 1) - 1 = N - outer - 2.
    SUB X12 X13 X4      # X12 = N - outer
    ADDI X12 X12 -2     # X12 = N - outer - 2

INNER_LOOP:
    BLT X5 X12 INNER_LOOP_BODY  # if j <= (limit) then do inner loop body
    J END_INNER_LOOP            # otherwise, end this inner loop pass

INNER_LOOP_BODY:
    LW X9 0(X8)         # Load A[j] into X9
    LW X10 4(X8)        # Load A[j+1] into X10
    # If the next element is less than the current, swap them.
    BLT X10 X9 SWAP     # (BLT branches if X10 <= X9)
    J NO_SWAP

SWAP:
    ADD X3 X9 X0       # X3 = A[j] (save original A[j])
    ADD X9 X10 X0      # X9 = A[j+1]
    ADD X10 X3 X0      # X10 = original A[j]
    SW X9 0(X8)        # Store swapped value into A[j]
    SW X10 4(X8)       # Store swapped value into A[j+1]

NO_SWAP:
    ADDI X5 X5 1       # j = j + 1
    ADDI X8 X8 4       # Increment pointer by 4 bytes to next element
    J INNER_LOOP

END_INNER_LOOP:
    ADDI X4 X4 1       # outer = outer + 1
    J OUTER_LOOP

DONE:
    # Sorting complete. (You can add a halt or a dummy instruction.)
    ADD X0 X0 X0