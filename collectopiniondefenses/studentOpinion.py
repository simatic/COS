# -*- coding: utf8 -*-

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

class StudentOpinion:
    """ Class holding all data concerning opinion (positive or negative) of a student concerning a defence """

    def __init__(self):
        self.criteriaIndex= -1
        self.nbCriteriaIndex = 0 # Counts how many times a student gave an positive (or negative) opinion on a defense
        self.comment= ""

    def __str__(self):
        return "StudentOpinion({}, {})".format(self.criteriaIndex, self.comment)
