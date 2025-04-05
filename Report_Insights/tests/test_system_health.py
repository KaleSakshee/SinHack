# tests/test_system_health.py
import unittest
from src.system_health import get_system_health
from src.report_generator import generate_report

class TestSystemHealth(unittest.TestCase):

    def test_get_system_health(self):
        """
        Test that the get_system_health function returns correct data.
        """
        system_health = get_system_health()
        self.assertEqual(system_health['cpu'], 70)
        self.assertEqual(system_health['memory'], 65)
        self.assertEqual(system_health['disk'], 85)

    def test_generate_report(self):
        """
        Test the generate_report function.
        """
        system_health = {
            'cpu': 70,
            'memory': 65,
            'disk': 85
        }
        report = generate_report(system_health)
        self.assertIn("System Health Report:", report)
        self.assertIn("CPU Usage: 70%", report)
        self.assertIn("Memory Usage: 65%", report)
        self.assertIn("Disk Usage: 85%", report)

if __name__ == '__main__':
    unittest.main()
