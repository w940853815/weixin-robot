# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'
from app.aiml.Kernel import Kernel
import time
import unittest
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class Base_Test(unittest.TestCase):

    def setUp(self):
        self.k = Kernel()

    def tearDown(self):
        try:
            pass
        except Error:
            print 'faild'
        print 'test success'

    def _testTag(self, kern, tag, input, outputList):
        """Tests 'tag' by feeding the Kernel 'input'.  If the result
        matches any of the strings in 'outputList', the test passes.

        """
        global _numTests, _numPassed
        _numTests += 1
        print "Testing <" + tag + ">:",
        response = kern.respond(input).decode(kern._textEncoding)
        if response in outputList:
            print "PASSED"
            _numPassed += 1
            return True
        else:
            print "FAILED (response: '%s')" % response.encode(kern._textEncoding, 'replace')
            return False

class Test_Tag(Base_Test):
    def test_common_tag(self):
        self.k.bootstrap(learnFiles="../aiml/self-test.aiml")

        global _numTests, _numPassed
        _numTests = 0
        _numPassed = 0

        self._testTag(self.k, 'bot', 'test bot', ["My name is Nameless"])

        self.k.setPredicate('gender', 'male')
        self._testTag(self.k, 'condition test #1', 'test condition name value', ['You are handsome'])
        self.k.setPredicate('gender', 'female')
        self._testTag(self.k, 'condition test #2', 'test condition name value', [''])
        self._testTag(self.k, 'condition test #3', 'test condition name', ['You are beautiful'])
        self.k.setPredicate('gender', 'robot')
        self._testTag(self.k, 'condition test #4', 'test condition name', ['You are genderless'])
        self._testTag(self.k, 'condition test #5', 'test condition', ['You are genderless'])
        self.k.setPredicate('gender', 'male')
        self._testTag(self.k, 'condition test #6', 'test condition', ['You are handsome'])

        # the date test will occasionally fail if the original and "test"
        # times cross a second boundary.  There's no good way to avoid
        # this problem and still do a meaningful test, so we simply
        # provide a friendly message to be printed if the test fails.
        date_warning = """
            NOTE: the <date> test will occasionally report failure even if it
            succeeds.  So long as the response looks like a date/time string,
            there's nothing to worry about.
            """
        if not self._testTag(self.k, 'date', 'test date', ["The date is %s" % time.asctime()]):
            print date_warning

        self._testTag(self.k, 'formal', 'test formal', ["Formal Test Passed"])
        self._testTag(self.k, 'gender', 'test gender', ["He'd told her he heard that her hernia is history"])
        self._testTag(self.k, 'get/set', 'test get and set', ["I like cheese. My favorite food is cheese"])
        self._testTag(self.k, 'gossip', 'test gossip', ["Gossip is not yet implemented"])
        self._testTag(self.k, 'id', 'test id', ["Your id is _global"])
        self._testTag(self.k, 'input', 'testinput', ['You just said:testinput'])
        self._testTag(self.k, 'javascript', 'test javascript', ["Javascript is not yet implemented"])
        self._testTag(self.k, 'lowercase', 'test lowercase', ["The Last Word Should Be lowercase"])
        self._testTag(self.k, 'person', 'test person', ['HE think i knows that my actions threaten him and his.'])
        self._testTag(self.k, 'person2', 'test person2', ['YOU think me know that my actions threaten you and yours.'])
        self._testTag(self.k, 'person2 (no contents)', 'test person2 I Love Lucy', ['YOU Love Lucy'])
        self._testTag(self.k, 'random', 'test random', ["response #1", "response #2", "response #3"])
        self._testTag(self.k, 'random empty', 'test random empty', ["Nothing here!"])
        self._testTag(self.k, 'sentence', "test sentence", ["My first letter should be capitalized."])
        self._testTag(self.k, 'size', "test size", ["I've learned %d categories" % self.k.numCategories()])
        self._testTag(self.k, 'sr', "test sr test srai", ["srai results: srai test passed"])
        self._testTag(self.k, 'sr nested', "test nested sr test srai", ["srai results: srai test passed"])
        self._testTag(self.k, 'srai', "test srai", ["srai test passed"])
        self._testTag(self.k, 'srai infinite', "test srai infinite", [""])
        self._testTag(self.k, 'star test #1', 'You should test star begin', ['Begin star matched: You should'])
        self._testTag(self.k, 'star test #2', 'test star creamy goodness middle', ['Middle star matched: creamy goodness'])
        self._testTag(self.k, 'star test #3', 'test star end the credits roll', ['End star matched: the credits roll'])
        self._testTag(self.k, 'star test #4', 'test star having multiple stars in a pattern makes me extremely happy',
                 ['Multiple stars matched: having, stars in a pattern, extremely happy'])
        self._testTag(self.k, 'system', "test system", ["The system says hello!"])
        self._testTag(self.k, 'that test #1', "test that", ["I just said: The system says hello!"])
        self._testTag(self.k, 'that test #2', "test that", ["I have already answered this question"])
        self._testTag(self.k, 'thatstar test #1', "test thatstar", ["I say beans"])
        self._testTag(self.k, 'thatstar test #2', "test thatstar", ["I just said \"beans\""])
        self._testTag(self.k, 'thatstar test #3', "test thatstar multiple", ['I say beans and franks for everybody'])
        self._testTag(self.k, 'thatstar test #4', "test thatstar multiple", ['Yes, beans and franks for all!'])
        self._testTag(self.k, 'think', "test think", [""])
        self.k.setPredicate("topic", "fruit")
        self._testTag(self.k, 'topic', "test topic", ["We were discussing apples and oranges"])
        self.k.setPredicate("topic", "Soylent Green")
        self._testTag(self.k, 'topicstar test #1', 'test topicstar', ["Solyent Green is made of people!"])
        self.k.setPredicate("topic", "Soylent Ham and Cheese")
        self._testTag(self.k, 'topicstar test #2', 'test topicstar multiple', ["Both Soylents Ham and Cheese are made of people!"])
        self._testTag(self.k, 'unicode support', u"你好你好", [u"Hey, you speak Chinese!你好你好"])
        self._testTag(self.k, 'uppercase', 'test uppercase', ["The Last Word Should Be UPPERCASE"])
        self._testTag(self.k, 'version', 'test version', ["PyAIML is version %s" % self.k.version()])
        self._testTag(self.k, 'whitespace preservation', 'test whitespace', ["Extra   Spaces\n   Rule!   (but not in here!)    But   Here   They   Do!"])

        # Report test results
        print "--------------------"
        if _numTests == _numPassed:
            print "%d of %d tests passed!" % (_numPassed, _numTests)
        else:
            print "%d of %d tests passed (see above for detailed errors)" % (_numPassed, _numTests)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(suite)



    # Run an interactive interpreter
    #print "\nEntering interactive mode (ctrl-c to exit)"
    #while True: print k.respond(raw_input("> "))
