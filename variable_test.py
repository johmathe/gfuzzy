#!/usr/bin/python2.6
#
# GFuzzy - A fuzzy engine written in python.
#
# Copyright 2010 Google Inc. All Rights Reserved.
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


"""Tests for gfuzzy.variable."""


import unittest
import variable


class MockFunction(object):
  """Defining a mock function."""

  def Evaluate(self, x):
    return x


class MockSet(object):
  """Defining a mock set."""

  membership_function = MockFunction()
  name = 'mock'


class VariableTest(unittest.TestCase):

  def assertVariableAlmostEquals(self, x, y):
    self.assertEquals(len(x), len(y))
    for i in range(0, len(x)):
      self.assertAlmostEquals(x[i], y[i])

  def setUp(self):
    self.x = variable.Variable([1.0, 0.5, 0.2, 0.0])
    self.y = variable.Variable([0.0, 0.1, 0.4, 0.9])

    self.set = MockSet()

  def tearDown(self):
    pass

  def testVariable_add(self):
    expected = [1.0, 0.55, 0.52, 0.9]
    z = self.x + self.y
    self.assertVariableAlmostEquals(expected, z)

  def testVariable_addConstant(self):
    expected = [1.0, 0.6, 0.36, 0.2]
    z = self.x + 0.2
    self.assertVariableAlmostEquals(expected, z)

  def testVariable_and(self):
    expected = [0.0, 0.1, 0.2, 0.0]
    z = self.x & self.y
    self.assertVariableAlmostEquals(expected, z)

  def testVariable_andConstant(self):
    expected = [0.4, 0.4, 0.2, 0.0]
    z = self.x & 0.4
    self.assertVariableAlmostEquals(expected, z)

  def testVariable_or(self):
    expected = [1.0, 0.5, 0.4, 0.9]
    z = self.x | self.y
    self.assertVariableAlmostEquals(expected, z)

  def testVariable_orConstant(self):
    expected = [1.0, 0.6, 0.6, 0.6]
    z = self.x | 0.6
    self.assertVariableAlmostEquals(expected, z)

  def testVariable_mul(self):
    expected = [0.0, 0.05, 0.08, 0.0]
    z = self.x * self.y
    self.assertVariableAlmostEquals(expected, z)

  def testVariable_mulConstant(self):
    expected = [0.5, 0.25, 0.1, 0.0]
    z = self.x * 0.5
    self.assertVariableAlmostEquals(expected, z)

  def testVariable_len(self):
    self.assertEquals(4, len(self.x))

  def testVariable_get(self):
    self.assertAlmostEquals(1.0, self.x[0])
    self.assertAlmostEquals(0.5, self.x[1])
    self.assertAlmostEquals(0.2, self.x[2])
    self.assertAlmostEquals(0.0, self.x[3])

  def testVariable_is(self):
    z = self.x.Is(self.set)
    self.assertVariableAlmostEquals(self.x, z)

  def testVariable_isNot(self):
    expected = [0.0, 0.5, 0.8, 1.0]
    z = self.x.IsNot(self.set)
    self.assertVariableAlmostEquals(expected, z)


if __name__ == '__main__':
  unittest.main()
