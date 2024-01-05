import unittest
import b_execute_perturbation 

class TestBExecutePerturbation(unittest.TestCase):
    def testGenerateBuggyLineContext1(self):
        line = 'test1'
        lineIdx = 19
        buggyLineNos = ['20', '21', '', '', '']
        corruptCode = ''
        
        result = b_execute_perturbation.generateBuggyLineContext(line, lineIdx, buggyLineNos, corruptCode)

        self.assertEqual(result, '<BUG>  </BUG> ')
    
    def testGenerateBuggyLineContext2(self):
        line = 'test1'
        lineIdx = 20
        buggyLineNos = ['20', '21', '', '', '']
        corruptCode = ''
        
        result = b_execute_perturbation.generateBuggyLineContext(line, lineIdx, buggyLineNos, corruptCode)

        self.assertEqual(result, '')

    def testGenerateBuggyLineContext3(self):
        line = 'test1'
        lineIdx = 21
        buggyLineNos = ['20', '21', '', '', '']
        corruptCode = ''
        
        result = b_execute_perturbation.generateBuggyLineContext(line, lineIdx, buggyLineNos, corruptCode)

        self.assertEqual(result, 'test1')
    
    def testGenerateBuggyLineContext4(self):
        line = 'test1'
        lineIdx = 18
        buggyLineNos = ['20', '21', '', '', '']
        corruptCode = ''
        
        result = b_execute_perturbation.generateBuggyLineContext(line, lineIdx, buggyLineNos, corruptCode)

        self.assertEqual(result, 'test1')

    