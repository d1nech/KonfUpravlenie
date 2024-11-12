import unittest
import json
from main import parse_assignment  # Assuming the main.py script contains parse_assignment

class TestParsing(unittest.TestCase):
    def test_weather_station_parsing(self):
        # Simulating the input lines for the first example (WeatherStation_X)
        input_lines = [
            'def station_id = 101',
            'def station_name = "WeatherStation_X"',
            'def measurement_intervals = ({ ({ 5, 10 }), ({ 15, 30, 45 }) })',
            'def device_settings = dict(light=dict(brightness=100), thermostat=dict(temp_range=({ 16, 30 })), camera=dict(resolution="1080p"))',
            'stop'
        ]
        
        memory = {}
        for line in input_lines:
            if line.strip() == 'stop':
                break
            key, var = parse_assignment(line, memory)
            memory[key] = var
        
        # Expected JSON structure
        expected = {
            "station_id": 101,
            "station_name": "WeatherStation_X",
            "measurement_intervals": [
                [5, 10],
                [15, 30, 45]
            ],
            "device_settings": {
                "light": {"brightness": 100},
                "thermostat": {"temp_range": [16, 30]},
                "camera": {"resolution": "1080p"}
            }
        }
        
        self.assertEqual(memory, expected)

    def test_smart_home_hub_parsing(self):
        # Simulating the input lines for the second example (SmartHomeHub)
        input_lines = [
            'def device_id = 2023',
            'def device_name = "SmartHomeHub"',
            'def supported_devices = ({ ({ "light", "thermostat" }), ({ "camera", "door_lock" }) })',
            'def device_settings = dict(light=dict(brightness=100), thermostat=dict(temp_range=({ 16, 30 })), camera=dict(resolution="1080p"))',
            'stop'
        ]
        
        memory = {}
        for line in input_lines:
            if line.strip() == 'stop':
                break
            key, var = parse_assignment(line, memory)
            memory[key] = var
        
        # Expected JSON structure
        expected = {
            "device_id": 2023,
            "device_name": "SmartHomeHub",
            "supported_devices": [
                ["light", "thermostat"],
                ["camera", "door_lock"]
            ],
            "device_settings": {
                "light": {"brightness": 100},
                "thermostat": {"temp_range": [16, 30]},
                "camera": {"resolution": "1080p"}
            }
        }
        
        self.assertEqual(memory, expected)

if __name__ == '__main__':
    unittest.main()
