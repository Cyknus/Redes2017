import re

class Calculator(object):
    """Clase que describe una calculadora básica, solo suma y resta."""
    def __init__(self):
        super(Calculator, self).__init__()

    def addition(self, arg1, arg2):
        """Suma el primer argumento con el segundo"""
        return arg1+arg2

    def difference(self, arg1, arg2):
        """Resta el segundo argumento del primero"""
        return arg1-arg2

    def basicParse(self, entry_string):
        """Divide la expresión en tokens. Solo acepta operadores binarios."""
        op = re.compile('[+\-]')
        operation = op.search(entry_string)
        if operation is not None:
            operator = operation.group(0)
            nums = re.split('\\'+ operator, entry_string)
            return (operator, nums)
        return None

    def basicEval(self, entry_string):
        """Evalúa la expresión recibida en tokens."""
        res = self.basicParse(entry_string)
        if res is None:
            return None
        (operator, nums) = res
        if operator == '+':
            return self.addition(float(nums[0]), float(nums[1]))
        if operator == '-':
            return self.difference(float(nums[0]), float(nums[1]))
        return None