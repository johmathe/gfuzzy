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


"""The class representing the fuzzy engine itself."""


import consequent
import fuzzy_config
import sys_input
import membership
import sys_output
import rule


class System(object):
  """Class defining a Fuzzy System."""

  def __init__(self):
    self.rules = {}
    self.sets = {}
    self.outputs = {}
    self.inputs = {}
    self.consequents = {}
    self.elements_mapping = {}

  def _EvaluateRules(self):
    """Apply fuzzy rules."""
    for r in self.rules:
      self.rules[r].Evaluate(self.elements_mapping)

  def _Aggregate(self):
    """Aggregate truth values."""
    for c in self.consequents:
      self.consequents[c].Aggregate()

  def _Defuzzify(self):
    """Defuzzify to output data."""
    for o in self.outputs:
      self.outputs[o].Defuzzify()

  def LoadConfig(self, filename):
    """Load fuzzy configuration."""
    sys = fuzzy_config.ReadConfig(filename)

    for p_input in sys.input:
      name = p_input.name
      input_ = sys_input.Input(name)
      self.inputs[name] = input_
      self.elements_mapping[name] = input_

    for p_set in sys.set:
      name = p_set.name
      fset = membership.CreateSet(p_set.type, name, p_set.param)
      self.sets[name] = fset
      self.elements_mapping[name] = fset

    for p_output in sys.output:
      name = p_output.name
      self.outputs[name] = sys_output.Output(name)

    for p_consequent in sys.consequent:
      name = p_consequent.name
      consequent_ = consequent.Consequent(self.sets[p_consequent.set])
      self.consequents[name] = consequent_
      self.outputs[p_consequent.output].consequents.append(consequent_)

    for p_rule in sys.rule:
      name = p_rule.name
      rule_ = rule.Rule(p_rule.antecedent)
      self.rules[name] = rule_
      # mapping the consequent associated to the rule
      self.consequents[p_rule.consequent].rules.append(rule_)

  def UpdateValues(self, variables):
    """Updates the whole fuzzy system."""
    # Constructs the input argument
    for d in variables:
      self.inputs[d].data = variables[d]

    self._EvaluateRules()
    self._Aggregate()
    self._Defuzzify()
    self.results = {}

    for o in self.outputs:
      self.results[o] = self.outputs[o].value

    self.variables = {}

    for o in self.outputs:
      self.variables[o] = dict([(c.fset.name, c.output.data)
                                for c in self.outputs[o].consequents])
