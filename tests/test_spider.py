import unittest
from spider_lang.lexer import Lexer
from spider_lang.parser import Parser
from spider_lang.runtime import Interpreter

class SpiderTests(unittest.TestCase):
    def run_source(self, source):
        out=[]; program=Parser(Lexer(source).tokens()).parse(); Interpreter(out.append).run(program); return out
    def test_math_and_output(self): self.assertEqual(self.run_source('spider::main { let x = 2 + 3 * 4; output(x) }'),[14])
    def test_if_else(self): self.assertEqual(self.run_source('spider::main { if 2 > 1 { output("yes") } else { output("no") } }'),['yes'])
    def test_while(self): self.assertEqual(self.run_source('spider::main { let x = 0; while x < 3 { output(x); x = x + 1 } }'),[0,1,2])
    def test_function(self): self.assertEqual(self.run_source('spider::main { fn double(x) { return x * 2 }; output(double(5)) }'),[10])
if __name__=="__main__": unittest.main()
