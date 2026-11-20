"""Recursive-descent parser for Spider v0.1."""
from dataclasses import dataclass

@dataclass
class Node:
    kind: str
    value: object = None
    children: list = None

class ParseError(Exception): pass

class Parser:
    def __init__(self, tokens): self.tokens=tokens; self.i=0
    def peek(self): return self.tokens[self.i]
    def take(self): t=self.peek(); self.i+=1; return t
    def match(self, value):
        if self.peek().value == value: self.take(); return True
        return False
    def expect(self, value):
        t=self.take()
        if t.value != value: raise ParseError(f"Expected {value!r} at {t.line}:{t.column}, got {t.value!r}")
        return t
    def expect_kind(self, kind):
        t=self.take()
        if t.kind != kind: raise ParseError(f"Expected {kind} at {t.line}:{t.column}, got {t.value!r}")
        return t
    def parse(self):
        statements=[]
        if self.match("spider"):
            self.expect("::"); self.expect("main"); self.expect("{")
            statements=self.block_contents()
        else:
            statements=self.block_contents(until="EOF")
        return Node("program", children=statements)
    def block_contents(self, until="}"):
        result=[]
        while self.peek().kind != "EOF" and (until=="EOF" or self.peek().value != until):
            result.append(self.statement())
        if until != "EOF": self.expect(until)
        return result
    def statement(self):
        if self.match("let"):
            name=self.expect_kind("IDENT").value; self.expect("="); return Node("let",name,[self.expression()])
        if self.match("if"):
            cond=self.expression(); self.expect("{"); yes=self.block_contents()
            no=[]
            if self.match("else"):
                self.expect("{"); no=self.block_contents()
            return Node("if",children=[cond,Node("block",children=yes),Node("block",children=no)])
        if self.match("while"):
            cond=self.expression(); self.expect("{"); body=self.block_contents(); return Node("while",children=[cond,Node("block",children=body)])
        if self.match("fn"):
            name=self.expect_kind("IDENT").value; self.expect("("); params=[]
            if self.peek().value != ")":
                params.append(self.expect_kind("IDENT").value)
                while self.match(","): params.append(self.expect_kind("IDENT").value
)
            self.expect(")"); self.expect("{"); body=self.block_contents(); return Node("fn",name,[Node("params",params),Node("block",children=body)])
        if self.match("return"):
            return Node("return",children=[self.expression()])
        if self.match("output") or self.match("say"):
            self.expect("("); expr=self.expression(); self.expect(")"); self.match(";"); return Node("output",children=[expr])
        if self.peek().kind=="IDENT" and self.tokens[self.i+1].value=="=":
            name=self.take().value; self.expect("="); expr=self.expression(); self.match(";"); return Node("assign",name,[expr])
        expr=self.expression(); self.match(";"); return Node("expr",children=[expr])
    PRECEDENCE={"||":1,"&&":2,"==":3,"!=":3,"<":4,"<=":4,">":4,">=":4,"+":5,"-":5,"*":6,"/":6,"%":6}
    def expression(self, min_prec=1):
        tok=self.take()
        if tok.value in ("-", "!"):
            left=Node("unary",tok.value,[self.expression(7)])
        elif tok.value=="(":
            left=self.expression(); self.expect(")")
        elif tok.kind=="NUMBER": left=Node("literal",float(tok.value) if "." in tok.value else int(tok.value))
        elif tok.kind=="STRING": left=Node("literal",tok.value)
        elif tok.value in ("true","false","null"): left=Node("literal",{"true":True,"false":False,"null":None}[tok.value])
        elif tok.kind=="IDENT": left=Node("variable",tok.value)
        else: raise ParseError(f"Unexpected token {tok.value!r} at {tok.line}:{tok.column}")
        while True:
            if self.peek().value=="(" and left.kind=="variable":
                self.take(); args=[]
                if self.peek().value!=")":
                    args.append(self.expression())
                    while self.match(","): args.append(self.expression())
                self.expect(")"); left=Node("call",left.value,args); continue
            op=self.peek().value; prec=self.PRECEDENCE.get(op,0)
            if prec < min_prec: break
            self.take(); right=self.expression(prec+1); left=Node("binary",op,[left,right])
        return left
