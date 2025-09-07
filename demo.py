#!/usr/bin/env python3
"""
Demonstration of the refactored monitor system
"""

from monitor import vitals_ok

def demo_vitals_monitoring():
    """Demonstrate the vitals monitoring system"""
    
    print("=== Vitals Monitoring System Demo ===\n")
    
    # Test cases
    test_cases = [
        (98.6, 70, 98, "Normal vitals"),
        (103, 70, 98, "High temperature"),
        (98.6, 101, 98, "High pulse rate"),
        (98.6, 59, 98, "Low pulse rate"),
        (98.6, 70, 89, "Low oxygen saturation"),
        (94, 101, 85, "Multiple issues")
    ]
    
    for temp, pulse, spo2, description in test_cases:
        print(f"\n--- Testing: {description} ---")
        print(f"Temperature: {temp}°F, Pulse: {pulse} bpm, SpO2: {spo2}%")
        result = vitals_ok(temp, pulse, spo2)
        if result:
            print("✅ All vitals are normal!")
        else:
            print("❌ Vitals are not normal!")
        print("-" * 50)

if __name__ == "__main__":
    demo_vitals_monitoring()
