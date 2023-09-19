import unittest
import json
from plot_data import parseMainForecastJSON
from plot_data import create_plot

class TestStringMethods(unittest.TestCase):

    def test_parseMainForecastJSON(self):
        with self.assertRaises(Exception):
            parseMainForecastJSON("forecastCampinas.json", "altitude")
        
        with self.assertRaises(Exception):
            parseMainForecastJSON("forecastCampinassssss.json", "temp")

        with self.assertRaises(Exception):
            parseMainForecastJSON("mockFileTest.txt", "temp")

        with self.assertRaises(Exception):
            parseMainForecastJSON("mockForecastCampinas.json", "temp")
    
    def test_create_plot(self):
        with self.assertRaises(Exception):
            create_plot("forecastCampinas.json", "temp", "mock")

if __name__ == '__main__':
    unittest.main()
