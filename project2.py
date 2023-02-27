import re


def check_function_header(code):
    """function takes in a list of strings code,iterates through
    each string in the list, and checks whether the string begins
    with the keyword 'def'. If it does, it attempts to parse the
    function header using regular expressions to ensure that it is
    correctly formatted with the function name and arguments
    surrounded by parentheses and followed by a colon. If the
    function header is correctly formatted, the string is added to
    a list of strings fixed_code. If the header is not correctly
    formatted, the function attempts to parse it using one of several
    regular expressions for common errors. If the header can be parsed,
    the correctly formatted header is added to fixed_code. Otherwise,
    the original line is added unaltered. The function returns a list
    of strings fixed_code."""

    fixed_code = []
    for line in range(len(code)):
        codeStripped = code[line].strip()
        if code[line].startswith("def"):
            match = re.search(r"def (\w+)\((.*)\):", codeStripped)
            match2 = re.search(r"def(\w+)\((.*)\):", codeStripped)
            match3 = re.search(r"def (\w+)\((.*)\:", codeStripped)
            match4 = re.search(r"def (\w+)\((.*)\)", codeStripped)
            if match:
                function_name = match.group(1)
                arguments = match.group(2)
                fixed_line = f"def {function_name}({arguments}):"
                fixed_code.append(fixed_line)
            elif match2:
                function_name = match2.group(1)
                arguments = match2.group(2)
                fixed_line = f"def {function_name}({arguments}):"
                fixed_code.append(fixed_line)
            elif match3:
                function_name = match3.group(1)
                arguments = match3.group(2)
                fixed_line = f"def {function_name}({arguments}):"
                fixed_code.append(fixed_line)
            elif match4:
                function_name = match4.group(1)
                arguments = match4.group(2)
                fixed_line = f"def {function_name}({arguments}):"
                fixed_code.append(fixed_line)
            # Same body but different conditional since we have to
            # account for all the different wrong header cases
        else:
            fixed_code.append(code[line])
            # puts it into the form of a list
    return fixed_code
    # Returns a list so that check_indentation() can properly run


def check_indentation(code):
    """function takes in a list of strings code, iterates through
    each string in the list, and checks the indentation level of
    each line. If the line begins with the keyword 'def', the
    function assumes that everything that follows belongs to the
    definition and increments the indentation level by one. If the
    line ends with a colon or begins with certain control structures
    (e.g., 'if', 'else', 'elif'), the function adds the line to the
    list fixed_code with an appropriate number of tabs added to the
    beginning to indicate the correct indentation level. If the line
    is blank, the function resets the indentation level to zero.
    Otherwise, the function adds the line to fixed_code with the
    appropriate number of tabs based on the current indentation level.
    The function returns a string of all lines in fixed_code concatenated
    together."""

    indentation_level = 0
    fixed_code = []
    in_definition = False
    for line in range(len(code)):
        stripped_line = code[line].strip()
        if stripped_line.startswith("def "):
            in_definition = True
            # boolean that tells us we are in a definition
            fixed_line = stripped_line + "\n"
            fixed_code.append(fixed_line)
            indentation_level += 1
            # Increase indentation level since everything inside
            # the definition needs to be indented at least once
        elif stripped_line.endswith(":") or stripped_line.startswith("if") \
            or stripped_line.startswith("else") or \
                stripped_line.startswith("elif"):
            # if the line ends with : and the first if statement
            # wasn't reached then it has to be another control structure
            # so we need to add it in with and indentation
            fixed_line = "\t" * indentation_level + stripped_line + "\n"
            fixed_code.append(fixed_line)
            indentation_level += 1
            # increment since the following line for a control structure
            # needs to be indented
        elif stripped_line == "":
            indentation_level = 0
            fixed_line = "\n"
            fixed_code.append(fixed_line)
            # blank line indicates space between defs since we were told defs
            # won't have blank lines within them we can safely assume that we
            # are outside the function
        else:
            fixed_line = "\t" * indentation_level + stripped_line + "\n"
            fixed_code.append(fixed_line)
            if in_definition:
                indentation_level = 1
                # inside the definition this has to be at least 1
            else:
                indentation_level = 0
                # Outside the definition we reset the indentation level
    return "".join(fixed_code)
    # This returns a string so that count_print_statements() can properly run


def count_print_statements(code):
    """function takes in a string code, splits it into lines,
    and iterates through each line to count the number of times
    the keyword 'print' is used outside of a comment or a string
    literal. The function maintains a flag in_string to track
    whether the current character is inside a string literal and
    a flag in_comment to track whether the current line is inside
    a comment. If the current line is empty or a comment, the function
    skips it. If the current line is inside a comment, the function
    sets the in_comment flag to true and skips the rest of the line.
    If the current character is the start or end of a string literal,
    the function toggles the in_string flag. If the current character
    is not inside a string literal or a comment and the string 'print('
    is found, the function increments a counter count. The function
    returns the final count."""

    count = 0
    in_string = False
    in_comment = False
    for line in code.splitlines():
        line = line.strip()
        if not line:
            # skip empty lines
            continue
        if line.startswith('#'):
            # skip comment lines
            continue
        for i in range(len(line)):
            if line[i:i+3] == '"""' or line[i:i+3] == "'''":
                # check for docstrings
                in_string = not in_string
                # toggle flag for in_string
            if not in_string and line[i:i+1] == '#':
                # check for comment
                in_comment = True
                break
            if not in_string and not in_comment and \
                    line[i:].startswith('print('):  # check "print(" keyword
                count += 1
                break
        in_comment = False
        # reset flag for in_comment for the next line
    return count


def process_code(code):
    """The process_code() function takes in a string code, runs it
    through check_function_header(), check_indentation(), and
    count_print_statements(), and returns the updated code as a string
    and the count of 'print' statements as an integer."""

    fixed_code = check_function_header(code)
    fixed_code = check_indentation(fixed_code)
    print_count = count_print_statements(fixed_code)
    return fixed_code, print_count


def write_to_file(input_code, output_code, print_count):
    """The write_to_file() function takes in the original string
    input_code, the updated string output_code, and the count of
    'print' statements print_count, and writes them to a file
    'output.txt'. The function first writes the original code to
    the file, then a separator, then the updated code, and finally
    the count of 'print' statements."""

    with open("output.txt", "w") as f:
        f.write("Original code:\n")
        f.writelines(input_code)
        f.write("\n\n")
        f.write("-----------------------------------------------------"
                "-----------------------\nUpdated code:\n\n")
        f.write(output_code)
        f.write("\n\n")
        f.write(f"The keyword 'print' was used {print_count} times.")


if __name__ == "__main__":
    codef = open("testExamples.py", "r", encoding='utf-8')
    code = codef.readlines()
    fixed_code, print_count = process_code(code)
    write_to_file(code, fixed_code, print_count)
    print("Processing complete. Check 'output.txt' for the results.")
