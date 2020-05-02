import sys, time
from urllib import request
from utils import FileMixins, byte_to_megabyte


class ReportHook(object):
    def __init__(self):
        self.start_time = time.time()

    def report(self, blocknum, block_size, total_size):
        """
        Print download progress message
        """

        if blocknum == 0:
            self.start_time = time.time()
            if total_size > 0:
                sys.stderr.write(
                                f"Downloading file of size:"
                                f"{byte_to_megabyte(total_size):.2f} MB\n"
                            )
        else:
            total_downloaded = blocknum * block_size
            status = f"{byte_to_megabyte(total_downloaded):3.2f} MB "

            if total_size > 0:
                percent_downloaded = total_downloaded * 100.0 / total_size
                # use carriage return plus sys.stderr to overwrite stderr
                download_rate = total_downloaded / (time.time() - self.start_time)
                estimated_time = (total_size - total_downloaded) / download_rate
                estimated_minutes = int(estimated_time / 60.0)
                estimated_seconds = estimated_time - estimated_minutes * 60.0
                status += (
                        f"{percent_downloaded:3.2f} %  "
                        f"{byte_to_megabyte(download_rate):5.2f} MB/sec"
                        f"{estimated_minutes:2.0f} min "
                        f"{estimated_seconds:2.0f} sec "
                    )
            status += "        \r"
            sys.stderr.write(status)


class Download(FileMixins):
    DIR = 'download'

    def __init__(self, *args, **kwargs):
        super(Download, self).__init__(self.DIR, *args, **kwargs)

    def __progress(self, block_num, block_size, total_size):
        downloaded = block_num * block_size
        progress = int((downloaded/total_size)*100)
        print("Download Progress",str(progress),"%")

    def run(self, url):
        try:
            sys.stderr.write("\nDownloading " + url + "\n")
            file, header = request.urlretrieve(
                                url,
                                self.path_to_store_file(),
                                reporthook=ReportHook().report
                            )
        except EnvironmentError:
            file, header = None, None
            sys.stderr.write("\nWarning: Unable to download " + url + "\n")
        return file, header
