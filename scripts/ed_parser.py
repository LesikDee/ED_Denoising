import scripts.dsn6_parser as dsn6_parser
import scripts.ccp4_parser as ccp4_parser
import scripts.molecule as molecule

def read(filename: str) -> molecule:
    file_type = filename.split('.').pop()
    if file_type == 'dsn6':
        ed: molecule = dsn6_parser.read(filename)
    elif file_type == 'ccp4':
        ed: molecule = ccp4_parser.read(filename)
    else:
        raise TypeError

    return ed