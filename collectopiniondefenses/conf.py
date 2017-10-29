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
from myutil import lookForNonBlankLine, openWithErrorManagement

floatConfKeys = [
    "bonusCriteriaOK"
]

intConfKeys = [
    "insertDateInFilename",
    "pointsCriteriaAverage",
    "pointsCriteriaKO",
    "pointsCriteriaOK"
]

strConfKeys = [
    "criteriaTypesFilename",
    "criteriasFilename",
    "csvSeparator",
    "decimalSeparator",
    "defenseBound",
    "defensesFilename",
    "encoding",
    "filledNominativeSheetsFilename",
    "genericSheetFilename",
    "genericTeacherMarksFilename",
    "negativeCommentBound",
    "nominativeSheetsFilename",
    "positiveCommentBound",
    "studentBound",
    "studentsFilename",
    "studentsMarksSheetFilename",
    "synthesisCommentsFilename",
    "teacherMarksFilename",
    "teacherName"
]

class Conf:
    """ Class holding all configuration data """
    def __init__(self, filename):
        """Opens file named filename and reads all configuration data"""
        self.confData = {}

        # We read all of the configuration data (without taking care of the type)
        f = openWithErrorManagement(filename, "r", encoding="utf8")
        nbLinesRead = [0]

        confKeys = floatConfKeys + intConfKeys + strConfKeys

        line = lookForNonBlankLine(f, nbLinesRead, True, """Une ligne de la forme "Cle = Valeur" """)
        while (line != ""):
            pos = line.find("=")
            if pos < 0:
                sys.exit("""ERREUR: Dans le fichier "{}", à la ligne {}, cette ligne contient "{}" qui ne respecte pas le format "Clé = Valeur" """.format(
                            f.name, nbLinesRead[0], line))
            key = line[:pos].strip(" \t\n")
            value = line[pos+1:].strip(" \t\n")

            if key not in confKeys:
                sys.exit("""ERREUR: Dans le fichier "{}", à la ligne {}, cette ligne contient "{}" qui définit la clé "{}" qui est inconnue (problème d'orthographe ?)""".format(
                            f.name, nbLinesRead[0], line, key))

            self.confData[key] = value

            line = lookForNonBlankLine(f, nbLinesRead, True, """Une ligne de la forme "Cle = Valeur" """)

        f.close()

        # We take care of float data
        for key in floatConfKeys:
            try:
                result = float(self.confData[key])
            except ValueError:
                sys.exit("""ERREUR: Dans le fichier "{}", la clé "{}" a pour valeur "{}" qui n'est pas un flottant.""".format(
                    f.name, key, confData[key]))
            self.confData[key] = result
        
        # We take care of int data
        for key in intConfKeys:
            try:
                result = int(self.confData[key])
            except ValueError:
                sys.exit("""ERREUR: Dans le fichier "{}", la clé "{}" a pour valeur "{}" qui n'est pas un entier.""".format(
                    f.name, key, confData[key]))
            self.confData[key] = result
            
        # Initialize opinionType2CommentBound
        self.opinionType2CommentBound = (self.confData["positiveCommentBound"], self.confData["negativeCommentBound"])

    
    def get(self, key):
        """ Returns value associated to key in confData."""
        try:
            result = self.confData[key]
        except KeyError:
            sys.exit("""ERREUR: Le programme essaye d'accéder à la clé "{}" qui n'existe pas dans les données de configuration.""".format(key))
        return result

    def getCommentBound(self, opinionType):
        """ Returns comment bound associated to opinionType."""
        return self.opinionType2CommentBound[opinionType]

