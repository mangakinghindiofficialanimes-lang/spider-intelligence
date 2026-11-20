# Spider Language v0.1

Spider is a small custom interpreted language. Source files use **.spi**.

## Run

From the repository root:

```bash
python -m spider_lang.cli run examples/hello.spi
```

## Syntax

```spider
spider::main {
    let name = "Spider"
    output("Hello, " + name)
    let n = 3
    while n > 0 {
        output(n)
        n = n - 1
    }
    fn square(x) { return x * x }
    output(square(5))
}
```

Implemented: numbers, strings, booleans, null, variables, assignment, arithmetic, comparisons, logical operators, output, if/else, while, functions, return, comments with # or //, and parentheses.

This is an early interpreter, not yet a compiler or encrypted bytecode system. The planned .spib format and protection pipeline are not implemented. Security claims must wait for threat modeling, independent review, and tests; encryption/obfuscation cannot make software impossible to reverse-engineer.

## Test

```bash
python -m unittest discover -s tests
```
