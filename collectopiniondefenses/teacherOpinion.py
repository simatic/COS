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
from criteria import Criteria
from student import POSITIVE_OPINION, AVERAGE_OPINION, NEGATIVE_OPINION

class TeacherOpinion:
    """ Class holding all data concerning opinion of a teacher on a given criteria """

    def __init__(self, mark, comment, criteria):
        self.mark= mark
        self.comment= comment
        # We initialize self.opinionType
        if mark <= criteria.maxCriteriaKO:
            self.opinionType = NEGATIVE_OPINION
        elif mark >= criteria.minCriteriaOK:
            self.opinionType = POSITIVE_OPINION
        else:
            self.opinionType = AVERAGE_OPINION        

    def __str__(self):
        return "TeacherOpinion({}, {})".format(self.mark, self.comment)

