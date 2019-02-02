#!/usr/bin/env python
def boolvec2int(boolvec) :
    """
    Turn an array (or list) of booleans into
    a integer by treating the array as the
    binary digits (True=1, False=0) of an
    integer, with the most significant digit
    in the 0th position.

    Should be equivalent to this:

    if len(boolvec) == 0 :
        return 0
    else :
        return int(boolvec[0]) + 2 * boolvec2int(boolvec[1:])   
    """
    return int(''.join(map(str,map(int,boolvec))),2)

def mat2html(M,fmt=str) :
    """
    Convert a numpy matrix (or list of lists)
    into an html table for display.  Takes an
    optional 2nd argument 'fmt' for converting
    matrix elements into strings.
    """
    s='<table>\n'
    for row in M :
        s += '<tr>'
        s += ''.join(('<td>' + fmt(_) + '</td>' for _ in row))
        s += '</tr>\n'
    s +='</table>\n'
    return s

def cartprod(*args) :
    """
    Return the cartesean product of the lists
    passed in as arguments.
    """
    return reduce(lambda x, y : [xx+[yy] for xx in x for yy in y],args,[[]])
