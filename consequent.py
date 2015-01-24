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


"""Defines the consequent of a rule."""


class Consequent(object):
  """Defines a consequent of a rule."""

  def __init__(self, fset):
    """Initialization of consequent.

    Args:
      fset: reference to a fuzzy set.
      rules: list of rules which have this consequent.
    """
    self.fset = fset
    self.rules = []
    self.output = None

  def Aggregate(self):
    """Aggregates of the truth values with max method."""
    # Loop over all the inputs. Use the overriden | operator
    # in Variable to take the maxiumum of all rules which
    # are inputs to this consequent.
    self.output = self.rules[0].output

    for i in range(1, len(self.rules)):
      self.output |= self.rules[i].output
