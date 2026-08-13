def construct_tape(input=""):
    tape = []

    if input == "":
        tape.append("ε")
        return tape

    for char in input:
        if char == " ":
            tape.append("_")
        else:
            tape.append(char)

    tape.append("ε")

    return tape