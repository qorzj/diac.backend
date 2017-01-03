def get_hint(diac_word):
    '''
    >>> get_hint('test_hint')
    'tooo_ooot'
    '''
    diac_word = diac_word.lower()
    ret = [diac_word[0]]
    for c in diac_word[1:-1]:
        ret.append('o' if 'a' <= c <= 'z' else c)
    return ''.join(ret) + diac_word[-1]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
