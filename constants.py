from enum import Enum, unique


@unique
class ReportType(Enum):
    DAILY = 'D'
    WEEKLY = 'W'
    MONTHLY = 'M'
    ANNUAL = 'A'

    def __init__(self, rt):
        self.rt = rt

    @property
    def is_daily(self):
        return self.rt=='D'

    @property
    def is_weekly(self):
        return self.rt=='W'
   
    @property
    def is_monthly(self):
        return self.rt=='M'

    @property
    def is_annual(self):
        return self.rt=='A' 

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_