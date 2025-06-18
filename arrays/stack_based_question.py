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
            # Determine the new context and push it to the stack
            if i > 0 and expr[i - 1] == '-':
                sign_stack.append(sign_stack[-1] * -1)
            else:
                sign_stack.append(sign_stack[-1])
            sign = 1  # Reset the current sign after entering '('
        elif char == ')':
            sign_stack.pop()
        elif char in '*/':
            result.append(char)
        elif char.isalnum():
            # Prepend sign if needed
            if result and result[-1] not in '(*+-/':
                # Add explicit '+' if needed
                if sign_stack[-1] * sign == 1:
                    result.append('+')
                else:
                    result.append('-')
            elif not result and sign_stack[-1] * sign == -1:
                result.append('-')

            result.append(char)
            sign = 1  # reset after applying
        i += 1

    return ''.join(result)


if __name__ == '__main__':
    # string = "(p*p)-(a-b)"
    # print(f"Correct string is - 1 {string} -> {remove_parentheses(string)}" )

    # string = "a-(b-c+d)"
    # print(f"Correct string is -  2 {string} -> {remove_parentheses(string)}")

    # string = "(a-(b+c)+d)"
    # print(f"Correct string is -  3 {string} -> {remove_parentheses(string)}")

    string = "a-(b-(c+d))"
    remove_parentheses(string)
    print(f"Correct string is -  4 {string} expected = a-b+c+d  -> {remove_parentheses(string)}")
#   Expected: a-b+c+d (or similar depending on rule)
# Actual: Wrong result
