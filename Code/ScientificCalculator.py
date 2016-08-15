from Code.Calculator import Calculator
import re

class ScientificCalculator(Calculator):
    """Clase que describe una calculadora científica que extiende las capacidades
    de la calculadora normal.
    """
    def __init__(self):
        super(ScientificCalculator, self).__init__()

    def multiplication(self, arg1, arg2):
        """Multiplica los dos argumentos que recibe"""
        return arg1*arg2

    def division(self, arg1, arg2):
        """Divide los dos argumentos que recibe"""
        return arg1/arg2
    
    def modulo(self, arg1, arg2):
        """Devuelve el primer argumento módulo el segundo"""
        return arg1%arg2
    
    def exponentiation(self, arg1, arg2):
        """Devuelve el primer argumento elevado a la potencia segundo argumento"""
        return arg1**arg2
        
    def evaluate(self, entry_string):
        """Primero trata de evaluar en caso de que sea una operacion básica.
        Si no, ya trabaja.
        """
        result = self.basicEval(entry_string)
        if result is None:
            (operator,nums) = self.parse(entry_string)
            if operator == '*':
                return self.multiplication(float(nums[0]),float(nums[1]))
            elif operator == '/':
                return self.division(float(nums[0]),float(nums[1]))
            elif operator == '%':
                return self.modulo(float(nums[0]),float(nums[1]))
            elif operator == '^':
                return self.exponentiation(float(nums[0]),float(nums[1]))
            return None
        return result

    def parse(self, entry_string):
        """Analiza la cadena de entrada para separar en tokens."""
        op = re.compile('[*/%^]')
        operation = op.search(entry_string)
        if operation is not None:
            operator = operation.group(0)
            nums = re.split('\\'+ operator, entry_string)
            return (operator, nums)
        return None

    def basicEval(self, entry_string):
        """Método heredado"""
        return super(ScientificCalculator,self).basicEval(entry_string)
