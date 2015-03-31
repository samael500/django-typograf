from typograf import RemoteTypograf
import binascii


def get_typograf_field_name(field_name):
    """ Return field_name with typograf prefix """
    return 'typograf_{field}'.format(field=field_name)


def get_typograf_hash_field_name(field_name):
    """ Return field_name with typograf prefix, and hash suffix """
    return 'typograf_{field}_hash'.format(field=field_name)


def make_typograf(instance, fields):
    """ For each instance.field in fields - make typograf """
    typograf = RemoteTypograf()
    for field in fields:
        # get field text
        text = getattr(instance, field)
        # get hash from instance already in bd
        hash_bd = getattr(instance, get_typograf_hash_field_name(field))
        # calculate hash of new text values
        text_hash = str(binascii.crc32(text.encode('utf-8')))
        # if not equals hash_bd and calculated hash
        if hash_bd != text_hash:
            # get typograf text
            typograf_text = typograf.try_process_text(text)
            # if was error and text was not change - set hash '0'
            if typograf_text == text:
                text_hash = None
            # update fields values
            setattr(instance, get_typograf_hash_field_name(field), text_hash)
            setattr(instance, get_typograf_field_name(field), typograf_text)
    return instance
