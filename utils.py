import os
import datetime
import time



def format_date(dtDateTime,strFormat="%Y-%m-%d"):
    # format a datetime object as YYYY-MM-DD string and return
    return dtDateTime.strftime(strFormat)


def make_date_time(dateString,strFormat="%Y-%m-%d"):
    # Expects "YYYY-MM-DD" string
    # returns a datetime object
    eSeconds = time.mktime(time.strptime(dateString,strFormat))
    return datetime.datetime.fromtimestamp(eSeconds)


def first_date_of_month(dtDateTime):
    # returns first date of month from given datetime object
    return make_date_time(format_date(dtDateTime,"%Y-%m-01"))


def get_file_name(name=None, ext='xls'):
    if bool(name):
        return f'{name}.{ext}'
    return f'{int(time.time())}.{ext}'


def byte_to_megabyte(byte):
    """
    Convert byte value to megabyte
    """

    return byte / (1024.0**2)


class FileMixins(object):
    def __init__(self, directory, **kwargs):
        self._directory = self.__create_dir(directory)
        self._sub_dir = self.__create_sub_dir(directory, **kwargs)
        self._file = get_file_name(
                        name=kwargs.get('file_name', None),
                        ext=kwargs.get('ext', 'xls'),
                    )

    def get_absolute_path(self):
        return os.path.abspath(self._directory)

    def path_to_store_file(self):
        if bool(self._sub_dir):
            return f'{self.get_absolute_path()}/{self._sub_dir}/{self._file}'
        return f'{self.get_absolute_path()}/{self._file}'

    def __create_dir(self, directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)
        return directory

    def __create_sub_dir(self, directory, **kwargs):
        subdir = kwargs.get('sub_dir', None)
        if subdir and (not os.path.isdir(f'{directory}/{subdir}')):
            os.mkdir(f'{directory}/{subdir}')
        return subdir
