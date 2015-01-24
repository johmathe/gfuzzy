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


"""Tests for gfuzzy.system."""


import csv
import unittest
import system


class SystemTest(unittest.TestCase):

  def setUp(self):
    self.system = system.System()
    self.system.LoadConfig('testdata/test_config.protoascii')

  def testUpdate(self):
    i = {'cpu': [1, 0.5, 0.6],
         'ram': [1, 1, 0.5]}
    self.system.UpdateValues(i)
    res = self.system.results.copy()
    self.assertAlmostEquals(0, res['health'][0])
    self.assertAlmostEquals(0, res['health'][1])
    self.assertAlmostEquals(0.5, res['health'][2])

  def testFeedSurface(self):
    xpath = 'testdata/x'
    ypath = 'testdata/y'

    x = []
    y = []
    csvread = csv.reader(open(xpath), delimiter=',')
    for row in csvread:
      for v in row:
        x.append(float(v))

    csvread2 = csv.reader(open(ypath), delimiter=',')
    for row in csvread2:
      for v in row:
        y.append(float(v))
    inpt = {'cpu': x, 'ram': y}
    res = self.system.UpdateValues(inpt)
    #self.writer = open('csv_output', 'w')
    #for v in res['health']:
    #  self.writer.write('%f,' % v)
    #self.writer.close()

if __name__ == '__main__':
  unittest.main()
