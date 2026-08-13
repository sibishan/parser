from utils import construct_tape

# test 1: we pass an empty input
input = ""
tape = construct_tape(input)
print("-------\nTest 1\nThe tape should only contain epsilon. Printing tape below...\n", tape)

# test 2: we pass a word as input
input = "sibishan"
tape = construct_tape(input)
print("-------\nTest 2\nThe tape should only contain s,i,b,i,s,h,a,n,ε. Printing tape below...\n", tape)

# test 3: we pass 2 words with space as input
input = "hello world"
tape = construct_tape(input)
print("-------\nTest 3\nThe tape should only contain h,e,l,l,o,_,w,o,r,l,d,ε. Printing tape below...\n", tape)
