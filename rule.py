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


"""This module implements rules of the fuzzy engine."""


import re


def Interpret(s):
  """Interpret a rule to terms that can be evaluated by Python.

  The terms for the fuzzy logic system are of the form:

  <variable> is <adjective>
  <variable> is not <adjective>

  Such terms are joined with operators *, +, |, & and grouped with
  parantheses. The final expression will be evaluated by Python,
  but the terms need to be interpreted into proper function calls.

  This function will replace terms like:

  <variable> is <adjective>

  with

  <variable>.Is(<adjective>

  and terms like

  <variable> is not <adjective>

  with

  <variable>.IsNot(<adjective>)

  In addition, since it is more natural to type 'and' and 'or' in the rules
  rather than the operators '&' and '|', it will replace 'and' with '&' and
  'or' with '|'. This is done because the latter can be overriden while the
  former can not.

  Args:
    s: The string to be interpreted

  Returns:
    the interpreted string

  """
  tokens = re.findall('\*|\||&|\+|\)|\(|[_\w]+', s)
  size = len(tokens)
  old_size = size + 1

  for i in range(size):
    if tokens[i].lower() == 'and':
      tokens[i] = '&'
    elif tokens[i].lower() == 'or':
      tokens[i] = '|'

  while size < old_size:
    for i in range(1, size-1):
      if tokens[i].lower() == 'is':
        if tokens[i+1].lower() == 'not':

          if i == size - 2:
            break

          new_term = tokens[i-1] + '.IsNot(' + tokens[i+2] + ')'
          tokens[i-1] = new_term
          del tokens[i:i+3]
          break
        else:
          new_term = tokens[i-1] + '.Is(' + tokens[i+1] + ')'
          tokens[i-1] = new_term
          del tokens[i:i+2]
          break

    old_size = size
    size = len(tokens)

  return ' '.join(tokens)


class Rule(object):
  """A class representing a fuzzy rule."""

  def __init__(self, antecedent, weight=1.0):
    self.__SetAntecedent(antecedent)
    self.weight = weight
    self.output = None

  def _CalculateAntecedent(self):
    raise NotImplementedError('Method not ready')

  def Evaluate(self, variables):
    self.output = self._CalculateAntecedent(variables) * self.weight

  def __SetAntecedent(self, antecedent):
    self.antecedent = antecedent
    self.interpreted_antecedent = Interpret(antecedent)
    self._CalculateAntecedent = lambda g: eval(self.interpreted_antecedent, g)
