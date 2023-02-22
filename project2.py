# -*- coding: utf-8 -*-
"""project2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IvIc6xYtU-xciQEjAVJiXAxZyaqRu2GO
"""

import re

def check_indentation(code):
    indentation_level = 0
    fixed_code = []
    in_definition = False
    for line in range(len(code)):
        stripped_line = code[line].strip()
        if stripped_line.startswith("def"):
            in_definition = True
            fixed_line = " " * (indentation_level * 4) + stripped_line + "\n"
            fixed_code.append(fixed_line)
            indentation_level += 1
        elif stripped_line.endswith(":"):
            fixed_line = " " * (indentation_level * 4) + stripped_line + "\n"
            fixed_code.append(fixed_line)
            indentation_level += 1
        elif stripped_line.startswith("return"):
            indentation_level = 1
            fixed_line = " " * (indentation_level * 4) + stripped_line + "\n"
            fixed_code.append(fixed_line)
            in_definition = False
        else:
            fixed_line = " " * (indentation_level * 4) + stripped_line + "\n"
            fixed_code.append(fixed_line)
            if in_definition:
                indentation_level = 1
            else:
                indentation_level = 0
    return "".join(fixed_code)

def check_function_header(code):
    fixed_code = []
    for line in range(len(code)):
        if code[line].startswith("def"):
            match = re.search("def (\w+)\((.*)\):", code[line])
            if match:
                function_name = match.group(1)
                arguments = match.group(2)
                fixed_line = f"def {function_name}({arguments}):"
                fixed_code.append(fixed_line)
        else:
            fixed_code.append(code[line])
    return "".join(fixed_code)

def count_print_keyword(code):
    # Remove comments and strings to avoid counting `print()` within them
    code = re.sub(r'(\".*?\"|\'.*?\')|(#.*)', '', code, flags=re.DOTALL)

    # Split the code into lines
    lines = code.split('\n')

    # Count the number of times `print()` is called
    count = 0
    for line in lines:
        if 'print(' in line and not 'print(' in line.split('print(')[-1]:
            count += 1

    return count

def process_code(code):
    fixed_code = check_indentation(code)
    fixed_code = check_function_header(fixed_code)
    print_count = count_print_keyword(fixed_code)
    return fixed_code, print_count

def write_to_file(input_code, output_code, print_count):
    with open("output.txt", "w") as f:
        f.write("Original code:\n")
        f.write(input_code)
        f.write("\n\n")
        f.write("-----------------------------------------------------"
                "-----------------------\nUpdated code:\n\n")
        f.write(output_code)
        f.write("\n\n")
        f.write(f"The keyword 'print' was used {print_count} times.")

if __name__ == "__main__":
    codef = open("test.py", "r")
    code = codef.readlines()
    fixed_code, print_count = process_code(code)
    write_to_file("".join(code), fixed_code, print_count)
    print("Processing complete. Check 'output.txt' for the results.")