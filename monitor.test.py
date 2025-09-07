import unittest
from unittest.mock import patch
from monitor import (
    vitals_ok, 
    is_temperature_normal, 
    is_pulse_rate_normal, 
    is_spo2_normal,
    check_vital_sign,
    print_alert
)


class MonitorTest(unittest.TestCase):
    
    # Test individual vital sign validators
    def test_temperature_normal_range(self):
        """Test temperature validation for normal range"""
        self.assertTrue(is_temperature_normal(98.6))  # Normal body temp
        self.assertTrue(is_temperature_normal(95))    # Lower boundary
        self.assertTrue(is_temperature_normal(102))   # Upper boundary
        self.assertTrue(is_temperature_normal(100))   # Within range
    
    def test_temperature_out_of_range(self):
        """Test temperature validation for out of range values"""
        self.assertFalse(is_temperature_normal(94.9))  # Below lower boundary
        self.assertFalse(is_temperature_normal(102.1)) # Above upper boundary
        self.assertFalse(is_temperature_normal(80))    # Way below
        self.assertFalse(is_temperature_normal(110))   # Way above
    
    def test_pulse_rate_normal_range(self):
        """Test pulse rate validation for normal range"""
        self.assertTrue(is_pulse_rate_normal(70))   # Normal rate
        self.assertTrue(is_pulse_rate_normal(60))   # Lower boundary
        self.assertTrue(is_pulse_rate_normal(100))  # Upper boundary
        self.assertTrue(is_pulse_rate_normal(85))   # Within range
    
    def test_pulse_rate_out_of_range(self):
        """Test pulse rate validation for out of range values"""
        self.assertFalse(is_pulse_rate_normal(59))   # Below lower boundary
        self.assertFalse(is_pulse_rate_normal(101))  # Above upper boundary
        self.assertFalse(is_pulse_rate_normal(30))   # Way below
        self.assertFalse(is_pulse_rate_normal(150))  # Way above
    
    def test_spo2_normal_range(self):
        """Test SpO2 validation for normal range"""
        self.assertTrue(is_spo2_normal(98))  # Normal level
        self.assertTrue(is_spo2_normal(90))  # Lower boundary
        self.assertTrue(is_spo2_normal(100)) # Maximum level
        self.assertTrue(is_spo2_normal(95))  # Within range
    
    def test_spo2_out_of_range(self):
        """Test SpO2 validation for out of range values"""
        self.assertFalse(is_spo2_normal(89))  # Below lower boundary
        self.assertFalse(is_spo2_normal(85))  # Below range
        self.assertFalse(is_spo2_normal(50))  # Way below
    
    def test_check_vital_sign_function(self):
        """Test the generic vital sign checker"""
        # Test normal case
        is_normal, message = check_vital_sign(98.6, is_temperature_normal, "Temp error")
        self.assertTrue(is_normal)
        self.assertIsNone(message)
        
        # Test error case
        is_normal, message = check_vital_sign(110, is_temperature_normal, "Temp error")
        self.assertFalse(is_normal)
        self.assertEqual(message, "Temp error")
    
    # Test vitals_ok function with mocked print_alert to avoid actual printing during tests
    @patch('monitor.print_alert')
    def test_vitals_ok_all_normal(self, mock_print_alert):
        """Test when all vitals are within normal range"""
        self.assertTrue(vitals_ok(98.6, 70, 98))
        mock_print_alert.assert_not_called()
    
    @patch('monitor.print_alert')
    def test_vitals_ok_temperature_critical_high(self, mock_print_alert):
        """Test when temperature is too high"""
        self.assertFalse(vitals_ok(103, 70, 98))
        mock_print_alert.assert_called_once_with('Temperature critical!')
    
    @patch('monitor.print_alert')
    def test_vitals_ok_temperature_critical_low(self, mock_print_alert):
        """Test when temperature is too low"""
        self.assertFalse(vitals_ok(94, 70, 98))
        mock_print_alert.assert_called_once_with('Temperature critical!')
    
    @patch('monitor.print_alert')
    def test_vitals_ok_pulse_rate_high(self, mock_print_alert):
        """Test when pulse rate is too high"""
        self.assertFalse(vitals_ok(98.6, 101, 98))
        mock_print_alert.assert_called_once_with('Pulse Rate is out of range!')
    
    @patch('monitor.print_alert')
    def test_vitals_ok_pulse_rate_low(self, mock_print_alert):
        """Test when pulse rate is too low"""
        self.assertFalse(vitals_ok(98.6, 59, 98))
        mock_print_alert.assert_called_once_with('Pulse Rate is out of range!')
    
    @patch('monitor.print_alert')
    def test_vitals_ok_spo2_low(self, mock_print_alert):
        """Test when SpO2 is too low"""
        self.assertFalse(vitals_ok(98.6, 70, 89))
        mock_print_alert.assert_called_once_with('Oxygen Saturation out of range!')
    
    @patch('monitor.print_alert')
    def test_vitals_ok_multiple_out_of_range(self, mock_print_alert):
        """Test when multiple vitals are out of range - should return False on first failure"""
        self.assertFalse(vitals_ok(103, 101, 89))
        # Should only call print_alert once (for the first failure - temperature)
        mock_print_alert.assert_called_once_with('Temperature critical!')
    
    # Test boundary values
    @patch('monitor.print_alert')
    def test_vitals_ok_boundary_values_normal(self, mock_print_alert):
        """Test boundary values that should be normal"""
        self.assertTrue(vitals_ok(95, 60, 90))    # All at lower boundaries
        self.assertTrue(vitals_ok(102, 100, 100)) # Temperature and pulse at upper boundaries
        mock_print_alert.assert_not_called()
    
    @patch('monitor.print_alert') 
    def test_vitals_ok_boundary_values_critical(self, mock_print_alert):
        """Test boundary values that should be critical"""
        self.assertFalse(vitals_ok(94.9, 70, 98))  # Temperature just below boundary
        mock_print_alert.assert_called_with('Temperature critical!')
    
    # Test the original test cases for backward compatibility
    @patch('monitor.print_alert')
    def test_not_ok_when_any_vital_out_of_range(self, mock_print_alert):
        """Original test case - updated parameter name"""
        self.assertFalse(vitals_ok(99, 102, 70))
        mock_print_alert.assert_called_once_with('Pulse Rate is out of range!')
    
    @patch('monitor.print_alert')
    def test_ok_when_all_vitals_normal(self, mock_print_alert):
        """Original test case"""
        self.assertTrue(vitals_ok(98.1, 70, 98))
        mock_print_alert.assert_not_called()


# Run the unit tests when this script is executed directly
if __name__ == '__main__':
    unittest.main()
