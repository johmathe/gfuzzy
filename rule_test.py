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


"""Tests for gfuzzy.rule."""


import unittest
import rule


class _FakeSet(object):
  """Fake fuzzy set."""


class _FakeVariable(object):
  """Fake variable."""

  def Is(self, fset):
    self.fset = fset
    return 0.4


class InterpreterTest(unittest.TestCase):

  def testInterpreter_parseIsExpression(self):
    self.assertEquals('a.Is(b)', rule.Interpret('a is b'))

  def testInterpreter_parseIsNotExpressions(self):
    self.assertEquals('a.IsNot(b)', rule.Interpret('a is not b'))

  def testInterpreter_parseMixedExpressions(self):
    self.assertEquals('( a.IsNot(b) ) | c.Is(d) & e.Is(f)',
                      rule.Interpret('(a is not b) or c is d and e is f'))


class RuleTest(unittest.TestCase):

  def setUp(self):
    self.vars = {'x': 6, 'y': 4}

  def tearDown(self):
    pass

  def testRule_Evaluate(self):
    add = rule.Rule('x + y')
    add.Evaluate(self.vars)
    self.assertEquals(10, add.output)

  def testRule_Weight(self):
    dummy_rule = rule.Rule('dummy', 0.5)
    # Mocking the _CalculateAntecedent function:
    dummy_rule._CalculateAntecedent = lambda x: x + 2.0
    dummy_rule.Evaluate(4.0)

    self.assertAlmostEquals(3.0, dummy_rule.output)

  # TODO(johmathe): Get rid of this
  #def testRule_Evaluate_and(self):
  #  xset = _FakeSet()
  #  yset = _FakeSet()
  #  self.varsand = {'a': _FakeVariable(),
  #                  'b': _FakeVariable(),
  #                  'xset': xset,
  #                  'yset': yset }
  #  andrule = rule.Rule('a is xset and b is yset')
  #  andrule.Evaluate(self.varsand)
  #  self.assertAlmostEquals(andrule.output, 0.4)


if __name__ == '__main__':
  unittest.main()
