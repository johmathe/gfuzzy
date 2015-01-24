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


"""Module implementing memberhsip functions and sets."""


EPSILON = 1e-10


class MembershipFunction(object):
  """Base class for a membership function."""

  def __init__(self):
    pass

  def Evaluate(self, argument):
    """Evaluates the membership function at the given point.

     This must be implemented by subclasses.

    Args:
      argument: point at which the function will be evaluated

    Returns:
      the value of the function for the given argument
    """
    raise NotImplementedError

  def GetArea(self, truth_value):
    """Computes the area under the y truth value in the mship fx.

    Args:
      truth_value: value under which area is calculated

    Returns:
      area under the y truth value
    """
    raise NotImplementedError

  def GetCentroidXAbscissa(self, truth_value):
    """Computes the X Abscissa of the Centroid value.

    The centroid is the one of the area under the truth value.

    Args:
      truth_value: value under which area is calculated

    Returns:
      X Abscissa of the Centroid value.
    """
    raise NotImplementedError


class RectangularMF(MembershipFunction):
  """Triangular membership function."""

  def __init__(self, params):
    """Create a rectangular membership function.

    Args:
      params: list of parameters, must contain two numbers.
    """
    MembershipFunction.__init__(self)
    self.__SetParams(params)

  def __SetParams(self, params):
    """Private function to set the parameters.

    This will perform sanity checks on the parameters.
    It will require an iterable of length 2. If not, it
    will raise an exception.

    Args:
      params: An iterable of 2 numbers

    Raises:
      AssertionError if length of the iterable is not 2
      ValueError if members of iterable are not castable to float
      TypeError if params is not an iterable
    """
    assert len(params) == 2, 'params length is not 2'
    self.params = [float(x) for x in params]
    assert self.params[0] < self.params[1], 'params not sorted'

  def Evaluate(self, argument):
    """Evaluate the rectangular membership function."""
    if argument <= self.params[0] or argument >= self.params[1]:
      return 0.0
    else:
      return 1.0

  def GetArea(self, truth_value):
    """Computes the area under the y truth value in the mship fx.

    Args:
      truth_value: value under which area is calculated

    Returns:
      area under the y truth value
    """
    return truth_value * (self.params[1] - self.params[0])

  def GetCentroidXAbscissa(self, truth_value):
    """Computes the X Abscissa of the Centroid value.

    The centroid is the one of the area under the truth value.

    Args:
      truth_value: value under which area is calculated

    Returns:
      X Abscissa of the Centroid value.
    """
    return (self.params[0] + self.params[1]) / 2


class TriangularMF(MembershipFunction):
  """Triangular membership function."""

  def __init__(self, params):
    """Create a triangular membership function.

    Args:
      params: list of parameters, must contain three numbers.
    """
    MembershipFunction.__init__(self)
    self.__SetParams(params)

  def __SetParams(self, params):
    """Private function to set the parameters.

    This will perform sanity checks on the parameters.
    It will require an iterable of length 3. If not, it
    will raise an exception.

    Args:
      params: An iterable of 3 numbers

    Raises:
      AssertionError if length of the iterable is not 3
      ValueError if members of iterable are not castable to float
      TypeError if params is not an iterable
    """
    assert len(params) == 3, 'params length is not 3'
    self.params = [float(x) for x in params]
    assert (self.params[0] < self.params[1] and
            self.params[1] < self.params[2]), 'params not sorted'

  def Evaluate(self, argument):
    """Evaluate the triangular membership function."""
    if argument <= self.params[0] or argument >= self.params[2]:
      return 0.0

    if argument <= self.params[1]:
      return (argument - self.params[0])/(self.params[1] - self.params[0])
    else:
      return (self.params[2] - argument)/(self.params[2] - self.params[1])

  def GetArea(self, truth_value):
    """Computes the area under the y truth value in the mship fx.

    Args:
      truth_value: value under which area is calculated

    Returns:
      area under the y truth value
    """
    # Need a copy of self.params here, since we modify x later.
    x = self.params[:]
    T = truth_value

    # Let's get the same vector as a trapezoid (x2 = x3)
    x.append(x[2])
    x[2] = x[1]

    P1 = x[0] + T * (x[1]-x[0])
    P2 = x[3] - T * (x[3]-x[2])

    Sr = T * (P2-P1)
    St1 = T * (P1-x[0])/2
    St2 = T * (x[3] - P2)/2

    return St1 + St2 + Sr

  def GetCentroidXAbscissa(self, truth_value):
    """Computes the X Abscissa of the Centroid value.

    The centroid is the one of the area under the truth value.

    Args:
      truth_value: value under which area is calculated

    Returns:
      X Abscissa of the Centroid value.
    """
    # Need a copy of self.params here, since we modify x later.
    x = self.params[:]
    T = truth_value

    # Let's get the same vector as a trapezoid (x2 = x3)
    # we get the same case here that the trapezoid computation.
    x.append(x[2])
    x[2] = x[1]

    P1 = x[0] + T * (x[1]-x[0])
    P2 = x[3] - T * (x[3]-x[2])

    Xr = (P1 + P2)/2
    Sr = T * (P2-P1)

    Xt1 = P1 - (P1-x[0])/3
    St1 = T * (P1-x[0])/2

    Xt2 = P2 + (x[3] - P2)/3
    St2 = T * (x[3] - P2)/2

    area = St1 + St2 + Sr

    if area < EPSILON:
      Xcentroid = (x[3] - x[0])/2
    else:
      Xcentroid = (Xt1*St1 + Xt2*St2 + Xr*Sr) / area

    return Xcentroid


class TrapezoidalMF(MembershipFunction):
  """Triangular membership function."""

  def __init__(self, params):
    """Create a trapezoidal membership function.

    Args:
      params: list of parameters, must contain four numbers.
    """
    MembershipFunction.__init__(self)
    self.__SetParams(params)

  def __SetParams(self, params):
    """Private function to set the parameters.

    This will perform sanity checks on the parameters.
    It will require an iterable of length 4. If not, it
    will raise an exception.

    Args:
      params: An iterable of 4 numbers

    Raises:
      AssertionError if length of the iterable is not 4
      ValueError if members of iterable are not castable to float
      TypeError if params is not an iterable
    """
    assert len(params) == 4, 'params length is not 4'
    self.params = [float(x) for x in params]
    assert (self.params[0] < self.params[1] and
            self.params[1] <= self.params[2] and
            self.params[2] < self.params[3]), 'params not sorted'

  def Evaluate(self, argument):
    """Evaluate the trapezoidal membership function."""
    if argument <= self.params[0] or argument >= self.params[3]:
      return 0.0

    if argument <= self.params[2] and argument >= self.params[1]:
      return 1.0

    if argument <= self.params[1]:
      return (argument - self.params[0])/(self.params[1] - self.params[0])
    else:
      return (self.params[3] - argument)/(self.params[3] - self.params[2])

  def GetArea(self, truth_value):
    """Computes the area under the y truth value in the mship fx.

    Args:
      truth_value: value under which area is calculated

    Returns:
      area under the y truth value
    """
    x = self.params
    T = truth_value

    P1 = x[0] + T * (x[1]-x[0])
    P2 = x[3] - T * (x[3]-x[2])

    Sr = T * (P2-P1)
    St1 = T * (P1-x[0])/2
    St2 = T * (x[3] - P2)/2

    return St1 + St2 + Sr

  def GetCentroidXAbscissa(self, truth_value):
    """Computes the X Abscissa of the Centroid value.

    The centroid is the one of the area under the truth value.

    Args:
      truth_value: value under which area is calculated

    Returns:
      X Abscissa of the Centroid value.
    """
    x = self.params
    T = truth_value

    P1 = x[0] + T * (x[1]-x[0])
    P2 = x[3] - T * (x[3]-x[2])

    Xr = (P1 + P2)/2
    Sr = T * (P2-P1)

    Xt1 = P1 - (P1-x[0])/3
    St1 = T * (P1-x[0])/2

    Xt2 = P2 + (x[3] - P2)/3
    St2 = T * (x[3] - P2)/2

    area = St1 + St2 + Sr

    if area < EPSILON:
      Xcentroid = (x[3] - x[0])/2
    else:
      Xcentroid = (Xt1*St1 + Xt2*St2 + Xr*Sr) / area

    return Xcentroid


mf_dictionary = {'triangular': TriangularMF,
                 'trapezoidal': TrapezoidalMF,
                 'rectangular': RectangularMF}


class Set(object):
  def __init__(self, name, membership_function):
    self.name = name
    self.membership_function = membership_function


def CreateSet(ftype, name, params):
  try:
    clazz = mf_dictionary[ftype]
  except KeyError:
    raise NotImplementedError('Function %s not implemented!' % ftype)

  return Set(name, clazz(params))
