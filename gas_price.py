from downloads import Download
from csv_services import CSVGenerator

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True


class EIAGasPrice:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url', None)
        self.browser = Firefox(options=opts)
        self.reporttype = kwargs.get('reporttype', None)
        if self.reporttype:
            self.download = Download(
                                sub_dir=self.reporttype.name
                            )
        else:
            self.download = Download()

    def download_file(self):
        url = self.find_download_url()
        if bool(url):
            file, header = self.download.run(url)
            return file
        return None

    def create_csv(self, xlsfile):
        csv = CSVGenerator(
            xlsfile,
            sheet_name='Data 1',
            header=2,
            names=['Date', 'Price'],
            sub_dir=self.reporttype.name,
            ext='csv',
            rt=self.reporttype
        )
        csv.generate()

    def find_download_url(self):
        element = self.browser.find_elements_by_link_text('Download Data (XLS File)')
        if len(element) > 0:
            return element[0].get_attribute('href')
        else:
            return ''

    def open(self):
        self.browser.get(self.url)
        assert "Henry Hub Natural Gas Spot Price (Dollars per Million Btu)" in self.browser.title

    def close(self):
        self.browser.close()




# import os
# import glob
# list_of_files = glob.glob('./download/*.xls')
# latest_file = max(list_of_files, key=os.path.getctime)
# # f = open(latest_file, 'r')
# print(latest_file, os.path.getctime)

# urllib.request.urlretrieve('https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls', 'RNGWHHDd.xls', reporthook=Download_Progress)
# print("success")
