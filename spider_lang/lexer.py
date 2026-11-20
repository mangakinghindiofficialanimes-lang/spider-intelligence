"""Tokenizer for Spider (.spi) source."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    line: int
    column: int

KEYWORDS = {"let", "if", "else", "while", "fn", "return", "true", "false", "null"}
TWO = {"==", "!=", "<=", ">=", "&&", "||", "::"}
SINGLE = set("{}(),;+-*/%!=<>")

class LexerError(Exception): pass

class Lexer:
    def __init__(self, source):
        self.source = source
        self.i = 0
        self.line = 1
        self.col = 1

    def advance(self):
        ch = self.source[self.i]
        self.i += 1
        if ch == "\n": self.line, self.col = self.line + 1, 1
        else: self.col += 1
        return ch

    def peek(self, offset=0):
        pos = self.i + offset
        return self.source[pos] if pos < len(self.source) else ""

    def tokens(self):
        out = []
        while self.i < len(self.source):
            ch = self.peek()
            if ch.isspace(): self.advance(); continue
            if ch == "#" or (ch == "/" and self.peek(1) == "/"):
                while self.i < len(self.source) and self.peek() != "\n": self.advance()
                continue
            line, col = self.line, self.col
            if ch in ('"', "'"):
                quote = self.advance(); value = ""
                while self.i < len(self.source) and self.peek() != quote:
                    c = self.advance()
                    if c == "\\":
                        if self.i >= len(self.source): raise LexerError(f"Unfinished escape at {line}:{col}")
                        e = self.advance(); value += {"n":"\n", "t":"\t", "r":"\r", "\\":"\\", quote:quote}.get(e, e)
                    else: value += c
                if self.peek() != quote: raise LexerError(f"Unterminated string at {line}:{col}")
                self.advance(); out.append(Token("STRING", value, line, col)); continue
            if ch.isdigit():
                value = self.advance()
                while self.peek().isdigit(): value += self.advance()
                if self.peek() == "." and self.peek(1).isdigit():
                    value += self.advance()
                    while self.peek().isdigit(): value += self.advance()
                out.append(Token("NUMBER", value, line, col)); continue
            if ch.isalpha() or ch == "_":
                value = self.advance()
                while self.peek().isalnum() or self.peek() == "_": value += self.advance()
                out.append(Token("KEYWORD" if value in KEYWORDS else "IDENT", value, line, col)); continue
            pair = ch + self.peek(1)
            if pair in TWO: self.advance(); self.advance(); out.append(Token("OP", pair, line, col)); continue
            if ch in SINGLE: self.advance(); out.append(Token("OP", ch, line, col)); continue
            raise LexerError(f"Unexpected character {ch!r} at {line}:{col}")
        out.append(Token("EOF", "", self.line, self.col))
        return out
