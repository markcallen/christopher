"""A mathematical expression evaluation server that provides safe calculation capabilities.

This module implements a server that can safely evaluate mathematical expressions
using Python's ast module, avoiding the security risks of eval().
"""  # noqa: E501

import ast
import operator


class MathServer:
    """A server that handles mathematical expression evaluation.

    This server provides a safe way to evaluate mathematical expressions
    using Python's ast module instead of eval() for security.
    """

    id: str = "math"

    # Define supported operators
    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def _safe_eval(self, node: ast.AST) -> float:
        """Safely evaluate an AST node.

        Args:
        ----
            node: The AST node to evaluate

        Returns:
        -------
            The evaluated result as a float

        Raises:
        ------
            ValueError: If the expression contains unsupported operations
            TypeError: If the expression contains complex numbers

        """
        if isinstance(node, ast.Constant):
            if isinstance(node.value, complex):
                raise TypeError("Complex numbers are not supported")
            return float(node.value)
        elif isinstance(node, ast.BinOp):
            left = self._safe_eval(node.left)
            right = self._safe_eval(node.right)
            op_type = type(node.op)
            if op_type not in self._operators:
                raise ValueError(f"Unsupported operation: {op_type.__name__}")
            return self._operators[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._safe_eval(node.operand)
            op_type = type(node.op)
            if op_type not in self._operators:
                raise ValueError(f"Unsupported operation: {op_type.__name__}")
            return self._operators[op_type](operand)
        else:
            raise ValueError(f"Unsupported node type: {type(node).__name__}")

    async def send_request(self, input_text: str) -> str:
        """Process a mathematical expression and return the result.

        Args:
        ----
            input_text: A string containing a mathematical expression

        Returns:
        -------
            A string containing either the result or an error message

        """
        try:
            # Parse the input into an AST
            tree = ast.parse(input_text, mode="eval")
            # Evaluate the expression safely
            result = self._safe_eval(tree.body)
            return f"Result: {result}"
        except (ValueError, SyntaxError, TypeError) as e:
            return f"Error evaluating expression: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
