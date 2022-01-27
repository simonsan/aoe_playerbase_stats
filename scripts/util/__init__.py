def unpack_list(_list):
    if len(_list) == 0:
        return _list
    if isinstance(_list[0], list):
        return unpack_list(_list[0]) + unpack_list(_list[1:])
    return _list[:1] + unpack_list(_list[1:])
