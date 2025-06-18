"""
Question: Simplify Expression by Removing Parentheses

You are given a string that represents a mathematical expression containing lowercase variables and the operators +, -, and *. The expression may contain parentheses.

Your task is to simplify the expression by removing the parentheses and correctly adjusting the operators to preserve the original order of operations and signs.

You should not evaluate the expression numerically — only simplify the expression by removing the parentheses and applying the correct signs.

⸻

Rules to Follow:
	•	Parentheses may change the signs of inner expressions, especially with preceding - operators.
	•	You must apply sign changes properly when removing the parentheses.
	•	Multiplication * is not affected by signs outside parentheses.
	•	There are no nested parentheses.

⸻

Examples:

Example 1:

Input:
(a-(b+c)+d)

Output:
a-b-c+d

Explanation:
	•	Remove parentheses while correctly adjusting the signs of b and c.

⸻

Example 2:

Input:
(p*p) - (a-b)

Output:
p*p-a+b

Explanation:
	•	The subtraction before the second parentheses flips the signs inside.

⸻

Example 3:

Input:
a-(b-c+d)

Output:
a-b+c-d

⸻

Constraints:
	•	The input expression contains only lowercase English letters, +, -, *, and parentheses.
	•	The expression is valid (parentheses are balanced and no syntax errors).
	•	No whitespace will be present in the input.

⸻
"""


def remove_parentheses(expr):
    result = []
    sign_stack = [1]
    sign = 1
    i = 0

    while i < len(expr):
        char = expr[i]

        if char == '+':
            sign = 1
        elif char == '-':
            sign = -1
        elif char == '(':
            # Check operator before '('
            prev = expr[i - 1] if i > 0 else ''
            if prev == '-':
                sign_stack.append(sign_stack[-1] * -1)
            elif prev == '+':
                sign_stack.append(sign_stack[-1])
            elif prev in '*/':
                # preserve parenthesis in * or / cases
                result.append(prev)
                result.append('(')
                sign_stack.append(sign_stack[-1])
            else:
                sign_stack.append(sign_stack[-1])
        elif char == ')':
            prev = expr[i - 1] if i > 0 else ''
            if len(result) >= 2 and result[-1] != ')' and result[-2] in '*/(':
                result.append(')')
            sign_stack.pop()
        elif char in '*/':
            # handled already above if it was before '('
            if i + 1 < len(expr) and expr[i + 1] == '(':
                pass  # defer
            else:
                result.append(char)
        elif char.isalnum():
            if result and result[-1] not in '(*+-/':
                if sign_stack[-1] * sign == 1:
                    result.append('+')
                else:
                    result.append('-')
            elif not result and sign_stack[-1] * sign == -1:
                result.append('-')
            result.append(char)
            sign = 1
        i += 1

    return ''.join(result)


if __name__ == '__main__':
    # string = "(p*p)-(a-b)"
    # print(f"Correct string is - 1 {string} -> {remove_parentheses(string)}" )

    # string = "a-(b-c+d)"
    # print(f"Correct string is -  2 {string} -> {remove_parentheses(string)}")

    # string = "(a-(b+c)+d)"
    # print(f"Correct string is -  3 {string} -> {remove_parentheses(string)}")

    string = "p*(x+y)"
    remove_parentheses(string)
    print(f"Correct string is -  4 {string} expected = a-b+c+d  -> {remove_parentheses(string)}")
#   Expected: a-b+c+d (or similar depending on rule)
# Actual: Wrong result
