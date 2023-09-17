import unittest
import json
import plot_data


class TestStringMethods(unittest.TestCase):

    def test_parseMainForecastJSON(self):
        with self.assertRaises(Exception):
            plot_data.parseMainForecastJson("forecastCampinas.json", "altitude")
        
        with self.assertRaises(Exception):
            plot_data.parseMainForecastJson("forecastCampinassssss.json", "temp")

        with self.assertRaises(Exception):
            plot_data.parseMainForecastJson("mockFileTest.txt", "temp")

        with self.assertRaises(Exception):
            plot_data.parseMainForecastJson("mockForecastCampinas.json", "temp")
    
    def test_create_plot(self):
        with self.assertRaises(Exception):
            plot_data.create_plot("forecastCampinas.json", "temp", "mock")

if __name__ == '__main__':
    unittest.main()