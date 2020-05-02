import sys, os
from shutil import copyfile
import pandas as pd
from utils import FileMixins, first_date_of_month



class CSVGenerator(FileMixins):
    DIR = 'csv'

    def __init__(self, file, *args, **kwargs):
        super(CSVGenerator, self).__init__(self.DIR, *args, **kwargs)
        self.sheet_name = kwargs.get('sheet_name', None)
        self.header = kwargs.get('header', 0)
        self.names = kwargs.get('names', None)
        self.reporttype = kwargs.get('rt', None)
        self.df = pd.read_excel(
                        file,
                        self.sheet_name,
                        header=self.header,
                        names=self.names
                    )

    def _update_dates(self):
        if 'Date' in self.df.columns:
            self.df["Date"] = self.df.Date.apply(
                                lambda x: first_date_of_month(x)
                            )

    def generate(self):
        rt = self.reporttype
        if rt and rt.is_monthly:
            self._update_dates()

        self.df.to_csv(self.path_to_store_file(), index=None)
        sys.stdout.write(f"CSV generated successfully")
        self.__copy()

    def __copy(self):
        source = self.path_to_store_file()
        target = os.path.join(self.get_absolute_path(),f'../data/{self.reporttype.name.lower()}-price.csv')
        try:
            copyfile(source, target)
            sys.stdout.write(f"File copied successfully \n")
        except IOError as e:
            sys.stderr.write(f"Unable to copy file. {e}")
            exit(1)
        except:
            sys.stderr.write(f"Unexpected error: {sys.exc_info()}")
            exit(1)

