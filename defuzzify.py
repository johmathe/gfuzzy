#!/usr/bin/python2.6
#
# GFuzzy - A fuzzy engine written in python.
#
# Copyright 2011 Google Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Module for the defuzzification process.

Defuzzification is done only using center of gravity method.
"""


import membership


def Defuzzify(truth_values):
  """Defuzzification function.

  Args:
    truth_values: list of tuples (set, truth_value)
  Returns:
    deffuzified value
  """
  areas = [s[0].membership_function.GetArea(s[1]) for s in truth_values]
  area_total = sum(areas)
  xcentroids = [s[0].membership_function.GetCentroidXAbscissa(s[1])
               for s in truth_values]
  v = 0

  # if area total is zero, we return an average of the centroid abiscas :
  if area_total > membership.EPSILON:
    for i in range(len(areas)):
      v += xcentroids[i] * areas[i]

    v /= area_total
  else:
    v = sum(xcentroids) / len(xcentroids)

  return v
