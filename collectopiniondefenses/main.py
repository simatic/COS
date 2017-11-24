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

import datetime
from operator import itemgetter
import sys

from conf import Conf
from criteria import Criteria
from defense import Defense
from student import Student, list_opinions, POSITIVE_OPINION, AVERAGE_OPINION, NEGATIVE_OPINION
from teacherOpinion import TeacherOpinion
from myutil import float2str, lookForNonBlankLine, openWithErrorManagement, removeComment, splitCsvLine, str2csvStr

opinionType2str = ("négatif", "Erreur (Valeur non utilisée dans opinionType2str)", "positif")
opinionType2sign = ("-", "+/-", "+")

def analyzeStudentsData(conf, defenses, students, criteriaTypes, criterias):
    """
    Enrich students information with the contents of conf.get("filledNominativeSheetsFilename")

    Parameters
    ----------
    conf : Conf
        Configuration information
    f : file
        File on which to write
    defenses : list of Defense
        List of defenses
    students : liste of Student
        List of students
    criteriaTypes : liste of str
        List of criteria types
    criterias : liste of Criteria
        List of criterias

    Returns
    -------
    void
    """
    #
    # Analyze the contents of conf.get("filledNominativeSheetsFilename"),
    #
    f = openWithErrorManagement(key2inputFileName("filledNominativeSheetsFilename", conf), "r", encoding=conf.get("encoding"))
    nbLinesRead = [0]
    while readLineWithSpecificContents(f, conf.get("studentBound"), nbLinesRead, True) != "":
        # Determine student index in students
        studentLine = lookForNonBlankLine(f, nbLinesRead, False, "Ligne contenant un nom d'etudiant")
        studentLine = studentLine[:studentLine.rfind("(")] # To suppress the name of the defense which is between parenthesis at the end of the line
        studentIndex = findName(studentLine, students, nbLinesRead, f, conf.get("studentsFilename"))
        if students[studentIndex].alreadyProcessed:
            sys.exit("""ERREUR: Dans le fichier "{}", derriere la ligne {}, l'etudiant ("{}") apparaît pour la deuxième fois.""".format(conf.get("filledNominativeSheetsFilename"), nbLinesRead[0], studentLine))
        students[studentIndex].alreadyProcessed = True
        
        # Skip delimiter of student name
        readLineWithSpecificContents(f, conf.get("studentBound"), nbLinesRead, False)
        
        # Analyze answers for the different defenses evaluated by the student
        # NB: There is one less defense evaluated by the student, as he does not
        #     evalkuate his own defense.
        for unusedIndex in list(range(len(defenses)-1)):
            # Skip delimiter of defense name
            readLineWithSpecificContents(f, conf.get("defenseBound"), nbLinesRead, False)
            # Determine defense index in defenses
            defenseLine = lookForNonBlankLine(f, nbLinesRead, False, "Ligne contenant un nom de projet")
            defenseIndex = findName(defenseLine, defenses, nbLinesRead, f, conf.get("defensesFilename"))
            if defenses[defenseIndex] == students[studentIndex].defense:
                sys.exit("""ERREUR: Dans le fichier "{}", derriere la ligne {}, l'étudiant "{}"a un commentaire de son propre projet "{}" : tentative de triche ?.""".format(conf.get("filledNominativeSheetsFilename"), nbLinesRead[0], students[studentIndex].name, defenses[defenseIndex].name))
            # Skip delimiter of defense name
            readLineWithSpecificContents(f, conf.get("defenseBound"), nbLinesRead, False)
            # For each criteria type
            for criteriaType in criteriaTypes:
                # Skip criteria type
                readLineWithSpecificContents(f, criteriaType, nbLinesRead, False)
                # Handle each critera in this criteria type
                for criteria in criterias:
                    if criteria.criteriaType == criteriaType:
                        criteriaLine = lookForNonBlankLine(f, nbLinesRead, False, "Ligne contenant un critère")
                        if criteriaLine[0] in "+-":
                            # We skip '+' or '-' sign which is at the beginning of the line
                            criteriaIndex = findName(criteriaLine[1:].strip(" \t"), criterias, nbLinesRead, f, conf.get("criteriasFilename"))
                        elif criteriaLine[-1] in "+-":
                            # We skip '+' or '-' sign which is at the end of the line
                            criteriaIndex = findName(criteriaLine[:-1].strip(" \t"), criterias, nbLinesRead, f, conf.get("criteriasFilename"))
                        else:
                            criteriaIndex = findName(criteriaLine, criterias, nbLinesRead, f, conf.get("criteriasFilename"))
                        if criteriaLine[0] == '+' or criteriaLine[-1] == '+':
                            students[studentIndex].opinionsPerDefense[defenseIndex][POSITIVE_OPINION].criteriaIndex = criteriaIndex
                            students[studentIndex].opinionsPerDefense[defenseIndex][POSITIVE_OPINION].nbCriteriaIndex += 1
                        elif criteriaLine[0] == '-' or criteriaLine[-1] == '-':
                            students[studentIndex].opinionsPerDefense[defenseIndex][NEGATIVE_OPINION].criteriaIndex = criteriaIndex
                            students[studentIndex].opinionsPerDefense[defenseIndex][NEGATIVE_OPINION].nbCriteriaIndex += 1
            # We now take care of opinion comments
            for opinionType in list_opinions:
                # Skip line introducing comment
                readLineWithSpecificContents(f, conf.getCommentBound(opinionType), nbLinesRead, False)
                # Take care of comment
                s = f.readline()
                nbLinesRead[0] += 1
                if s == "":
                    sys.exit("""ERREUR: Dans le fichier "{}", derriere la ligne {}, il devrait y avoir un commentaire {} et non la fin du fichier.""".format(
                              conf.get("filledNominativeSheetsFilename"), nbLinesRead[0], opinionType2str[opinionType]))
                s = removeComment(s)
                s = s.strip(" \t\n")
                if s == "":
                    # It may happen that a student fills up the second line of the comment instead of the first line.
                    # If the first line is empty, we read the second line in case.
                    s = f.readline()
                    nbLinesRead[0] += 1
                    if s == "":
                        sys.exit("""ERREUR: Dans le fichier "{}", derriere la ligne {}, il devrait y avoir un commentaire {} et non la fin du fichier.""".format(
                                  conf.get("filledNominativeSheetsFilename"), nbLinesRead[0], opinionType2str[opinionType]))
                    s = removeComment(s)
                    s = s.strip(" \t\n")            
                students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].comment = s
                # Compute bonus for comment
                if students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].nbCriteriaIndex > 1:
                    # Student has given a "+" (or a "-") to several criteras ==>
                    # We cannot say for which criteria is this comment ==>
                    # We ignore this comment.
                    print("""ATTENTION: Pour la soutenance "{}", l'étudiant "{}" a mis le commentaire ({})\n"{}"\nMais, il a mis le signe "{}" sur plusieurs critères\n==> COS ne peut donc pas prendre en compte ce commentaire\n==> Regardez si vous pouvez ne garder qu'un "{}" dans "{}" qui correspondrait à ce commentaire.\n""".format(
                                defenses[defenseIndex].name, studentLine, opinionType2str[opinionType], 
                                students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].comment,
                                opinionType2sign[opinionType], opinionType2sign[opinionType], f.name))
                    students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].comment = ""
                if students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].comment != "":
                    criteriaIndex = students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].criteriaIndex
                    if criteriaIndex < 0:
                        print("""ATTENTION: Pour la soutenance "{}", l'étudiant "{}" a mis un commentaire {} sans sélectionner de critère {}\n==> Regardez si vous pouvez mettre un "{}" dans "{}" qui correspondrait à ce commentaire.\n""".format(
                                defenses[defenseIndex].name, studentLine, opinionType2str[opinionType], opinionType2str[opinionType],
                                opinionType2sign[opinionType], f.name))
                        students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].comment = ""
                    elif defenses[defenseIndex].teacherOpinionsPerCriteria[criteriaIndex].opinionType == opinionType:
                        # Student gave the same mak as the teacher ==> bonus
                        students[studentIndex].bonus += conf.get("bonusCriteriaOK")
                    elif (((opinionType == POSITIVE_OPINION and defenses[defenseIndex].teacherBestOpinionType == AVERAGE_OPINION) or
                           (opinionType == NEGATIVE_OPINION and defenses[defenseIndex].teacherWorstOpinionType == AVERAGE_OPINION)) and
                            defenses[defenseIndex].teacherOpinionsPerCriteria[criteriaIndex].opinionType == AVERAGE_OPINION):
                        # The teacher found no criteria with opinionType and, for this criteria which index is criteriaIndex,
                        # the teacher gave a mark signifying AVERAGE_OPINION. As the student cannot give an average opinion,
                        # we consider that this is a good answer.
                        students[studentIndex].bonus += conf.get("bonusCriteriaOK")  
    f.close()

def key2inputFileName(key, conf):
    """ Converts a key to a name for an output file """
    return conf.get("rootDirectory") + conf.get(key)

def key2ouputFileName(key, conf, dateTime):
    """ Converts a key to a name for an output file """
    name = conf.get("rootDirectory") + conf.get(key)
    if conf.get("insertDateInFilename") == 1:
        pos = name.rfind(".")
        name = name[:pos] + '_' + dateTime.replace(" ","_") + name[pos:]
    return name

def writeDefenseSheet(conf, f, defense, criteriaTypes, criterias):
    """ For defense defense, writes a criteria sheet in file f """
    f.write("{}\n{}\n{}\n".format(conf.get("defenseBound"), defense.name, conf.get("defenseBound")))
    for criteriaType in criteriaTypes:
        f.write("{}\n".format(criteriaType))
        for criteria in criterias:
            if criteria.criteriaType == criteriaType:
                f.write("    {}\n".format(criteria.name))
    for opinionType in list_opinions:
        f.write("{}\n\n\n".format(conf.getCommentBound(opinionType)))

def generateModels(conf, defenses, students, criteriaTypes, criterias, dateTime):
    """
    Generates models in conf.get("nominativeSheetsFilename"), conf.get("genericSheetFilename") and conf.get("genericTeacherMarksFilename")

    Parameters
    ----------
    conf : Conf
        Configuration information
    defenses : list of Defense
        List of defenses
    students : liste of Student
        List of students
    criteriaTypes : liste of str
        List of criteria types
    criterias : liste of Criteria
        List of criterias
    dateTime : str
        String containing date and time to be used in name of output files

    Returns
    -------
    void
    """
    #
    # Generate conf.get("nominativeSheetsFilename")
    #
    f = openWithErrorManagement(key2ouputFileName("nominativeSheetsFilename", conf, dateTime), "w", encoding=conf.get("encoding"))
    for student in students:
        f.write("{}\n{} ({})\n{}\n".format(conf.get("studentBound"), student.name, student.defense.name, conf.get("studentBound")))
        for defense in defenses:
            if defense != student.defense:
                writeDefenseSheet(conf, f, defense, criteriaTypes, criterias)
    f.close()
    
    #
    # Generate conf.get("genericSheetFilename")
    #
    f = openWithErrorManagement(key2ouputFileName("genericSheetFilename", conf, dateTime), "w", encoding=conf.get("encoding"))
    f.write("{}\n\nNOM Prénom :                                       Soutenance :\n\n{}\n\n".format(conf.get("studentBound"), conf.get("studentBound")))
    for defense in defenses:
        writeDefenseSheet(conf, f, defense, criteriaTypes, criterias)
    f.close()

    #
    # Generate conf.get("genericTeacherMarksFilename")
    #
    f = openWithErrorManagement(key2ouputFileName("genericTeacherMarksFilename", conf, dateTime), "w", encoding=conf.get("encoding"))
    # Generate the title of the columns
    f.write("{}Note max critere KO{}Note min critere OK".format(conf.get("csvSeparator"), conf.get("csvSeparator")))
    for defense in defenses:
        f.write("{}{}".format(conf.get("csvSeparator"), str2csvStr(defense.name, conf.get("csvSeparator"))))
    f.write("\n")
    # For each criteria, generate a line for the mark and a line for the comment
    for criteria in criterias:
        s = str2csvStr("{} / {} ({} points)".format(criteria.criteriaType, criteria.name, criteria.maxPoints),
                       conf.get("csvSeparator")
                      )
        f.write(s)
        f.write(conf.get("csvSeparator"))
        f.write(float2str(criteria.maxCriteriaKO, conf))
        f.write(conf.get("csvSeparator"))
        f.write(float2str(criteria.minCriteriaOK, conf))
        f.write(conf.get("csvSeparator") * len(defenses))
        f.write("\n");

        f.write("Commentaire de ce critère")
        f.write(conf.get("csvSeparator") * 2) # For the 2 columns corresponding to criteria.maxCriteriaKO and criteria.minCriteriaOK
        f.write(conf.get("csvSeparator") * len(defenses))
        f.write("\n")
        
    f.write(str2csvStr("Ligne inutilisée (par exemple, pour y mettre des totaux)", conf.get("csvSeparator")))
    f.write(conf.get("csvSeparator") * len(defenses))
    f.write("\n");

    f.write(str2csvStr("Commentaires généraux", conf.get("csvSeparator")))
    f.write(conf.get("csvSeparator") * len(defenses))
        
    f.close()

def analyzeTeacherData(conf, defenses, criteriaTypes, criterias):
    """
    Enrich defenses information with the contents of conf.get("teacherMarksFilename")

    Parameters
    ----------
    conf : Conf
        Configuration information
    f : file
        File on which to write
    defenses : list of Defense
        List of defenses
    students : liste of Student
        List of students
    criteriaTypes : liste of str
        List of criteria types
    criterias : liste of Criteria
        List of criterias

    Returns
    -------
    void
    """
    #
    # Analyze the contents of conf.get("teacherMarksFilename"),
    #
    f = openWithErrorManagement(key2inputFileName("teacherMarksFilename", conf), "r", encoding=conf.get("encoding"))
    nbLinesRead = [0]

    lookForNonBlankLine(f, nbLinesRead, False, "Ligne de titre des colonnesNom soutenance")  # We ignore the line giving the title of the columns
    # We deal with each criteria
    for criteria in criterias:
        # Read the marks for this criteria
        lineMarks = lookForNonBlankLine(f, nbLinesRead, False, "Ligne contenant les notes pour un critère donné")
        marks = splitCsvLine(lineMarks, conf.get("csvSeparator"))
        # Read the comments for this criteria
        lineComments = lookForNonBlankLine(f, nbLinesRead, False, "Ligne contenant les commentaires pour un critère donné")
        comments = splitCsvLine(lineComments, conf.get("csvSeparator"))
        # Add (mark, comment) to each defense
        column = 3 # We set column to 3 in order to skip :
                   #   - column 0 which contains title of the line,
                   #   - column 1 which contains value for maxCriteriaKO
                   #   - column 2 which contains value for minCriteriaOK
        for defense in defenses:
            try:
                mark = float(marks[column])
            except ValueError:
                sys.exit("""Dans le fichier "{}", la soutenance "{}" a son critère "{}" qui a reçu la note "{}" qui n'est n'est pas un flottant compris entre 0 et {}.""".format(
                         f.name, defense.name, criteria.name, marks[column], criteria.maxPoints))                
            if (mark < 0 or mark > criteria.maxPoints):
                sys.exit("""Dans le fichier "{}", la soutenance "{}" a son critère "{}" qui a reçu la note de {} qui n'est pas comprise entre 0 et {}.""".format(
                         f.name, defense.name, criteria.name, mark, criteria.maxPoints))
            defense.addMarkComment(TeacherOpinion(mark, comments[column], criteria))
            column += 1

    lookForNonBlankLine(f, nbLinesRead, False, "Ligne de titre des colonnesNom soutenance")  # We ignore the line left intentionally blank

    lineGeneralComments = lookForNonBlankLine(f, nbLinesRead, False, "Ligne contenant les commentaires généraux de chaque projet")
    generalComments = splitCsvLine(lineGeneralComments, conf.get("csvSeparator"))
    column = 3 # We set column to 3 in order to skip column 0 which contains title of the line,
               # column 1 which contains Note max critere KO, and column 2 which contains 
               # Note min critere OK
    for defense in defenses:
        defense.generalComment = generalComments[column]
        column += 1
    f.close()
    
    #
    # Update each defense, now that we know all the marks given by teacher
    #
    for defense in defenses:
        defense.update()

def readLineWithSpecificContents(f, specificContents, nbLinesRead, isEOF_OK):
    """
    Reads file f waiting to read string specificContents.

    Reads file f until it finds a non-empty line.
    If this non-empty line is specificContents (differences in number of spaces 
    are accepted), it returns it. Otherwise, it displays an error message 
    mentioning filename and nbLinesRead.
    If it finds EOF during its search
        If isEOF_OK is True, just returns "".
        Otherwise displays an error message and stops.

    Parameters
    ----------
    f : file
        File descriptor to read
    specificContents : str
        String which should be read.
    nbLinesRead : list containing one int
        Number of lines read until now in the file. This number is incremented during execution
    isEOF_OK : bool
        If true, if EOF is detected, returns False. Otherwise, generates an error.

    Returns
    -------
    str
        String containing specificContents or "" if EOF
    """
    line = lookForNonBlankLine(f, nbLinesRead, isEOF_OK, specificContents)
    if line == "":
        if isEOF_OK:
            return ""
        sys.exit("""ERREUR: Dans le fichier "{}", à la ligne {}, le programme s'attendait à la ligne "{}" et est arrivé à la fin du fichier.""".format(f.name, nbLinesRead[0], specificContents))
    if line.replace(" ", "") != specificContents.replace(" ", ""):
        sys.exit("""ERREUR: Dans le fichier "{}", à la ligne {}, le programme s'attendait à la ligne "{}" et a lu la ligne "{}".""".format(f.name, nbLinesRead[0], specificContents, line))
    return line

def findName(name, searchedList, nbLinesRead, f, nameType):
    """
    Looks for a name in searchedList (where objects of the list all have a name field) and returns its index (or stops with an error if it did not find it)

    Parameters
    ----------
    name : str
        Searched name
    searchedList : list
        List in which to do the search
    nbLinesRead : list containing one int
        Number of lines read until now in the file.
    f : file
        File on which we are working
    nameType : string
        Name of the type on which we are working

    Returns
    -------
    int
        Index of student in students
    """
    nameWithoutSpace = name.replace(" ", "")
    index = 0
    while index < len(searchedList) and nameWithoutSpace != searchedList[index].nameWithoutSpace:
        index += 1
    if index >= len(searchedList):
        sys.exit("""ERREUR: Dans le fichier "{}", à la ligne {}, le nom "{}" n'existe pas dans le fichier des "{}".""".format(f.name, nbLinesRead[0], name, nameType))
    return index

def generateResults(conf, defenses, students, criteriaTypes, criterias, dateTime):
    """
    Generates files conf.get("synthesisCommentsFilename"), conf.get("evaluationCommentsFilename")
    and conf.get("studentsMarksSheetFilename")

    Parameters
    ----------
    conf : Conf
        Configuration information
    f : file
        File on which to write
    defenses : list of Defense
        List of defenses
    students : liste of Student
        List of students
    criteriaTypes : liste of str
        List of criteria types
    criterias : liste of Criteria
        List of criterias
    dateTime : str
        String containing date and time to be used in name of output files

    Returns
    -------
    void
    """

    #
    # Generate conf.get("synthesisCommentsFilename")
    #
    f = openWithErrorManagement(key2ouputFileName("synthesisCommentsFilename", conf, dateTime), "w", encoding=conf.get("encoding"))
    for defenseIndex in list(range(len(defenses))):
        # We cound how many '+' and '-' there are for each criteria
        nbPosNeg = [ [], [], [] ]
        for criteriaIndex in list(range(len(criterias))):
            for opinionType in list_opinions:
                nbPosNeg[opinionType].append([0, criteriaIndex])
        for student in students:
            for opinionType in list_opinions:
                if student.opinionsPerDefense[defenseIndex][opinionType].criteriaIndex >= 0:
                    nbPosNeg[opinionType][student.opinionsPerDefense[defenseIndex][opinionType].criteriaIndex][0] += 1
        # We get a sorted version of nbPositive and nbNegative
        sortedNbPosNeg = [sorted(nbPosNeg[NEGATIVE_OPINION], key=itemgetter(0)),
                          sorted(nbPosNeg[AVERAGE_OPINION],  key=itemgetter(0)),
                          sorted(nbPosNeg[POSITIVE_OPINION], key=itemgetter(0))
                          ]
        # We display the project name and the general comment on the defense
        f.write("{}\n{}\n{}\n".format(conf.get("defenseBound"), defenses[defenseIndex].name, conf.get("defenseBound")))
        if defenses[defenseIndex].generalComment == "":
            f.write("Pas de commentaire général de {}\n\n".format(conf.get("teacherName")))
        else:
            f.write("Commentaire général de {} :\n".format(conf.get("teacherName")))
            for lineComment in defenses[defenseIndex].generalComment.split("\\n"):
                f.write(lineComment)
                f.write("\n")
            f.write("\n")
        # We display the results for positive criteria and negative criteria            
        for opinionType in list_opinions:
            for index in list(range(len(criterias)-1, -1, -1)):
                criteriaIndex = sortedNbPosNeg[opinionType][index][1]
                teacherOpinion = defenses[defenseIndex].teacherOpinionsPerCriteria[criteriaIndex]
                if ((sortedNbPosNeg[opinionType][index][0] > 0)
                    or (teacherOpinion.opinionType == opinionType)
                    or ((opinionType == AVERAGE_OPINION) and (opnionType == POSITIVE_OPINION))):
                    f.write("""({}) Cité {:2} fois par les étudiants : {} - Note {} = {}/{} (correspondant à "{}")""".format(
                           opinionType2sign[opinionType],
                           sortedNbPosNeg[opinionType][index][0],
                           criterias[criteriaIndex].name,
                           conf.get("teacherName"),
                           teacherOpinion.mark,
                           criterias[criteriaIndex].maxPoints,
                           opinionType2sign[teacherOpinion.opinionType]))
                    if defenses[defenseIndex].teacherOpinionsPerCriteria[criteriaIndex].comment != "":
                        f.write(", " + defenses[defenseIndex].teacherOpinionsPerCriteria[criteriaIndex].comment)
                    f.write("\n")
                    for student in students:
                        if (student.opinionsPerDefense[defenseIndex][opinionType].criteriaIndex == criteriaIndex and
                            student.opinionsPerDefense[defenseIndex][opinionType].comment != ""):
                            f.write("\t* {}\n".format(student.opinionsPerDefense[defenseIndex][opinionType].comment))
        f.write("\n")
    f.close()
    
    #
    # Generate conf.get("evaluationCommentsFilename")
    #
    f = openWithErrorManagement(key2ouputFileName("evaluationCommentsFilename", conf, dateTime), "w", encoding=conf.get("encoding"))
    for student in students:
        f.write("{}\n{} ({})\n{}\n".format(conf.get("studentBound"), student.name, student.defense.name, conf.get("studentBound")))
        for defenseIndex in list(range(len(defenses))):
            defense = defenses[defenseIndex]
            if defense != student.defense:
                f.write("{}\n{}\n{}\n".format(conf.get("defenseBound"), defense.name, conf.get("defenseBound")))
                for opinionType in list_opinions:
                    criteriaIndex = student.opinionsPerDefense[defenseIndex][opinionType].criteriaIndex;
                    if criteriaIndex >= 0:
                        f.write("{} {}\n".format(opinionType2sign[opinionType], criterias[criteriaIndex].name))
                        teacherOpinion = defense.teacherOpinionsPerCriteria[criteriaIndex]
                        f.write("""  Evaluation de {} = {}/{} (correspondant à "{}")\n""".format(
                                conf.get("teacherName"),
                                teacherOpinion.mark,
                                criterias[criteriaIndex].maxPoints,
                                opinionType2sign[teacherOpinion.opinionType]))
                    else:
                        f.write("{} non évalué, car non fourni (ou alors manque de commentaire)\n".format(opinionType2sign[opinionType]))
        f.write("\n")
    f.close()
    
    #
    # Generate conf.get("studentsMarksSheetFilename")
    #
    f = openWithErrorManagement(key2ouputFileName("studentsMarksSheetFilename", conf, dateTime), "w", encoding=conf.get("encoding"))
    f.write("Nom etudiant{}Note donnee par {} a la soutenance{}Bonus opinion{}Note finale module\n".format(
        conf.get("csvSeparator"), conf.get("teacherName"), conf.get("csvSeparator"), conf.get("csvSeparator")))
    for student in students:
        f.write("{}{}{}{}{}{}{}\n".format(
            str2csvStr(student.name, conf.get("csvSeparator")), conf.get("csvSeparator"),
            float2str(student.defense.teacherFinalMark, conf), conf.get("csvSeparator"),
            float2str(student.bonus, conf), conf.get("csvSeparator"),
            float2str(student.defense.teacherFinalMark + student.bonus, conf)))
    f.close()

def usage():
    print("USAGE: DefensePairEvaluation -12 configuration.txt")

def main():
    """Main entry point of the application"""

    #
    # Call parameter analysis
    #
    if len(sys.argv) != 3:
        print("ERREUR: Pas assez de parametres")
        usage()
        return

    if sys.argv[1][0] != '-':
        print("""ERREUR: Le premier parametre devrait etre "-1" ou "-2" (sans les guillemets)""")
        usage()
        return

    if len(sys.argv[1]) == 1 or sys.argv[1][1] not in "12":
        print("""ERREUR: Le premier parametre devrait etre "-1" ou "-2" (sans les guillemets)""")
        usage()
        return
    
    #
    # We display cos version before starting the processing
    #
    print()
    print("cos version 1.0.0")
    print()

    #
    # Read all configuration data
    #
    conf = Conf(sys.argv[2])

    #
    # Read the list of defenses
    #
    defenses = []
    f = openWithErrorManagement(key2inputFileName("defensesFilename", conf), "r", encoding=conf.get("encoding"))
    nbLinesRead = [0]
    name = lookForNonBlankLine(f, nbLinesRead, True, "Nom soutenance")
    while name != "":
        defenses.append(Defense(name))
        name = lookForNonBlankLine(f, nbLinesRead, True, "Nom soutenance")
    f.close()
    
    #
    # Read the list of students and the title of their defense
    #
    students = []
    f = openWithErrorManagement(key2inputFileName("studentsFilename", conf), "r", encoding=conf.get("encoding"))
    nbLinesRead = [0]
    
    lookForNonBlankLine(f, nbLinesRead, True, "Nom soutenance") # We ignore the line giving the title of the columns
    studentLine = lookForNonBlankLine(f, nbLinesRead, True, "Nom soutenance")
    while studentLine != "":
        info = splitCsvLine(studentLine, conf.get("csvSeparator"))
        # We look for info in the list of defense names
        found = False
        for defense in defenses:
            if info[1] == defense.name:
                # OK, this defense name is known
                students.append(Student(info[0], defense, defenses))
                found = True
                break
        if not found:
            sys.exit("""ERREUR: Dans le fichier "{}", la ligne {} ("{}") fait référence à une soutenance intitulée "{}" qui n'apparaît pas dans le fichier "{}".""".format(conf.get("studentsFilename"), nbLinesRead[0], studentLine, info[1], conf.get("defensesFilename")))
        studentLine = lookForNonBlankLine(f, nbLinesRead, True,  "Nom soutenance")
    f.close()    

    #
    # Read the list of criteria types
    #
    criteriaTypes = []
    f = openWithErrorManagement(key2inputFileName("criteriaTypesFilename", conf), "r", encoding=conf.get("encoding"))
    nbLinesRead = [0]
    criteriaType = lookForNonBlankLine(f, nbLinesRead, True, "Type de critère")
    while criteriaType != "":
        criteriaTypes.append(criteriaType)
        criteriaType = lookForNonBlankLine(f, nbLinesRead, True, "Type de critère")
    f.close()
    
    #
    # Read the list of criterias
    #
    criterias = []
    f = openWithErrorManagement(key2inputFileName("criteriasFilename", conf), "r", encoding=conf.get("encoding"))
    nbLinesRead = [0]
    
    lookForNonBlankLine(f, nbLinesRead, True, "Nom critère") # We ignore the line giving the title of the columns
    criteriaLine = lookForNonBlankLine(f, nbLinesRead, True, "Nom critère")
    while criteriaLine != "":
        info = splitCsvLine(criteriaLine, conf.get("csvSeparator"))
        # We look for info[0] in the list of criteria types
        found = False
        for criteriaType in criteriaTypes:
            if info[0] == criteriaType:
                found = True
                break
        if not found:
            sys.exit("""ERREUR: Dans fichier "{}", la ligne {} ("{}") fait référence à un type de critère intitulée "{}" qui n'apparaît pas dans le fichier "{}".""".format(
                    f.name, nbLinesRead[0], criteriaLine, info[0], conf.get("criteriaTypesFilename")))
        # OK, this citeriaType is known
        try:
            floatValue = float(info[2])
        except ValueError:
            sys.exit("""ERREUR: Dans fichier "{}", la ligne {} ("{}") a son 3ème champ ("{}") qui n'est pas un flottant.""".format(
                    f.name, nbLinesRead[0], criteriaLine, info[2]))
        criterias.append(Criteria(info[0], info[1], floatValue, conf.get("ratioCriteriaKO"), conf.get("ratioCriteriaOK")))
        criteriaLine = lookForNonBlankLine(f, nbLinesRead, True, "Nom critère")
    f.close()
    
    #
    # Prepare dateTime string which may be used for names of output files
    #
    date = datetime.datetime.now()
    s = str(date)
    dateTime = s[:s.find('.')]
    
    #
    # Remaining work depends on what the user asks for
    #
    if sys.argv[1][1] == '1':
        generateModels(conf, defenses, students, criteriaTypes, criterias, dateTime);
    else:
        analyzeTeacherData(conf, defenses, criteriaTypes, criterias);
        analyzeStudentsData(conf, defenses, students, criteriaTypes, criterias);
        generateResults(conf, defenses, students, criteriaTypes, criterias, dateTime);

    #
    # We display an end of execution message
    #
    if sys.argv[1][1] == '1':
        print("""OK, exécution de la phase {} terminée : les fichiers "{}", "{}" et "{}" ont été générés.""".format(
                sys.argv[1][1],
                key2ouputFileName("nominativeSheetsFilename", conf, dateTime),
                key2ouputFileName("genericSheetFilename", conf, dateTime),
                key2ouputFileName("genericTeacherMarksFilename", conf, dateTime)))
    else:
        print("""OK, exécution de la phase {} terminée : les fichiers "{}", "{}" et "{}" ont été générés.""".format(
                sys.argv[1][1],
                key2ouputFileName("synthesisCommentsFilename", conf, dateTime), 
                key2ouputFileName("evaluationCommentsFilename", conf, dateTime), 
                key2ouputFileName("studentsMarksSheetFilename", conf, dateTime)))
    print()
    
    return

# Main entry point of the program
main()
