import pytest
import unittest

from app.calc import Calculator


@pytest.mark.unit
class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.add(2, 2))
        self.assertEqual(0, self.calc.add(2, -2))
        self.assertEqual(0, self.calc.add(-2, 2))
        self.assertEqual(1, self.calc.add(1, 0))
        #añado
        self.assertEqual(-4, self.calc.add(-2, -2)) 
        self.assertEqual(0.3, self.calc.add(0.1, 0.2))
        self.assertEqual(0, self.calc.add(0, 0))
        self.assertEqual(2**30 + 4**50, self.calc.add(2**31, 4**50))

    def test_add_method_returns_correct_result1(self):
        self.assertEqual(6, self.calc.add(3, 3))
        self.assertEqual(0, self.calc.add(2, -2))
        self.assertEqual(0, self.calc.add(-2, 2))
        self.assertEqual(1, self.calc.add(1, 0))      
        
    def test_divide_method_returns_correct_result(self):
        self.assertEqual(1, self.calc.divide(2, 2))
        self.assertEqual(1.5, self.calc.divide(3, 2))
        self.assertRaises(TypeError, self.calc.divide, "2", 2)
        #añado
        self.assertEqual(0, self.calc.divide(0, 5))
        self.assertEqual(0.25, self.calc.divide(1, 4))
        self.assertEqual(-0.5, self.calc.divide(-1, 2))
        self.assertEqual(1, self.calc.divide(1**20, 1**20))
    #añado para arreglar el error de la linea 24 en calc.py
    def test_divide_method_fails_with_zero_division(self):
        with self.assertRaises(TypeError, msg="Division by zero is not possible"):
        self.calc.divide(5, 0)

  
    def test_add_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.add, "2", 2)
        self.assertRaises(TypeError, self.calc.add, 2, "2")
        self.assertRaises(TypeError, self.calc.add, "2", "2")
        self.assertRaises(TypeError, self.calc.add, None, 2)
        self.assertRaises(TypeError, self.calc.add, 2, None)
        self.assertRaises(TypeError, self.calc.add, object(), 2)
        self.assertRaises(TypeError, self.calc.add, 2, object())
    
    def test_divide_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.divide, "2", 2)
        self.assertRaises(TypeError, self.calc.divide, 2, "2")
        self.assertRaises(TypeError, self.calc.divide, "2", "2")

    def test_multiply_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.multiply(2, 2))
        self.assertEqual(0, self.calc.multiply(1, 0))
        self.assertEqual(0, self.calc.multiply(-1, 0))
        self.assertEqual(-2, self.calc.multiply(-1, 2))
        self.assertRaises(TypeError, self.calc.multiply, "0", 0)
        
    def test_power_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.power(2, 2))
        self.assertEqual(1, self.calc.power(1, 0))
        self.assertEqual(1, self.calc.power(-1, 0))
        self.assertEqual(-27, self.calc.power(-3, 3))
        self.assertRaises(TypeError, self.calc.power, "0", 0)
        
    def test_substract_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.substract(10, 6))
        self.assertEqual(-2, self.calc.substract(256, 258))
        self.assertEqual(-1, self.calc.substract(-1, 0))
        self.assertEqual(0, self.calc.substract(0, 0))
        self.assertEqual(0, self.calc.substract(0, 0))
        self.assertRaises(TypeError, self.calc.substract, "0", 0)
        
if __name__ == "__main__":  # pragma: no cover
    unittest.main()
