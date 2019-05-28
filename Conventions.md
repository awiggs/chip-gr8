# Conventions

The following outlines basic code conventions that will be used for this project.

## C Code

All blocks will be tabbed using four spaces

```c
int functionA() {
    if (condition) {
        functionB();
    } else {
        functionC();
    }
}
```

Variable names will be written in camelCase

```c
int myVariable = 42;
```

Constants will be written in all caps with underscores

```c
#define MY_CONSTANT 42
// or
const int MY_CONSTANT = 42;
```

Structs and unions will be written UpperCamelCase followed by the `_t` posfix

```c
typedef struct MyStruct_t MyStruct_t;
```

Type aliases of non-compound types (`int`, `char`, etc.) will be written in camelcase and optionally followed by the `_t` postfix

```c
typedef int myInt;
// or
typedef int myInt_t;
```

Curly braces will appear on the same line

```c 
for (i = 0; i < N; ++i) {
    // ...
}
```

`for` loops, `while` loops, `if` statements will pad round brackets with spaces and will always be followed by curly braces

```c
if (condition) {
    // ...
}
```

Function calls are written with no additional whitespace padding except after the `,`

```c
myFunction(arg1, arg2, arg3);
```

Functions should generally be documented with a doc-comment that follows the following format

```c
/**
 * A description of the function's purpose.
 * 
 * @params arg1 A description of arg1
 *         arg2 A description of arg2
 * @returns     A description of the return value
 */
int myFunction(int arg1, int arg2) {
    // ...
}
```

Inline comments should place a space between the `//` and the comment start

```c
// A comment
```

## Python

All blocks will be tabbed using four spaces

```python
def functionA():
    if condition:
        functionB()
    else:
        functionC()
```

Variable names will be written in camelCase

```python
myVariable = 42
```

Constants will be written in all caps with underscores

```python
MY_CONSTANT = 42
```

Class names will be written in UpperCamelCase

```python
class MyClass(object):
    # ...
```