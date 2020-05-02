import sys
from constants import ReportType
from gas_price import EIAGasPrice


if __name__ == '__main__':
    print("Henry Hub Natural Gas Spot Price!")
    welcome_str = f"How do you want to fetch gas price. \n"
    welcome_str += f"{ReportType.DAILY.name} : {ReportType.DAILY.value} \n"
    welcome_str += f"{ReportType.WEEKLY.name} : {ReportType.WEEKLY.value} \n"
    welcome_str += f"{ReportType.MONTHLY.name} : {ReportType.MONTHLY.value} \n"
    welcome_str += f"{ReportType.ANNUAL.name} : {ReportType.ANNUAL.value} \n"
    welcome_str += f"Select one choice({ReportType.DAILY.value} |"
    welcome_str += f" {ReportType.WEEKLY.value} | {ReportType.MONTHLY.value}"
    welcome_str += f" | {ReportType.ANNUAL.value}): \n"
    

    price_report_type = input(welcome_str).upper()
    if ReportType.has_value(price_report_type):
        url = f"https://www.eia.gov/dnav/ng/hist/rngwhhd{price_report_type}.htm"
        eia = EIAGasPrice(url=url, reporttype=ReportType(price_report_type))
        eia.open()
        downloaded_file = eia.download_file()
        if bool(downloaded_file):
            eia.create_csv(downloaded_file)
        else:
            sys.stdout.write(f"Download failed")
        eia.close()
    else:
        print("Select correct value!")
        sys.exit(0)
