from io import BytesIO


def _generate_protocol_file_names(protocol):
    file_names = []
    for i in tuple(range(2, 3 + 1)) + ('SingleApp',):
        file_names.append('fcsProtocolEF{}_{}'.format(i, protocol))
    file_names.append('fcsProtocolZK_{}'.format(protocol))
    return file_names


def unzip_protocol_files(zip_file, protocol):
    protocol_files = {}
    protocol_file_names = tuple(_generate_protocol_file_names(protocol))
    for xml_name in zip_file.namelist():
        if xml_name.startswith(protocol_file_names) and (xml_name.endswith('.xml')):
            try:
                xml = BytesIO(zip_file.read(xml_name))
                protocol_files[xml_name.split('_')[0]] = xml
            except KeyError:
                print('some errors occurred %s' % KeyError)
            if (len(protocol_files) == 2) or ('fcsProtocolZPFinal' in protocol_files):
                break
    return protocol_files
