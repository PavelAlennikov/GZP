from ftplib import FTP
from io import BytesIO
from zipfile import ZipFile

import utils.date_utils as date_utils
from utils import zip_handler as zh


class GUFtpDownloader:
    def __init__(self):
        self.ftp = FTP('ftp.zakupki.gov.ru', 'free', 'free')
        self.ftp.cwd('/fcs_regions/Novosibirskaja_obl/protocols/')

    def download_zip_and_extract_xmls(self, dates_and_protocols):
        xml_files = []
        for date in dates_and_protocols.keys():
            zip_files = self._download_zip_files(date)
            protocols = dates_and_protocols[date]
            extracted_files = self._extract_xmls(zip_files, protocols)
            xml_files.extend(extracted_files)
        return xml_files

    def _download_zip_files(self, date):
        zip_files = []
        print('Downloading zip files for ', date)
        months_added = 0
        iter_date = date
        while months_added != 3:
            zip_name = self._generate_filename(iter_date)
            for file_name in self.ftp.nlst():
                if zip_name in file_name:
                    file = BytesIO()
                    print('Downloading file ', file_name, '...')
                    self.ftp.retrbinary('RETR ' + file_name, file.write)
                    zip_files.append(file)
            iter_date = date_utils.add_months(iter_date, 1)
            months_added += 1
        print('All files downloaded!')
        return zip_files

    @staticmethod
    def _extract_xmls(zip_files, protocol_numbers):
        xml_files = []
        for protocol_number in protocol_numbers:
            protocol_files = {}
            found = False
            print('Extracting xml files for %s protocol' % protocol_number)
            for zip_file in zip_files:
                unzipped_xml_files = zh.unzip_protocol_files(ZipFile(zip_file, 'r'), protocol_number)
                if unzipped_xml_files:
                    protocol_files.update(unzipped_xml_files)
                    if (len(protocol_files) == 2) or ('fcsProtocolZK' in protocol_files) or \
                     ('fcsProtocolEFSingleApp' in protocol_files):
                        found = True
                        xml_files.append(protocol_files)
                        print('Files for protocol %s were extracted successfully.\n' % protocol_number)
                        break
                else:
                    continue
            if not found:
                print("ERROR: CANT FIND PROTOCOL'S DATA FOR", protocol_number, 'PROTOCOL.\n')
        return xml_files

    @staticmethod
    def _generate_filename(date):
        return 'protocol_Novosibirskaja_obl_' + \
               date_utils.generate_date_interval(date)
