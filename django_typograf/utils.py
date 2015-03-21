from typograf import RemoteTypograf
import binascii


def make_typograf(instance, fields):
    """ For each instance.field in fields - make typograf """
    typograf = RemoteTypograf()
    for field in fields:
        # get field text
        text = instance.__dict__[field]
        # get hash from instance already in bd
        hash_bd = instance.__dict__['typograf_{field}_hash'.format(field=field)]
        # calculate hash of new text values
        text_hash = binascii.crc32(text.encode('utf-8'))
        # if not equals hash_bd and calculated hash
        if hash_bd != text_hash:
            # get typograf text
            typograf_text = typograf.try_process_text(text)
            # if was error and text was not change - set hash '0'
            if typograf_text == text:
                text_hash = 0
            # update fields values
            instance.__dict__['typograf_{field}_hash'.format(field=field)] = text_hash
            instance.__dict__['typograf_{field}'.format(field=field)] = typograf_text
    return instance


def get_typograf_field_name(field_name):
    """ Return field_name with typograf prefix """
    return 'typograf_{field}'.format(field=field_name)

def get_typograf_hash_field_name(field_name):
    """ Return field_name with typograf prefix, and hash suffix """
    return 'typograf_{field}_hash'.format(field=field_name)
