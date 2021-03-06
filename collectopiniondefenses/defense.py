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

class Defense:
    """ Class holding all defense data """
    
    def __init__(self, name):
        self.generalComment = ""
        self.name = name
        self.nameWithoutSpace = self.name.replace(" ", "")
        self.teacherFinalMark = 0
        self.teacherOpinionsPerCriteria = []
        self.teacherWorstOpinionType = sys.maxsize
        self.teacherBestOpinionType  = -sys.maxsize
    
    def addMarkComment(self, teacherOpinion):
        self.teacherOpinionsPerCriteria.append(teacherOpinion)
    
    def update(self):
        """ Updates teacherFinalMark, bestMark and worstmark """
        for opinion in self.teacherOpinionsPerCriteria:
            self.teacherFinalMark += opinion.mark
            self.teacherWorstOpinionType = min(self.teacherWorstOpinionType, opinion.opinionType)
            self.teacherBestOpinionType  = max(self.teacherBestOpinionType,  opinion.opinionType)
        
