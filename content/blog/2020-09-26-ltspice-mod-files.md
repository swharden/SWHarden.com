---
title: Using MOD Files in LTSpice
date: 2020-09-27 16:21:00
tags: ["circuit"]
---

# Using MOD Files in LTSpice

**This page shows how to use the LM741 op-amp model file in LTSpice.** This is surprisingly un-intuitive, but is a good thing to know how to do. Model files can often be downloaded by vendor sites, but LTSpice only comes pre-loaded with models of common LT components.

## Step 1: Download a Model (.mod) File

I found [`LM741.MOD`](https://swharden.com/static/2020/09/26/LM741.MOD) available on the TI's [LM741 product page](https://www.ti.com/product/LM741).

Save it wherever you want, but you will need to know the full path to this file later.

## Step 2: Determine the Name

Open the model file in a text editor and look for the line starting with `.SUBCKT`. The top of LM741.MOD looks like this:

```c
* connections:      non-inverting input
*                   |   inverting input
*                   |   |   positive power supply
*                   |   |   |   negative power supply
*                   |   |   |   |   output
*                   |   |   |   |   |
*                   |   |   |   |   |
.SUBCKT LM741/NS    1   2  99  50  28
```

The last line tells us the name of this model's sub-circuit is `LM741/NS`

## Step 3: Include the Model File

Click the ".op" button on the toolbar, then add `.include` followed by the full path to the model file. After clicking OK place the text somewhere on your LTSpice circuit diagram.

<div class="text-center img-border">

![](https://swharden.com/static/2020/09/26/op2.png)

</div>

## Step 4: Insert a General Purpose Part

We know the part we are including is a 5-pin op-amp, so we can start by placing a generic component. Notice the description says _you must give the value a name and include this file_. We will do this in the next step.

<div class="text-center img-border">

![](https://swharden.com/static/2020/09/26/opamp.png)

</div>

## Step 5: Configure the Component to use the Model

Right-click the op-amp and update its `Value` to match the name of the subcircuit we read from the model file earlier.

<div class="text-center img-border">

![](https://swharden.com/static/2020/09/26/name.png)

</div>

## Step 6: Simulate Your Circuit

Your new component will run using the properties of the model you downloaded.

<div class="text-center img-border">

![](https://swharden.com/static/2020/09/26/ltspice-lm741.png)

</div>