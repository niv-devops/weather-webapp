""" Module for handling weather forecast data """
class forecast:
    """ Represents a weather forecast for a specific date """
    def __init__(self, date, eve_temper=None, mor_temper=None, humidity=None):
        """ Initializes a Forecast object """
        self.date = date
        if isinstance(eve_temper, float):
            self.eve_temper = round(eve_temper, 2)
        if mor_temper != -99999:
            self.mor_temper = round(mor_temper, 2)
        if isinstance(humidity, float):
            self.humidity = round(humidity, 2)

    def to_dict(self):
        """ Converts the Forecast object to a dictionary """
        return {
            'date': self.date,
            'mor_temper': self.mor_temper,
            'eve_temper': self.eve_temper,
            'humidity': self.humidity
        }
