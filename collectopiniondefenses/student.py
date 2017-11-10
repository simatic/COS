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

from studentOpinion import StudentOpinion

NEGATIVE_OPINION = 0
AVERAGE_OPINION  = 1
POSITIVE_OPINION = 2
# Array list_opinions lists only opinions which can be given by the student
list_opinions = (POSITIVE_OPINION, NEGATIVE_OPINION)

class Student:
    """ Class holding all student data """

    def __init__(self, name, defense, defenses):
        self.alreadyProcessed = False
        self.bonus = 0.0
        self.defense = defense
        self.name = name
        self.nameWithoutSpace = self.name.replace(" ", "")
        self.opinionsPerDefense = []
        for defense in defenses:
            self.opinionsPerDefense.append([StudentOpinion(), None, StudentOpinion()]) # None value is because student
                                                                                       # cannot give an average opinion

