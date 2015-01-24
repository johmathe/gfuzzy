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


"""Tests for gfuzzy.membership."""


import unittest
import membership


class MembershipTest(unittest.TestCase):
  """Test the membership functions for sanity and evaluation."""

  def setUp(self):
    """Set up the membership functions for evaluations tests."""
    self.triangular_mf = membership.TriangularMF([0.0, 0.5, 1.0])
    self.trapezoidal_mf = membership.TrapezoidalMF([0.0, 1.0, 2.0, 3.0])
    self.rectangular_mf = membership.RectangularMF([-2, 2])

  def tearDown(self):
    """Teardown. Nothing to do here."""
    pass

  def testMembershipFunction_evaluateFails(self):
    """Tests that the base class Evaluate fails."""
    mf = membership.MembershipFunction()
    self.assertRaises(NotImplementedError, mf.Evaluate, 1)

  def testTriangularMF_floatParameters(self):
    """Tests that proper instantiation works."""
    membership.TriangularMF([0.1, 0.5, 1.0])

  def testTriangularMF_intParameters(self):
    """Tests that integers work since they are castable to float."""
    membership.TriangularMF([1, 5, 10])

  def testTriangularMF_wrongParameterCount(self):
    """Tests that wrong number of parameters raises AssertionError."""
    self.assertRaises(AssertionError,
                      membership.TriangularMF,
                      [1, 5, 10, 12])

  def testTriangularMF_badParameterType(self):
    """Tests that incorrect parameter type raises ValueError."""
    self.assertRaises(ValueError,
                      membership.TriangularMF,
                      ['a', 'b', 'c'])

  def testTriangularMF_badParameter(self):
    """Tests that passing a non-iterable type raises TypeError."""
    self.assertRaises(TypeError, membership.TriangularMF, 1)

  def testTriangularMF_evaluateLeftZero(self):
    """Tests that a value on the far left evaluate to zero."""
    self.assertAlmostEquals(0.0, self.triangular_mf.Evaluate(-1.0))

  def testTriangularMF_evaluateLeftRamp(self):
    """Tests that a value on the left ramp evaluates correctly."""
    self.assertAlmostEquals(0.4, self.triangular_mf.Evaluate(0.2))

  def testTriangularMF_evaluateRightRamp(self):
    """Tests that a value on the right ramp evaluates correctly."""
    self.assertAlmostEquals(0.8, self.triangular_mf.Evaluate(0.6))

  def testTriangularMF_evaluateRightZero(self):
    """Tests that a values on the far right evaluates to zero."""
    self.assertAlmostEquals(0.0, self.triangular_mf.Evaluate(2.0))

  def testTriangularMF_invariantCentroid(self):
    t = 1.0

    while t > 0.0:
      self.assertAlmostEquals(0.5, self.triangular_mf.GetCentroidXAbscissa(t))
      t /= 2.0

  def testTrapezoidalMF_floatParameters(self):
    """Tests that proper instantiation works."""
    membership.TrapezoidalMF([0.1, 0.5, 1.0, 1.5])

  def testTrapezoidalMF_intParameters(self):
    """Tests that instantiation works with integral parameters."""
    membership.TrapezoidalMF([1, 5, 10, 15])

  def testTrapezoidalMF_wrongParameterCount(self):
    """Tests that incorrect number of parameters raises AssertionError."""
    self.assertRaises(AssertionError, membership.TrapezoidalMF, [1, 5, 10])

  def testTrapezoidalMF_badParameterType(self):
    """Tests that bad parameter type raises ValueError."""
    self.assertRaises(ValueError,
                      membership.TrapezoidalMF,
                      ['a', 'b', 'c', 'd'])

  def testTrapezoidalMF_badParameter(self):
    """Tests that non-iterable type raises a TypeError."""
    self.assertRaises(TypeError, membership.TrapezoidalMF, 1)

  def testTrapezoidalMF_evaluateLeftZero(self):
    """Tests that a value on the far left evaluates to zero."""
    self.assertAlmostEquals(0.0, self.trapezoidal_mf.Evaluate(-1.0))

  def testTrapezoidalMF_evaluateLeftRamp(self):
    """Tests that a value on the left ramp evaluates correctly."""
    self.assertAlmostEquals(0.4, self.trapezoidal_mf.Evaluate(0.4))

  def testTrapezoidalMF_evaluateRightRamp(self):
    """Tests that a value on the right ramp evaluates correctly."""
    self.assertAlmostEquals(0.8, self.trapezoidal_mf.Evaluate(2.2))

  def testTrapezoidalMF_evaluateRightZero(self):
    """Tests that a value on the far right evaluates to zero."""
    self.assertAlmostEquals(0.0, self.trapezoidal_mf.Evaluate(4.0))

  def testTrapezoidalMF_evaluateCenterOne(self):
    """Tests that a value in the center evaluates to one."""
    self.assertAlmostEquals(1.0, self.trapezoidal_mf.Evaluate(1.5))

  def testRectangularMF_evaluateLeftZero(self):
    """Tests that a value on the far left evaluates to zero."""
    self.assertAlmostEquals(0.0, self.rectangular_mf.Evaluate(-2.1))

  def testRectangularMF_evaluateRightZero(self):
    """Tests that a value on the far left evaluates to zero."""
    self.assertAlmostEquals(0.0, self.rectangular_mf.Evaluate(2.1))

  def testRectangularMF_evaluateCenterOne(self):
    """Tests that a value on the far left evaluates to zero."""
    self.assertAlmostEquals(1.0, self.rectangular_mf.Evaluate(0.3))

  def testCreateSet_triangular(self):
    """Tests that a triangular membership function can be created."""
    membership.CreateSet('triangular', 'triangle', [0.5, 1.5, 2.5])

  def testCreateSet_trapezoidal(self):
    """Tests that a trapezoidal membership function set can be created."""
    membership.CreateSet('trapezoidal', 'triangle', [0.5, 1.5, 2.5, 3.5])

  def testCreateSet_notImplemented(self):
    """Tests that a non-implemented set can't be created."""
    self.assertRaises(NotImplementedError,
                      membership.CreateSet,
                      'dombilical', 'dombili',
                      [0.5, 1.5, 2.5, 3.5])

  def testGetArea_triangular(self):
    """Tests the getArea method for a triangular MFx."""
    self.assertAlmostEquals(0.375, self.triangular_mf.GetArea(0.5))

  def testGetArea_triangular_0truth(self):
    """Tests if the getarea returns 0 for a 0 truth value."""
    self.assertEquals(0, self.triangular_mf.GetArea(0))

  def testGetArea_trapezoidal(self):
    """Tests the getArea method for a triangular MFx."""
    self.assertAlmostEquals(1.25, self.trapezoidal_mf.GetArea(0.5))

  def testGetArea_trapezoidal_0truth(self):
    """Tests if the getarea returns 0 for a 0 truth value."""
    self.assertEquals(0, self.trapezoidal_mf.GetArea(0))


if __name__ == '__main__':
  unittest.main()
