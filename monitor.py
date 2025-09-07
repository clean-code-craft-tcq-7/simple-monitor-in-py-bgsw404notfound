
from time import sleep
import sys


# Pure functions for vital sign validation
def is_temperature_normal(temperature):
    """Check if temperature is within normal range (95-102°F)"""
    return 95 <= temperature <= 102


def is_pulse_rate_normal(pulse_rate):
    """Check if pulse rate is within normal range (60-100 bpm)"""
    return 60 <= pulse_rate <= 100


def is_spo2_normal(spo2):
    """Check if SpO2 is within normal range (>= 90%)"""
    return spo2 >= 90


def check_vital_sign(value, validator, message):
    """Generic function to check a vital sign and return status with message"""
    if not validator(value):
        return False, message
    return True, None


# I/O function separated from logic
def print_alert(message):
    """Print alert message with blinking effect"""
    print(message)
    for i in range(6):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(1)
        print('\r *', end='')
        sys.stdout.flush()
        sleep(1)


def vitals_ok(temperature, pulse_rate, spo2):
    """
    Check if all vital signs are within normal ranges.
    Returns True if all vitals are normal, False otherwise.
    """
    # Define vital checks with their validators and messages
    vital_checks = [
        (temperature, is_temperature_normal, 'Temperature critical!'),
        (pulse_rate, is_pulse_rate_normal, 'Pulse Rate is out of range!'),
        (spo2, is_spo2_normal, 'Oxygen Saturation out of range!')
    ]
    
    # Check each vital sign
    for value, validator, message in vital_checks:
        is_normal, error_message = check_vital_sign(value, validator, message)
        if not is_normal:
            print_alert(error_message)
            return False
    
    return True
