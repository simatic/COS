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

from myutil import lookForFloatValue, lookForIntValue, lookForNonBlankLine, openWithErrorManagement

class Conf:
    """ Class holding all configuration data """
    def __init__(self, filename):
        """Opens file named filename and reads all configuration data"""
        f = openWithErrorManagement(filename, "r", encoding="utf8")
        nbLinesRead = [0]
        self.teacherName = lookForNonBlankLine(f, nbLinesRead, False, "Nom encadrant")
        self.bonusCriteriaOK = lookForFloatValue(f, nbLinesRead, False, "Bonus sur note etudiant si critere OK")
        self.pointsCriteriaOK = lookForIntValue(f, nbLinesRead, False, "Points sur note etudiant si critere revele une bonne maitrise")
        self.pointsCriteriaAverage = lookForIntValue(f, nbLinesRead, False, "Points sur note etudiant si critere requiert ameliorations mineures")
        self.pointsCriteriaKO= lookForIntValue(f, nbLinesRead, False, "Points sur note etudiant si critere requiert ameliorations majeures")

        self.defensesFilename = lookForNonBlankLine(f, nbLinesRead, False, "Nom du fichier contenant la liste des soutenances")
        self.studentsFilename = lookForNonBlankLine(f, nbLinesRead, False, "Nom du fichier contenant la liste des étudiants et le titre de leur soutenances")
        self.criteriaTypesFilename = lookForNonBlankLine(f, nbLinesRead, False, "Nom du fichier contenant la liste des types de critères")
        self.criteriasFilename = lookForNonBlankLine(f, nbLinesRead, False, "Nom du fichier contenant la liste des critères")

        self.nominativeSheetsFilename = lookForNonBlankLine(f, nbLinesRead, False, "Nom du fichier contenant la liste de toutes les fiches nominatives")
        self.genericSheetFilename = lookForNonBlankLine(f, nbLinesRead, False, "Nom du fichier contenant une fiche générique")
        self.genericTeacherMarksFilename = lookForNonBlankLine(f, nbLinesRead, False, "Nom du fichier contenant la structure de base du fichier des notes de l'encadrant")

        self.filledNominativeSheetsFilename = lookForNonBlankLine(f, nbLinesRead, False, "Nom du fichier contenant les fiches nominatives remplies")
        self.teacherMarksFilename = lookForNonBlankLine(f, nbLinesRead, False, "Nom du fichier contenant les notes et commentaires de l'encadrant")
        self.synthesisCommentsFilename = lookForNonBlankLine(f, nbLinesRead, False, "Nom du fichier contenant la synthese des commentaires des etudiants")
        self.studentsMarksSheetFilename = lookForNonBlankLine(f, nbLinesRead, False, "Nom du fichier contenant les notes finales des etudiants")

        self.csvSeparator = lookForNonBlankLine(f, nbLinesRead, False, "Separateur dans fichiers CSV")
        self.decimalSeparator = lookForNonBlankLine(f, nbLinesRead, False, "Separateur de la partie décimale dans fichiers CSV")
        self.encoding = lookForNonBlankLine(f, nbLinesRead, False, "Encodage des fichiers utilisés")
        self.studentBound = lookForNonBlankLine(f, nbLinesRead, False, "Délimiteur entre étudiants")
        self.defenseBound = lookForNonBlankLine(f, nbLinesRead, False, "Délimiteur entre soutenances")
        self.commentBound = (lookForNonBlankLine(f, nbLinesRead, False, "Délimiteur commentaire positif"),
                             lookForNonBlankLine(f, nbLinesRead, False, "Délimiteur commentaire négatif"))
        f.close()
        
    def __str__(self):
        return ("self.teacherName = '" + self.teacherName + "'\n" +
            "self.bonusCriteriaOK = '" + str(self.bonusCriteriaOK) + "'\n" +
            "self.pointsCriteriaOK = '" + str(self.pointsCriteriaOK) + "'\n" +
            "self.pointsCriteriaAverage = '" + str(self.pointsCriteriaAverage) + "'\n" +
            "self.pointsCriteriaKO = '" + str(self.pointsCriteriaKO) + "'\n" +
            "self.defensesFilename = '" + self.defensesFilename + "'\n" +
            "self.studentsFilename = '" + self.studentsFilename + "'\n" +
            "self.criteriaTypesFilename = '" + self.criteriaTypesFilename + "'\n" +
            "self.criteriasFilename = '" + self.criteriasFilename + "'\n" +
            "self.nominativeSheetsFilename = '" + self.nominativeSheetsFilename + "'\n" +
            "self.genericSheetFilename = '" + self.genericSheetFilename + "'\n" +
            "self.genericTeacherMarksFilename = '" + self.genericTeacherMarksFilename + "'\n" +
            "self.filledNominativeSheetsFilename = '" + self.filledNominativeSheetsFilename + "'\n" +
            "self.teacherMarksFilename = '" + self.teacherMarksFilename + "'\n" +
            "self.synthesisCommentsFilename = '" + self.synthesisCommentsFilename + "'\n" +
            "self.studentsMarksSheetFilename = '" + self.studentsMarksSheetFilename + "'\n" +
            "self.csvSeparator = '" + self.csvSeparator + "'\n" +
            "self.decimalSeparator = '" + self.decimalSeparator + "'\n" +
            "self.encoding = '" + self.encoding + "'\n" +
            "self.studentBound = '" + self.studentBound + "'\n" +
            "self.defenseBound = '" + self.projectBound + "'\n" +
            "self.commentBound[0] = '" + self.commentBound[0] + "'\n" +
            "self.commentBound[1] = '" + self.commentBound[1] + "'\n")
