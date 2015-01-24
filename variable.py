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


"""Class representing a fuzzy variable."""


class Variable(object):
  """Class representing a fuzzy variable."""

  def __init__(self, data):
    self.data = data

  def __and__(self, c):
    if type(c) is Variable:
      return Variable([min(self.data[i], c.data[i]) for i in
                       range(len(self.data))])
    else:
      return Variable([min(self.data[i], c) for i in
                       range(len(self.data))])

  def __or__(self, c):
    if type(c) is Variable:
      return Variable([max(self.data[i], c.data[i]) for i in
                       range(len(self.data))])
    else:
      return Variable([max(self.data[i], c) for i in
                       range(len(self.data))])

  def __mul__(self, c):
    if type(c) is Variable:
      return Variable([self.data[i] * c.data[i] for i in
                       range(len(self.data))])
    else:
      return Variable([self.data[i] * c for i in
                       range(len(self.data))])

  def __add__(self, c):
    if type(c) is Variable:
      return Variable([self.data[i] + c.data[i] - self.data[i] * c.data[i]
                       for i in range(len(self.data))])
    else:
      return Variable([self.data[i] + c - self.data[i] * c
                       for i in range(len(self.data))])

  def __getitem__(self, i):
    return self.data[i]

  def __len__(self):
    return len(self.data)

  def Is(self, fset):
    return Variable([fset.membership_function.Evaluate(x)
                     for x in self.data])

  def IsNot(self, fset):
    return Variable([1.0 - fset.membership_function.Evaluate(x)
                     for x in self.data])
