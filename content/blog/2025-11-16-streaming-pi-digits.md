---
title: Streaming Digits of Pi
description: Exploring a strategy to calculate infinite digits of π without floating point arithmetic
Date: 2025-11-16 19:30:00
tags: ["csharp", "JavaScript"]
---

**This page describes a strategy for calculating pi one digit at a time** using a streaming algorithm that does not require floating point arithmetic. Although there are more exotic strategies for calculating pi, this one is surprisingly simple to implement, and it streams the digits of pi infinitely with O(N<sup>2</sup>) time complexity and O(N) space complexity. Before we dive in, [give it a try in your browser](https://swharden.com/static/2025/11/16/pi)!

<a href="https://swharden.com/static/2025/11/16/pi" target="_blank">
<img src="https://swharden.com/static/2025/11/16/calculate-pi-browser2.png" class="w-75 mx-auto">
</a>

## Theory

It has long been known that pi can be represented as the product of an infinite series. The [Wallis Product](https://en.wikipedia.org/wiki/Wallis_product) published in 1656 represents Pi as the product of an infinite series:

<img src="https://swharden.com/static/2025/11/16/sum.png" class="mx-auto">

Which can be expanded to:

<img src="https://swharden.com/static/2025/11/16/wallis.png" class="mx-auto">

Or alternatively expressed as:

<img src="https://swharden.com/static/2025/11/16/expanded.png" class="mx-auto">

**[Spigot Algorithm for the Digits of Pi](https://www.cs.williams.edu/~heeringa/classes/cs135/s15/readings/spigot.pdf) (1995) by 
Stanley Rabinowitz and Stan Wagon described how infinite product series can be expanded to allow calculation digit by digit, representing the output in base 10.** The algorithm is is described in the paper on page 5. Appendix 2 has a useful bit of code attributed to "Macalester student Simeon Simeonov" implementing the algorithm in Pascal. It notes that this code makes use of the fact that the queue of predigits always has a pile of 9s to the right of its leftmost member, and so only this leftmost predigit and the number of 9s need be remembered.

## Pascal Implementation

```pascal
Program PiSpigot;

const
  n   = 1000;
  len = 10 * n div 3;

var
  i, j, k, q, x, nines, predigit: integer;
  a: array[1..len] of longint;

begin
  for j := 1 to len do
    a[j] := 2;  {Start with 2s}

  nines := 0;
  predigit := 0;  {First predigit is a 0}

  for j := 1 to n do
  begin
    q := 0;

    for i := len downto 1 do  {Work backwards}
    begin
      x := 10 * a[i] + q * i;
      a[i] := x mod (2 * i - 1);
      q := x div (2 * i - 1);
    end;

    a[1] := q mod 10;
    q := q div 10;

    if q = 9 then
      nines := nines + 1
    else if q = 10 then
    begin
      write(predigit + 1);

      for k := 1 to nines do
        write(0);  {zeros}

      predigit := 0;
      nines := 0;
    end
    else
    begin
      write(predigit);
      predigit := q;

      if nines <> 0 then
      begin
        for k := 1 to nines do
          write(9);

        nines := 0;
      end;
    end;
  end;

  writeln(predigit);
end.
```

## C# Implementation

A line-by-line translation to C# is as follows

```cs
int maxDigits = 1000;
int len = (10 * maxDigits) / 3;

int[] a = new int[len + 1];
int nines = 0;
int predigit = 0;

for (int j = 1; j <= len; j++)
    a[j] = 2;

for (int j = 1; j <= maxDigits; j++)
{
    int q = 0;

    for (int i = len; i >= 1; i--)
    {
        int x = 10 * a[i] + q * i;
        a[i] = x % (2 * i - 1);
        q = x / (2 * i - 1);
    }

    a[1] = q % 10;
    q /= 10;

    if (q == 9)
    {
        nines++;
    }
    else if (q == 10)
    {
        Console.Write(predigit + 1);

        for (int k = 1; k <= nines; k++)
            Console.Write(0);

        predigit = 0;
        nines = 0;
    }
    else
    {
        if (j > 1)
            Console.Write(predigit);
        if (j == 2)
            Console.Write(".");

        predigit = q;

        if (nines != 0)
        {
            for (int k = 1; k <= nines; k++)
                Console.Write(9);

            nines = 0;
        }
    }
}
```

**It generates the first thousand digits of pi in about 60 milliseconds.** The first 10,000 took 3.3 sec, and additional performance benchmarks can be found at the bottom of this page. The output in accurate, checked using some online tables I found of pi to a large number of decimal places.

<div class="font-monospace p-2 bg-light border rounded text-muted">
3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912983367336244065664308602139494639522473719070217986094370277053921717629317675238467481846766940513200056812714526356082778577134275778960917363717872146844090122495343014654958537105079227968925892354201995611212902196086403441815981362977477130996051870721134999999837297804995105973173281609631859502445945534690830264252230825334468503526193118817101000313783875288658753320838142061717766914730359825349042875546873115956286388235378759375195778185778053217122680661300192787661119590921642019
</div>

## Calculate Pi in your Browser

**I implemented the [Spigot Algorithm for the Digits of Pi](https://www.cs.williams.edu/~heeringa/classes/cs135/s15/readings/spigot.pdf) in JavaScript and [adapted it to run in the browser](https://swharden.com/static/2025/11/16/pi).** It utilizes JavaScript's [BigInt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt) type to manage math with arbitrarily large integers and runs with a performance comparable to the C# example above.

<a href="https://swharden.com/static/2025/11/16/pi" target="_blank">
<img src="https://swharden.com/static/2025/11/16/calculate-pi-browser2.png" class="w-75 mx-auto">
</a>

* **Try it Live:** [Calculate Pi in your browser](https://swharden.com/static/2025/11/16/pi)
* **Source Code** is on GitHub [swharden/Calculate-Pi](https://github.com/swharden/Calculate-Pi)

Performance of the JavaScript implementation is surprisingly good. You can generate virtually infinite digits of pi using your desktop of mobile device. You never know when you're going to need a few thousand digits of pi, and it is always good to be prepared.

## Resources
* [Source Code](https://github.com/swharden/Calculate-Pi) (GitHub) for C# and JavaScript projects used on this page
* [Spigot Algorithm for the Digits of Pi](https://www.cs.williams.edu/~heeringa/classes/cs135/s15/readings/spigot.pdf) (1995) is the paper this article is based on
* [The Wallis Formula for Pi](https://mindyourdecisions.com/blog/2016/10/12/the-wallis-product-formula-for-pi-and-its-proof/) (2016) By Presh Talwalkar is a nice commentary on the original paper
* [Unbounded Spigot Algorithms for the Digits of Pi](https://www.cs.ox.ac.uk/people/jeremy.gibbons/publications/spigot.pdf) (2005) by Jeremy Gibbons
* [Practical implementation of Spigot Algorithms for Transcendental Constants](https://www.hvks.com/Numerical/Downloads/HVE%20Practical%20implementation%20of%20Spigot%20Algorithms%20for%20transcendental%20constants.pdf) (2022) by Henrik Vestermark
* [Nilakantha’s formula for pi](https://vixra.org/pdf/2302.0056v1.pdf) (2023) by Edgar Valdebenito