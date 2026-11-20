"""Command-line runner for Spider source files."""
import argparse, pathlib, sys
from .lexer import Lexer, LexerError
from .parser import Parser, ParseError
from .runtime import Interpreter, SpiderError

def run_file(path):
    source=pathlib.Path(path).read_text(encoding="utf-8")
    try: program=Parser(Lexer(source).tokens()).parse(); Interpreter().run(program)
    except (LexerError,ParseError,SpiderError) as e:
        print(f"Spider error: {e}",file=sys.stderr); return 1
    return 0

def main():
    p=argparse.ArgumentParser(prog="spider",description="Spider language interpreter v0.1")
    p.add_argument("command",choices=["run"]); p.add_argument("file",help="Source file (.spi)")
    args=p.parse_args(); raise SystemExit(run_file(args.file))
if __name__=="__main__": main()
