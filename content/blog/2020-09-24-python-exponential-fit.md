---
title: Exponential Fit with Python
date: 2020-09-24 17:45:00
tags: ["python"]
---

# Exponential Fit with Python

**Fitting an exponential curve to data is a common task** and in this example we'll use Python and SciPy to determine parameters for a curve fitted to arbitrary X/Y points. You can follow along using the [fit.ipynb](https://swharden.com/static/2020/09/24/fit.ipynb) Jupyter notebook.

```python
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

xs = np.arange(12) + 7
ys = np.array([304.08994, 229.13878, 173.71886, 135.75499,
               111.096794, 94.25109, 81.55578, 71.30187, 
               62.146603, 54.212032, 49.20715, 46.765743])

plt.plot(xs, ys, '.')
plt.title("Original Data")
```

<div class="text-center">

![](https://swharden.com/static/2020/09/24/original.png)

</div>

**To fit an arbitrary curve** we must first define it as a function. We can then call `scipy.optimize.curve_fit` which will tweak the arguments (using arguments we provide as the starting parameters) to best fit the data. In this example we will use a single [exponential decay](https://en.wikipedia.org/wiki/Exponential_decay) function. 

```python
def monoExp(x, m, t, b):
    return m * np.exp(-t * x) + b
```

**In biology / electrophysiology _biexponential_ functions are often used** to separate fast and slow components of exponential decay which may be caused by different mechanisms and occur at different rates. In this example we will only fit the data to a method with a exponential component (a _monoexponential_ function), but the idea is the same.

```python
# perform the fit
p0 = (2000, .1, 50) # start with values near those we expect
params, cv = scipy.optimize.curve_fit(monoExp, xs, ys, p0)
m, t, b = params
sampleRate = 20_000 # Hz
tauSec = (1 / t) / sampleRate

# determine quality of the fit
squaredDiffs = np.square(ys - monoExp(xs, m, t, b))
squaredDiffsFromMean = np.square(ys - np.mean(ys))
rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
print(f"R² = {rSquared}")

# plot the results
plt.plot(xs, ys, '.', label="data")
plt.plot(xs, monoExp(xs, m, t, b), '--', label="fitted")
plt.title("Fitted Exponential Curve")

# inspect the parameters
print(f"Y = {m} * e^(-{t} * x) + {b}")
print(f"Tau = {tauSec * 1e6} µs")
```

<div class="text-center">

![](https://swharden.com/static/2020/09/24/fitted.png)

</div>

```
Y = 2666.499 * e^(-0.332 * x) + 42.494
Tau = 150.422 µs
R² = 0.999107330342064
```

## Extrapolating the Fitted Curve

**We can use the calculated parameters to extend this curve** to any position by passing X values of interest into the function we used during the fit. 

**The value at time 0** is simply `m + b` because the exponential component becomes e^(0) which is 1.

```python
xs2 = np.arange(25)
ys2 = monoExp(xs2, m, t, b)

plt.plot(xs, ys, '.', label="data")
plt.plot(xs2, ys2, '--', label="fitted")
plt.title("Extrapolated Exponential Curve")
```

<div class="text-center">

![](https://swharden.com/static/2020/09/24/fitted2.png)

</div>

## Constraining the Infinite Decay Value

**What if we know our data decays to 0?** It's not best to fit to an exponential decay function that lets the `b` component be whatever it wants. Indeed, our fit from earlier calculated the ideal `b` to be `42.494` but what if we know it should be `0`? The solution is to fit using an exponential function where `b` is constrained to 0 (or whatever value you know it to be).

```python
def monoExpZeroB(x, m, t):
    return m * np.exp(-t * x)

# perform the fit using the function where B is 0
p0 = (2000, .1) # start with values near those we expect
paramsB, cv = scipy.optimize.curve_fit(monoExpZeroB, xs, ys, p0)
mB, tB = paramsB
sampleRate = 20_000 # Hz
tauSec = (1 / tB) / sampleRate

# inspect the results
print(f"Y = {mB} * e^(-{tB} * x)")
print(f"Tau = {tauSec * 1e6} µs")

# compare this curve to the original
ys2B = monoExpZeroB(xs2, mB, tB)
plt.plot(xs, ys, '.', label="data")
plt.plot(xs2, ys2, '--', label="fitted")
plt.plot(xs2, ys2B, '--', label="zero B")
```

```
Y = 1245.580 * e^(-0.210 * x)
Tau = 237.711 µs
```

<div class="text-center">

![](https://swharden.com/static/2020/09/24/fits.png)

</div>

**The curves produced are very different** at the extremes (especially when time is 0), even though they appear to both fit the data points nicely. Which curve is more accurate? That depends on your application. A hint can be gained by inspecting the time constants of these two curves.

<div class="text-center">

Parameter | Fitted B | Fixed B
---|---|---
m|2666.499|1245.580
t|0.332|0.210
Tau|150.422 µs|237.711 µs
b|42.494|0

</div>

**By inspecting Tau** I can gain insight into which method may be better for me to use in my application. I expect Tau to be near 250 µs, leading me to trust the fixed-B method over the fitted B method. Choosing the correct method has great implications on the value of `m` (which is also the value of the curve when time is 0).