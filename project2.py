import re


def check_function_header(code):
    fixed_code = []
    codeCopy = code.copy()
    for line in range(len(codeCopy)):
        codeCopy[line] = codeCopy[line].strip()
        if code[line].startswith("def"):
            match = re.search("def (\w+)\((.*)\):", codeCopy[line])
            # This match is if the function header is correctly formatted
            match2 = re.search("def(\w+)\((.*)\):", codeCopy[line])
            # This match is if the function header does not have a space between
            # the def and function name
            match3 = re.search("def (\w+)\((.*)\:", codeCopy[line])
            # This match is if the function header is missing the closing parentheses
            match4 = re.search("def (\w+)\((.*)\)", codeCopy[line])
            # This match is if the function header is missing the final colon
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
    indentation_level = 0
    fixed_code = []
    in_definition = False
    codeCopy = code.copy()
    for line in range(len(codeCopy)):
        stripped_line = codeCopy[line].strip()
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
            # wasn't reached then it has to be one of the other control structure
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
            if not in_string and not in_comment and line[i:].startswith('print('):  # check for "print(" keyword
                count += 1
                break
        in_comment = False
        # reset flag for in_comment for the next line
    return count


def process_code(code):
    fixed_code = check_function_header(code)
    fixed_code = check_indentation(fixed_code)
    print_count = count_print_statements(fixed_code)
    return fixed_code, print_count


def write_to_file(input_code, output_code, print_count):
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
