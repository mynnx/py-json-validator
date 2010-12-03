#!/usr/bin/env python2.6

import unittest
import sys; sys.path.append('../src')
from jsonvalidator import validate, ValidationError

# Example validator functions
def evenNumber(number):
    if number % 2 != 0:
        raise ValidationError("%d is not an even number" % number)

def greaterThanSeven(number):
    if number <= 7:
        raise ValidationError("%d is not greater than 7" % number)


class ValidationTest(unittest.TestCase):
    def _check(self, schema, accepted, rejected):
        for case in accepted:
            try:
                validate(case, schema)
            except ValidationError, exc:
                error = "Valid data was rejected: %s\nReason:%s"
                raise AssertionError(error % (format(case), exc))

        for case in rejected:
            try:
                validate(case, schema)
                error = "Invalid data was accepted: %s"
                raise AssertionError(error % format(case))
            except ValidationError:
                pass

class ValueTest(ValidationTest):
    def testOptional(self):
        schema = { 'one?' : (basestring,) }

        accepted = [
            { 'one' : '' },
            {  }
        ]

        rejected = [
            { 'one': None },
        ]

        self._check(schema, accepted, rejected)

    def testRequired(self):
        schema = { 'one' : (basestring, ) }

        accepted = [
            { 'one' : '' },
        ]

        rejected = [
            {  },
            { 'one' : None },
            { 'two' : '' },
        ]

        self._check(schema, accepted, rejected)

    def testOneRequiredOneOptional(self):
        schema = {
            'one' : (basestring, ),
            'two?' : (basestring, )
        }

        accepted = [
            { 'one' : '' },
            { 'one' : '', 'two' : '' },
            { 'one' : '', 'three' : '' },
        ]

        rejected = [
            { 'one' : 5 },
            { 'two' : '' },
            { 'one' : None, 'two' : '' },
            { 'one' : '', 'two' : None },
        ]

        self._check(schema, accepted, rejected)

class ListTest(ValidationTest):
    def testSimpleList(self):
        schema = { 'one': [ (basestring, ) ] }

        accepted = [
            {'one' : ['x'] },
            {'one' : ['x', 'y'] },
        ]

        rejected = [
            {'one' : [ ] },
            {'one' : [5] },
            {'one' : ['x', 5] },
        ]

        self._check(schema, accepted, rejected)

    def testListCanBeEmpty(self):
        schema = { 'one': [ (basestring, ), None ] }

        accepted = [
            {'one' : [ ] },
            {'one' : ['x'] },
            {'one' : ['x', 'y'] },
        ]

        rejected = [
            {'one' : [5] },
            {'one' : ['x', 5] },
        ]

        self._check(schema, accepted, rejected)

class NestingTest(ValidationTest):
    def testSimpleNest(self):
        schema = {
            'one' : {
                'two' : (basestring, )
            }
        }

        accepted = [
            { 'one' : { 'two' : 'three' }}
        ]

        rejected = [
            { 'one' : 5 },
            { 'one' : [] },
            { 'one' : {} },
            { 'one' : { 'three' : 'four' }},
        ]

        self._check(schema, accepted, rejected)
    def testOptionalNest(self):
        schema = {
            'one?' : {
                'two' : (basestring, )
            }
        }

        accepted = [
            { },
            { 'one' : { 'two' : 'three' }},
        ]

        rejected = [
            { 'one' : 5 },
            { 'one' : [] },
            { 'one' : {} },
            { 'one' : { 'three' : 'four' }},
        ]

        self._check(schema, accepted, rejected)

    def testAllOptionalNest(self):
        schema = {
            'one?' : {
                'two?' : (basestring, )
            }
        }

        accepted = [
            { },
            { 'one' : {} },
            { 'one' : { 'two' : 'three' }},
            { 'one' : { 'three' : 'four' }},
        ]

        rejected = [
            { 'one' : 5 },
            { 'one' : [] },
        ]

        self._check(schema, accepted, rejected)
    
    def testDeeperNest(self):
        schema = {
            'one' : {
                'two' : {
                    'three' : {
                        'four' : (basestring, ),
                    }
                }
            }
        }

        accepted = [
            {'one' : { 'two' : { 'three' : { 'four' : 'value' }}}}
        ]

        rejected = [
            { 'one' : 5 },
            { 'one' : [] },
            { 'one' : {} },
            { 'one' : { 'two' : { 'three' : 'value' }}},
        ]

        self._check(schema, accepted, rejected)

class ValidatorFunctionTest(ValidationTest):
    def testSimple(self):
        schema = { 'one' : (int, evenNumber) }

        accepted = [
            { 'one' : 2 },
            { 'one' : 4 },
        ]

        rejected = [
            {  },
            { 'one' : 1 },
            { 'one' : None },
        ]
        
        self._check(schema, accepted, rejected)

    def testSimpleList(self):
        schema = { 'one' : [ (int, evenNumber) ] }

        accepted = [
            { 'one' : [2] },
            { 'one' : [4, 6] },
        ]

        rejected = [
            {  },
            { 'one' : [1] },
            { 'one' : [2, 4, 7] },
            { 'one' : [None] },
        ]

        self._check(schema, accepted, rejected)
    
    def testChained(self):
        schema = { 'one' : (int, evenNumber, greaterThanSeven) }

        accepted = [
            { 'one' : 8 },
            { 'one' : 10 },
        ]

        rejected = [
            {  },
            { 'one' : 4 },
            { 'one' : 9 },
            { 'one' : None },
        ]

        self._check(schema, accepted, rejected)

    def testChainedList(self):
        schema = { 'one' : [ (int, evenNumber, greaterThanSeven) ] }

        accepted = [
            { 'one' : [8] },
            { 'one' : [10, 12] },
        ]

        rejected = [
            {  },
            { 'one' : [4] },
            { 'one' : [8, 9] },
            { 'one' : [10, 6] },
            { 'one' : [None] },
        ]

        self._check(schema, accepted, rejected)

if __name__ == '__main__':
    unittest.main()

# vim:et:fdm=indent:fdn=2
