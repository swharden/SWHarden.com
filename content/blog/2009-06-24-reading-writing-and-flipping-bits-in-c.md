---
title: Flipping Bits in C
date: 2009-06-24 15:28:07
---

# Flipping Bits in C

__Bitwise programming techniques (manipulating the 1s and 0s of binary numbers) are simple, but hard to  remember if you don't use them often.__ Recently I've needed to perform a lot of bitwise operations. If I'm storing true/false (1-bit) information in variables, it's a waste of memory to assign a whole variable to the task (the smallest variable in C is a char, and it contains 8 bits). When cramming multiple values into individual variables, it's nice to know how to manipulate each bit of a variable.

```c
// set the Nth bit of x to 0
x &= ~(1 << n);

// set the Nth bit of x to 1
x |= (1 << n); 

// store the Nth bit of x in y (y becomes 0 or 1)
y = (x >> n) & 1; 

// leave the lowest N bits of x alone and set higher bits to 0.
x &= (1 << (n + 1)) - 1;

// toggle the Nth bit of x
x ^= (1 << n);

// toggle every bit of x
x = ~x;
```

