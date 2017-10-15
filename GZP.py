import pandas as pd
from utils import excel_handler as eh, xml_handler as xmlh
from utils.ftp_downloader import GUFtpDownloader as ftpd

dates_and_protocols, protocols_count = eh.read_dates_and_protocols('input.xlsx')
ftp_downloader = ftpd()
excel_output_data = pd.DataFrame()
all_protocol_files = ftp_downloader.download_zip_and_extract_xmls(dates_and_protocols)

print(len(all_protocol_files), ' protocols found out of ', protocols_count)

for xml_files_for_one_protocol in all_protocol_files:
    excel_output_data = xmlh.extract_fields(xml_files_for_one_protocol, excel_output_data)
print('All xml files parsed successfully')
eh.write_fields_into_excel('protocols_data.xlsx', excel_output_data)
input('Results in protocols_data.xlsx file. To exit press "Enter"...')
