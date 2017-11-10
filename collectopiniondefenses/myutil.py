# -*- coding: utf-8 -*-

"""
 This file is part of COS : Collecte d'Opinions lors de Soutenances
 (Collect Opinions during defenSes).

 Copyright: Copyright (C) 2016-2017
 Contact: michel.simatic@telecom-sudparis.eu

 This file is part of COS : Collecte d'Opinions lors de Soutenances
 (Collect Opinions during defenSes).

 COS is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 COS is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with COS.  If not, see <http://www.gnu.org/licenses/>.

 Developer(s): Michel Simatic
"""

import sys

def float2str(f, conf):
    ### Converts float f to a string with 1 decimal digit taking into account decimal separator to be used###
    s = "{:.2f}".format(f)
    if '.' in s and conf.get("decimalSeparator") != '.':
        s = str2csvStr(s.replace('.', conf.get("decimalSeparator")), conf.get("csvSeparator"))
    return s

def lookForNonBlankLine(f, nbLinesRead, isEOF_OK, searchedInfo):
    """
    Looks for a non-blank line in file .

    Parameters
    ----------
    f : file
        File descriptor to read
    nbLinesRead : list containing one int
        Number of lines read until now in the file. This number is incremented during execution
    isEOF_OK : bool
        If true, if EOF is detected, returns an empty string. Otherwise, generates an error.
    searchedInfo : string
        Searched info for which lookForNonBlankLine was called

    Returns
    -------
    string
        the line read (without comments and leading and trailing spaces).
    """
    s = ""
    while s == "":
        s = f.readline()
        nbLinesRead[0] += 1
        if s == "":
            if isEOF_OK:
                return ""
            else:
                sys.exit("""ERREUR: Dans fichier "{}", information "{}" non trouvee""".format(f.name, searchedInfo))
        s = removeComment(s)
        s = s.strip(" \t\n")
    #print("{}:{} {}".format(filename, nbLinesRead[0], s))
    return s

def openWithErrorManagement(filename, mode, encoding):
    """Opens file called filnema with mode mode and encoding encod. Displays an error message if required."""
    try:
        f = open(filename, mode, encoding=encoding)
    except IOError:
        if mode == 'r':
            sys.exit("""ERREUR: Impossible d'ouvrir le fichier "{}". Soit il n'existe pas, soit il vous manque le droit de lecture sur ce fichier.""".format(filename))
        else:
            sys.exit("""ERREUR: Impossible d'ouvrir le fichier "{}". Soit il n'existe pas, soit il vous manque le droit d'écriture sur ce fichier.""".format(filename))
    return f

def removeComment(s):
    """If there is a '#' in s, removes '#' and the following characters"""
    result = s.find('#')
    if result == 0:
        s = ""
    elif result > 0:
        s = s[0:result-1]
    return s

def splitCsvLine(csvLine, sep):
    """
    Splits csvLine containing fields separated by sep into a list of fields

    split cannot be used for spliting CSV lines because:
      - If a field contains the character sep, the CSV field starts and ends 
        with a '"'
      - If a field is supposed to contain a character '"', it appears as '""' 
        in the CSV line
    spltCsvLine provides the correct splittring of a CSV line
    
    Parameters
    ----------
    csvLine : str
        CSV line to split
    sep : str
        Separator used for splitting.
        NB : must contain a single character

    Returns
    -------
    list of str
        each element of the list corresponds to a field found in csvLine
    """
    result = []
    current = 0
    while current < len(csvLine):
        if csvLine[current] != '"':
            # This field contains no '"' or sep ==> We look for the next sep
            pos = csvLine.find(sep, current)
            if pos < 0:
                result.append(csvLine[current:])
                current = len(csvLine)
            else:
                result.append(csvLine[current:pos])
                current = pos+1 # + 1 to skip sep
                if current == len(csvLine):
                    result.append("")
        else:
            # We look for the terminating '"', building the field at the same time
            field = ""
            fieldNotYetAppended = True
            pos = current+1 # We skip the '"' which we know is here
            while (csvLine[pos] != '"' or  # Character is not a '"'
                   pos+1 < len(csvLine)): # Character is a '"' and it is not the last one of the line
                if csvLine[pos] == '"':
                    # We are sure that we are not at the end of the line
                    if csvLine[pos+1] == sep:
                        result.append(field)
                        current = pos+2
                        fieldNotYetAppended = False
                        break
                    else:
                        # The character at pos+1 is necessarely a '"'
                        field += '"'
                        pos += 2
                else:
                    field += csvLine[pos]
                    pos += 1
            if fieldNotYetAppended:
                result.append(field)
                current = pos+1
    return result

def str2csvStr(s, sep):
    """
    Converts string s to CSV format

    - If a field contains the character sep, the CSV field must start and end 
      with a '"'
    - If a field is supposed to contain a character '"', it appears as '""' 
      in the CSV line
    
    Parameters
    ----------
    s : str
        String to convert
    sep : str
        Separator used for splitting.
        NB : must contain a single character

    Returns
    -------
    str
        Converted string
    """
    s = s.replace('"', '""')
    if '"' in s or sep in s:
        s = '"' + s +'"'
    return s


