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


"""Output of the fuzzy engine."""


import defuzzify


class Output(object):
  """Object representing output of the fuzzy engine."""

  def __init__(self, name):
    self.name = name
    self.value = None
    self.consequents = []

  def Defuzzify(self):
    """Defuzzify outputs of the consequents and produce the output values."""
    # TODO(johmathe): assert all the consequents have the same amount of truth
    # values
    consequent1 = self.consequents[0]
    results = []
    for i in range(len(consequent1.output.data)):
      defuzzify_params = [(c.fset, c.output[i]) for c in
                          self.consequents]
      results.append(defuzzify.Defuzzify(defuzzify_params))

    self.value = results
