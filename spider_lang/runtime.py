"""Interpreter for Spider v0.1. It never uses Python eval/exec."""
class SpiderError(Exception): pass
class ReturnSignal(Exception):
    def __init__(self, value): self.value=value

class Environment:
    def __init__(self, parent=None): self.values={}; self.parent=parent
    def define(self, name, value): self.values[name]=value
    def get(self, name):
        if name in self.values: return self.values[name]
        if self.parent: return self.parent.get(name)
        raise SpiderError(f"Undefined variable: {name}")
    def assign(self, name, value):
        if name in self.values: self.values[name]=value; return
        if self.parent: self.parent.assign(name,value); return
        raise SpiderError(f"Undefined variable: {name}")

class Function:
    def __init__(self, params, body, closure): self.params=params; self.body=body; self.closure=closure

class Interpreter:
    def __init__(self, output=print, max_loop_iterations=100000):
        self.output=output; self.globals=Environment(); self.max_loop_iterations=max_loop_iterations
        self.globals.define("output", self.output)
    def run(self, program):
        for stmt in program.children: self.execute(stmt,self.globals)
    def execute(self,node,env):
        k=node.kind
        if k=="let": env.define(node.value,self.evaluate(node.children[0],env))
        elif k=="assign": env.assign(node.value,self.evaluate(node.children[0],env))
        elif k=="output": self.output(self.evaluate(node.children[0],env))
        elif k=="expr": self.evaluate(node.children[0],env)
        elif k=="block":
            local=Environment(env)
            for s in node.children: self.execute(s,local)
        elif k=="if": self.execute(node.children[1 if self.truth(self.evaluate(node.children[0],env)) else 2],env)
        elif k=="while":
            count=0
            while self.truth(self.evaluate(node.children[0],env)):
                if count>=self.max_loop_iterations: raise SpiderError("Loop limit reached; stopping runaway program")
                count+=1; self.execute(node.children[1],env)
        elif k=="fn": env.define(node.value,Function(node.children[0].value,node.children[1],env))
        elif k=="return": raise ReturnSignal(self.evaluate(node.children[0],env))
        else: raise SpiderError(f"Unknown statement: {k}")
    def evaluate(self,node,env):
        k=node.kind
        if k=="literal": return node.value
        if k=="variable": return env.get(node.value)
        if k=="unary":
            v=self.evaluate(node.children[0],env)
            if node.value=="-": return -v
            if node.value=="!": return not self.truth(v)
        if k=="binary":
            a=self.evaluate(node.children[0],env); op=node.value
            if op=="&&": return self.truth(a) and self.truth(self.evaluate(node.children[1],env))
            if op=="||": return self.truth(a) or self.truth(self.evaluate(node.children[1],env))
            b=self.evaluate(node.children[1],env)
            try:
                return {"+":lambda:a+b,"-":lambda:a-b,"*":lambda:a*b,"/":lambda:a/b,"%":lambda:a%b,"==":lambda:a==b,"!=":lambda:a!=b,"<":lambda:a<b,"<=":lambda:a<=b,">":lambda:a>b,">=":lambda:a>=b}[op]()
            except (TypeError,ZeroDivisionError) as e: raise SpiderError(f"Invalid operation {op}: {e}") from e
        if k=="call":
            fn=env.get(node.value); args=[self.evaluate(a,env) for a in node.children]
            if callable(fn): return fn(*args)
            if not isinstance(fn,Function): raise SpiderError(f"{node.value} is not callable")
            if len(args)!=len(fn.params): raise SpiderError(f"{node.value} expects {len(fn.params)} arguments, got {len(args)}")
            local=Environment(fn.closure)
            for name,value in zip(fn.params,args): local.define(name,value)
            try:
                for s in fn.body.children: self.execute(s,local)
            except ReturnSignal as r: return r.value
            return None
        raise SpiderError(f"Cannot evaluate node: {k}")
    @staticmethod
    def truth(v): return bool(v)
