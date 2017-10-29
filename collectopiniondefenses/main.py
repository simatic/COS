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
from operator import itemgetter

from conf import Conf
from criteria import Criteria
from defense import Defense
from student import Student, list_opinions, POSITIVE_OPINION, NEGATIVE_OPINION
from teacherOpinion import TeacherOpinion
from myutil import float2str, lookForNonBlankLine, openWithErrorManagement, removeComment, splitCsvLine, str2csvStr

opinionType2str = ("positif", "négatif")
opinionType2sign = ("+", "-")

def analyzeStudentsData(conf, defenses, students, criteriaTypes, criterias):
    """
    Enrich students information with the contents of conf.filledNominativeSheetsFilename

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
    # Analyze the contents of conf.filledNominativeSheetsFilename,
    #
    f = openWithErrorManagement(conf.filledNominativeSheetsFilename, "r", encoding=conf.encoding)
    nbLinesRead = [0]
    while readLineWithSpecificContents(f, conf.studentBound, nbLinesRead, True) != "":
        # Determine student index in students
        studentLine = lookForNonBlankLine(f, nbLinesRead, False, "Ligne contenant un nom d'etudiant")
        studentLine = studentLine[:studentLine.rfind("(")] # To suppress the name of the defense which is between parenthesis at the end of the line
        studentIndex = findName(studentLine, students, nbLinesRead, f, conf.studentsFilename)
        if students[studentIndex].alreadyProcessed:
            sys.exit("""ERREUR: Dans le fichier "{}", derriere la ligne {}, l'etudiant ("{}") apparaît pour la deuxième fois.""".format(conf.filledNominativeSheetsFilename, nbLinesRead[0], studentLine))
        students[studentIndex].alreadyProcessed = True
        
        # Skip delimiter of student name
        readLineWithSpecificContents(f, conf.studentBound, nbLinesRead, False)
        
        # Analyze answers for the different defenses evaluated by the student
        # NB: There is one less defense evaluated by the student, as he does not
        #     evalkuate his own defense.
        for unusedIndex in list(range(len(defenses)-1)):
            # Skip delimiter of defense name
            readLineWithSpecificContents(f, conf.defenseBound, nbLinesRead, False)
            # Determine defense index in defenses
            defenseLine = lookForNonBlankLine(f, nbLinesRead, False, "Ligne contenant un nom de projet")
            defenseIndex = findName(defenseLine, defenses, nbLinesRead, f, conf.defensesFilename)
            if defenses[defenseIndex] == students[studentIndex].defense:
                sys.exit("""ERREUR: Dans le fichier "{}", derriere la ligne {}, l'étudiant "{}"a un commentaire de son propre projet "{}" : tentative de triche ?.""".format(conf.filledNominativeSheetsFilename, nbLinesRead[0], students[studentIndex].name, defenses[defenseIndex].name))
            # Skip delimiter of defense name
            readLineWithSpecificContents(f, conf.defenseBound, nbLinesRead, False)
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
                            criteriaIndex = findName(criteriaLine[1:].strip(" \t"), criterias, nbLinesRead, f, conf.criteriasFilename)
                        else:
                            criteriaIndex = findName(criteriaLine, criterias, nbLinesRead, f, conf.criteriasFilename)
                        if criteriaLine[0] == '+':
                            students[studentIndex].opinionsPerDefense[defenseIndex][POSITIVE_OPINION].criteriaIndex = criteriaIndex
                            students[studentIndex].opinionsPerDefense[defenseIndex][POSITIVE_OPINION].nbCriteriaIndex += 1
                        elif criteriaLine[0] == '-':
                            students[studentIndex].opinionsPerDefense[defenseIndex][NEGATIVE_OPINION].criteriaIndex = criteriaIndex
                            students[studentIndex].opinionsPerDefense[defenseIndex][NEGATIVE_OPINION].nbCriteriaIndex += 1
            # We now take care of opinion comments
            opinionType2pointsCriteria = (conf.pointsCriteriaOK, conf.pointsCriteriaKO)
            for opinionType in list_opinions:
                # Skip line introducing comment
                readLineWithSpecificContents(f, conf.commentBound[opinionType], nbLinesRead, False)
                # Take care of comment
                s = f.readline()
                nbLinesRead[0] += 1
                if s == "":
                    sys.exit("""ERREUR: Dans le fichier "{}", derriere la ligne {}, il devrait y avoir un commentaire {} et non la fin du fichier.""".format(
                              conf.filledNominativeSheetsFilename, nbLinesRead[0], opinionType2str[opinionType]))
                s = removeComment(s)
                s = s.strip(" \t\n")
                if s == "":
                    # It may happen that a student fills up the second line of the comment instead of the first line.
                    # If the first line is empty, we read the second line in case.
                    s = f.readline()
                    nbLinesRead[0] += 1
                    if s == "":
                        sys.exit("""ERREUR: Dans le fichier "{}", derriere la ligne {}, il devrait y avoir un commentaire {} et non la fin du fichier.""".format(
                                  conf.filledNominativeSheetsFilename, nbLinesRead[0], opinionType2str[opinionType]))
                    s = removeComment(s)
                    s = s.strip(" \t\n")            
                students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].comment = s
                # Compute bonus for comment
                if students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].nbCriteriaIndex > 1:
                    # Student has given a "+" (or a "-") to several criteras ==>
                    # We cannot say for which criteria is this comment ==>
                    # We ignore this comment.
                    print("""WARNING: Pour la soutenance "{}", l'étudiant "{}" a mis le commentaire ({})\n"{}"\nMais, il a mis le signe "{}" sur plusieurs critères\n==> COS ne peut donc pas prendre en compte ce commentaire\n==> Regardez si vous pouvez ne garder qu'un "{}" dans "{}" qui correspondrait à ce commentaire.\n""".format(
                                defenses[defenseIndex].name, studentLine, opinionType2str[opinionType], 
                                students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].comment,
                                opinionType2sign[opinionType], opinionType2sign[opinionType], f.name))
                    students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].comment = ""
                if students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].comment != "":
                    criteriaIndex = students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].criteriaIndex
                    if criteriaIndex < 0:
                        print("""WARNING: Pour la soutenance "{}", l'étudiant "{}" a mis un commentaire {} sans sélectionner de critère {}\n==> Regardez si vous pouvez mettre un "{}" dans "{}" qui correspondrait à ce commentaire.\n""".format(
                                defenses[defenseIndex].name, studentLine, opinionType2str[opinionType], opinionType2str[opinionType],
                                opinionType2sign[opinionType], f.name))
                        students[studentIndex].opinionsPerDefense[defenseIndex][opinionType].comment = ""
                    elif defenses[defenseIndex].teacherOpinionsPerCriteria[criteriaIndex].mark == opinionType2pointsCriteria[opinionType]:
                        # Student gave the same mak as the teacher ==> bonus
                        students[studentIndex].bonus += conf.bonusCriteriaOK
                    elif (((opinionType == POSITIVE_OPINION and defenses[defenseIndex].teacherBestMark == conf.pointsCriteriaAverage) or
                           (opinionType == NEGATIVE_OPINION and defenses[defenseIndex].teacherWorstMark == conf.pointsCriteriaAverage)) and
                            defenses[defenseIndex].teacherOpinionsPerCriteria[criteriaIndex].mark == conf.pointsCriteriaAverage):
                        # The teacher found no criteria with opinionType2pointsCriteria[opinionType] and gave a mark with
                        # average value to criteria which index is criteriaInde. As the student cannot give an average opinion,
                        # we consider that this is a good answer.
                        students[studentIndex].bonus += conf.bonusCriteriaOK  
    f.close()

def writeDefenseSheet(conf, f, defense, criteriaTypes, criterias):
    """ For defense defense, writes a criteria sheet in file f """
    f.write("{}\n{}\n{}\n".format(conf.defenseBound, defense.name, conf.defenseBound))
    for criteriaType in criteriaTypes:
        f.write("{}\n".format(criteriaType))
        for criteria in criterias:
            if criteria.criteriaType == criteriaType:
                f.write("    {}\n".format(criteria.name))
    for opinionType in list_opinions:
        f.write("{}\n\n\n".format(conf.commentBound[opinionType]))

def generateModels(conf, defenses, students, criteriaTypes, criterias):
    """
    Generates models in conf.nominativeSheetsFilename, conf.genericSheetFilename and conf.genericTeacherMarksFilename

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

    Returns
    -------
    void
    """
    #
    # Generate conf.nominativeSheetsFilename
    #
    f = openWithErrorManagement(conf.nominativeSheetsFilename, "w", encoding=conf.encoding)
    for student in students:
        f.write("{}\n{} ({})\n{}\n".format(conf.studentBound, student.name, student.defense.name, conf.studentBound))
        for defense in defenses:
            if defense != student.defense:
                writeDefenseSheet(conf, f, defense, criteriaTypes, criterias)
    f.close()
    
    #
    # Generate conf.genericSheetFilename
    #
    f = openWithErrorManagement(conf.genericSheetFilename, "w", encoding=conf.encoding)
    f.write("{}\n\nNOM Prénom :                                       Soutenance :\n\n{}\n\n".format(conf.studentBound, conf.studentBound))
    for defense in defenses:
        writeDefenseSheet(conf, f, defense, criteriaTypes, criterias)
    f.close()

    #
    # Generate conf.genericTeacherMarksFilename
    #
    f = openWithErrorManagement(conf.genericTeacherMarksFilename, "w", encoding=conf.encoding)
    # Generate the title of the columns
    for defense in defenses:
        f.write("{}{}".format(conf.csvSeparator, str2csvStr(defense.name, conf.csvSeparator)))
    f.write("\n")
    # For each criteria, generate a line for the mark and a line for the comment
    for criteria in criterias:
        s = str2csvStr("Note ({}, {} ou {} points) pour {} / {}".format(
                conf.pointsCriteriaKO, conf.pointsCriteriaAverage, conf.pointsCriteriaOK,
                criteria.criteriaType, criteria.name), conf.csvSeparator)
        f.write(s)
        f.write(conf.csvSeparator * len(defenses))
        f.write("\n");

        s = str2csvStr("Commentaire  de {} / {}".format(criteria.criteriaType, criteria.name), conf.csvSeparator)
        f.write(s)
        f.write(conf.csvSeparator * len(defenses))
        f.write("\n")
        
    f.write(str2csvStr("Ligne inutilisée (par exemple, pour y mettre des totaux)", conf.csvSeparator))
    f.write(conf.csvSeparator * len(defenses))
    f.write("\n");

    f.write(str2csvStr("Commentaires généraux", conf.csvSeparator))
    f.write(conf.csvSeparator * len(defenses))
        
    f.close()

def analyzeTeacherData(conf, defenses, criteriaTypes, criterias):
    """
    Enrich defenses information with the contents of conf.teacherMarksFilename

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
    # Analyze the contents of conf.teacherMarksFilename,
    #
    f = openWithErrorManagement(conf.teacherMarksFilename, "r", encoding=conf.encoding)
    nbLinesRead = [0]

    lookForNonBlankLine(f, nbLinesRead, False, "Ligne de titre des colonnesNom soutenance")  # We ignore the line giving the title of the columns
    # We deal with each criteria
    for criteria in criterias:
        # Read the marks for this criteria
        lineMarks = lookForNonBlankLine(f, nbLinesRead, False, "Ligne contenant les notes pour un critère donné")
        marks = splitCsvLine(lineMarks, conf.csvSeparator)
        # Read the comments for this criteria
        lineComments = lookForNonBlankLine(f, nbLinesRead, False, "Ligne contenant les commentaires pour un critère donné")
        comments = splitCsvLine(lineComments, conf.csvSeparator)
        # Add (mark, comment) to each defense
        column = 1 #We set column to 1 in order to skip column 0 which contains title of the line
        for defense in defenses:
            try:
                mark = int(marks[column])
            except ValueError:
                sys.exit("""Dans le fichier "{}", la soutenance "{}" a son critère "{}" qui a reçu la note "{}" qui n'est ni {}, ni {} ou {}.""".format(
                         f.name, defense.name, criteria.name, marks[column],
                         conf.pointsCriteriaKO, conf.pointsCriteriaAverage, conf.pointsCriteriaOK))                
            if (mark < conf.pointsCriteriaKO or mark > conf.pointsCriteriaOK):
                sys.exit("""Dans le fichier "{}", la soutenance "{}" a son critère "{}" qui a reçu la note de {} qui n'est ni {}, ni {} ou {}.""".format(
                         f.name, defense.name, criteria.name, mark,
                         conf.pointsCriteriaKO, conf.pointsCriteriaAverage, conf.pointsCriteriaOK))
            defense.addMarkComment(TeacherOpinion(mark, comments[column]))
            column += 1

    lookForNonBlankLine(f, nbLinesRead, False, "Ligne de titre des colonnesNom soutenance")  # We ignore the line left intentionally blank

    lineGeneralComments = lookForNonBlankLine(f, nbLinesRead, False, "Ligne contenant les commentaires généraux de chaque projet")
    generalComments = splitCsvLine(lineGeneralComments, conf.csvSeparator)
    column = 1 #We set column to 1 in order to skip column 0 which contains title of the line
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

def generateResults(conf, defenses, students, criteriaTypes, criterias):
    """
    Generates files conf.synthesisCommentsFilename and conf.studentsMarksSheetFilename

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
    # Generate conf.synthesisCommentsFilename
    #
    f = openWithErrorManagement(conf.synthesisCommentsFilename, "w", encoding=conf.encoding)
    for defenseIndex in list(range(len(defenses))):
        # We cound how many '+' and '-' there are for each criteria
        nbPosNeg = [ [], [] ]
        for criteriaIndex in list(range(len(criterias))):
            for opinionType in list_opinions:
                nbPosNeg[opinionType].append([0, criteriaIndex])
        for student in students:
            for opinionType in list_opinions:
                if student.opinionsPerDefense[defenseIndex][opinionType].criteriaIndex >= 0:
                    nbPosNeg[opinionType][student.opinionsPerDefense[defenseIndex][opinionType].criteriaIndex][0] += 1
        # We get a sorted version of nbPositive and nbNegative
        sortedNbPosNeg = [sorted(nbPosNeg[POSITIVE_OPINION], key=itemgetter(0)), sorted(nbPosNeg[NEGATIVE_OPINION], key=itemgetter(0)) ]
        # We display the project name and the general comment on the defense
        f.write("{}\n{}\n{}\n".format(conf.defenseBound, defenses[defenseIndex].name, conf.defenseBound))
        if defenses[defenseIndex].generalComment == "":
            f.write("Pas de commentaire général de {}\n\n".format(conf.teacherName))
        else:
            f.write("Commentaire général de {} : {}\n\n".format(conf.teacherName, defenses[defenseIndex].generalComment))
        # We display the results for positive criteria and negative criteria            
        for opinionType in list_opinions:
            for index in list(range(len(criterias)-1, -1, -1)):
                criteriaIndex = sortedNbPosNeg[opinionType][index][1]
                f.write("({}) Cite {:2} fois par les étudiants : {} - Note {} = {}/{}".format(
                       opinionType2sign[opinionType],
                       sortedNbPosNeg[opinionType][index][0],
                       criterias[criteriaIndex].name,
                       conf.teacherName,
                       defenses[defenseIndex].teacherOpinionsPerCriteria[criteriaIndex].mark,
                       conf.pointsCriteriaOK))
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
    # Generate conf.studentsMarksSheetFilename
    #
    f = openWithErrorManagement(conf.studentsMarksSheetFilename, "w", encoding=conf.encoding)
    f.write("Nom etudiant{}Note donnee par {} a la soutenance{}Bonus opinion{}Note finale module\n".format(
        conf.csvSeparator, conf.teacherName, conf.csvSeparator, conf.csvSeparator))
    for student in students:
        f.write("{}{}{}{}{}{}{}\n".format(
            str2csvStr(student.name, conf.csvSeparator), conf.csvSeparator,
            student.defense.teacherFinalMark, conf.csvSeparator,
            float2str(student.bonus, conf), conf.csvSeparator,
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
    f = openWithErrorManagement(conf.defensesFilename, "r", encoding=conf.encoding)
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
    f = openWithErrorManagement(conf.studentsFilename, "r", encoding=conf.encoding)
    nbLinesRead = [0]
    
    lookForNonBlankLine(f, nbLinesRead, True, "Nom soutenance") # We ignore the line giving the title of the columns
    studentLine = lookForNonBlankLine(f, nbLinesRead, True, "Nom soutenance")
    while studentLine != "":
        info = splitCsvLine(studentLine, conf.csvSeparator)
        # We look for info in the list of defense names
        found = False
        for defense in defenses:
            if info[1] == defense.name:
                # OK, this defense name is known
                students.append(Student(info[0], defense, defenses))
                found = True
                break
        if not found:
            sys.exit("""ERREUR: Dans le fichier "{}", la ligne {} ("{}") fait référence à une soutenance intitulée "{}" qui n'apparaît pas dans le fichier "{}".""".format(conf.studentsFilename, nbLinesRead[0], studentLine, info[1], conf.defensesFilename))
        studentLine = lookForNonBlankLine(f, nbLinesRead, True,  "Nom soutenance")
    f.close()    

    #
    # Read the list of criteria types
    #
    criteriaTypes = []
    f = openWithErrorManagement(conf.criteriaTypesFilename, "r", encoding=conf.encoding)
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
    f = openWithErrorManagement(conf.criteriasFilename, "r", encoding=conf.encoding)
    nbLinesRead = [0]
    
    lookForNonBlankLine(f, nbLinesRead, True, "Nom soutenance") # We ignore the line giving the title of the columns
    criteriaLine = lookForNonBlankLine(f, nbLinesRead, True, "Nom soutenance")
    while criteriaLine != "":
        info = splitCsvLine(criteriaLine, conf.csvSeparator)
        # We look for info[0] in the list of criteria types
        found = False
        for criteriaType in criteriaTypes:
            if info[0] == criteriaType:
                found = True
                break
        if not found:
            sys.exit("""ERREUR: Dans fichier "{}", la ligne {} ("{}") fait référence à un type de critère intitulée "{}" qui n'apparaît pas dans le fichier "{}".""".format(conf.criteriasFilename, nbLinesRead[0], criteriaLine, info[0], conf.criteriaTypesFilename))
        # OK, this citeriaType is known
        criterias.append(Criteria(info[0], info[1]))
        criteriaLine = lookForNonBlankLine(f, nbLinesRead, True, "Nom soutenance")
    f.close()
    
    #
    # Remaining work depends on what the user asks for
    #
    if sys.argv[1][1] == '1':
        generateModels(conf, defenses, students, criteriaTypes, criterias);
    else:
        analyzeTeacherData(conf, defenses, criteriaTypes, criterias);
        analyzeStudentsData(conf, defenses, students, criteriaTypes, criterias);
        generateResults(conf, defenses, students, criteriaTypes, criterias);

    #
    # We display an end of execution message
    #
    if sys.argv[1][1] == '1':
        print("""OK, exécution de la phase {} terminée : les fichiers "{}", "{}" et "{}" ont été générés.""".format(
                sys.argv[1][1],
                conf.nominativeSheetsFilename, conf.genericSheetFilename, conf.genericTeacherMarksFilename))
    else:
        print("""OK, exécution de la phase {} terminée : les fichiers "{}" et "{}" ont été générés.""".format(
                sys.argv[1][1],
                conf.synthesisCommentsFilename, conf.studentsMarksSheetFilename))
    print()
    
    return

# Main entry point of the program
main()
