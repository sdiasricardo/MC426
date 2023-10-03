import csv

class WeatherForecastUser:
    """This class represents a user of the Weather Forecast app.
    Read the user data from a csv file and return the user data.
    """
    
    def __init__(
            self, 
            csv_file_path: str = 'user_data_sample.csv',
            email: str = 'viniciusseidel2@gmail.com'
            ):
        
        self.email = email
        self.name = None
        
        # Open csv file
        with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:
                if row['email'] == email:
                    self.email = row['email']
                    self.name = row['nome'].upper()
                    self.city = row['cidade'].upper()
                    self.receive_email = int(row['notificacao'])
                    self.risk = int(row['risco'])
                    break
            
            if self.name is None:
                raise ValueError('Email not found in csv file.')

        # Close csv file    
        csv_file.close()
    
    def get_user_name(self):
        return self.name
    
    def get_user_email(self):
        return self.email
    
    def get_user_city(self):
        return self.city
    
    def get_user_receive_email(self):
        return self.receive_email
    
    def get_user_risk(self):
        return self.risk