
Deviation 0.2
=============

[Deviation](https://github.com/d-zo/Deviation) is a simple Python class which can be used
to estimate the worst-case error for (basic) arithmetic operations
with measurement values.

Often, multiple sets of measurement values are reduced to one set of mean values
before deriving other values from it.
This can easily deceive the accuracy of the derived results.
A common strategy is to use the standard deviation
and calculate confidence intervals for the results
(e.g. with the [uncertainties](https://github.com/lebigot/uncertainties/) package).
But if an upper bound on the worst-case error is needed,
this class can be useful.

Since this class only takes into account the greatest errors,
extreme outliers in the input data might render the worst-case error approximation unusable
(strategies based on standard deviation are more suited for these cases).
The calculated worst-case error of measurement data readily shows
how much the output data could possibly deviate from the calculated result
due to fluctuations in the input data.

Please note that the worst-case error is an upper bound on the actual error.
It might greatly overestimate the actual error and
the actual error might be bigger to one side than the other (not equally around the mean).



Installation
------------

Deviation requires a working Python 3.x environment and
can be downloaded and run with Python.
A simple solution is to copy the main file `Deviation.py` in the current working directory.



Loading the Deviation class
---------------------------

To load the Deviation class,
the main file `Deviation.py` must be accessible from the current Python environment.
Simply import it by

```
from Deviation import Deviation
```



Usage and Documentation
-----------------------

Given a set of measurement values <i>a<sub>1</sub>, a<sub>2</sub>, ..., a<sub>n</sub></i>
which can be described by a mean value _&mu;_ and a worst-case error _s_ by

<i>&mu; = </i>(<i>&#8721;<sub>i=1</sub><sup>n</sup> a<sub>i</sub></i>)<i> / n</i> and<br />
<i>s = </i>max(<i>|a<sup>i</sup> - &mu;|</i>) for <i>i = 1, n</i>.

If noise or measurement uncertainity is present,
_s_ is always a (possibly small) positive value.
A pair of mean value and its worst-case errorcan be used to describe the measured values.
This pair is the base type of the Deviation class.

The Deviation class can be useful,
if the error contribution of basic arithmetic operations on those measured values is of interest.
Apart from defining the initial values as instances of the Deviation class,
basic calculations can be done as usual without any changes.
The error propagation used in this class will automatically calculate the worst-case impact
on the overall error of each operation.
The current worst-case error can be obtained by simply printing the corresponding (intermediate) value or result.

In the following example,
a Deviation instance `dev` is initialized with a list of measured values.
Mean value and worst-case error are automatically computed when using `from_list()`.

```
value_list = [4.477, 4.423, 4.452];

dev = Deviation();
dev.from_list(value_list);
```

Supported arithmetic operations with instances of the Deviation class are `+`, `-`, `*`, `/` and `**`.
The operations can include one or more `int`, `float` and other Deviation instances like:

```
offset = Deviation();
offset.from_list([1.02, 1.01, 1.02, 1.02, 1.02, 1.01]);

fac = Deviation();
fac.from_list([4.332, 4.340, 4.328]);

result = (offset + 2.0)*7.55 - fac**2;

print('\n'.join([str(round(x, 5)) for x in [offset, fac, result]]));
```

In this example, `offset = 1.01667 ±0.00667` and `fac = 4.33333 ±0.00667`.
The result 3.99806 ±0.10816 shows,
that the calculated value is between 3.88990 and 4.10622
(the mean value and worst-case error can be obtained with the `get_values()` method).



Worst-case error in basic arithmetic operations
-----------------------------------------------

Supported operations with the Deviation package are

 - Addition (<i>&mu;<sub>a</sub> ± s<sub>a</sub></i>)<i> + </i>(<i>&mu;<sub>b</sub> ± s<sub>b</sub></i>) ,<br />
 - Subtraction (<i>&mu;<sub>a</sub> ± s<sub>a</sub></i>)<i> - </i>(<i>&mu;<sub>b</sub> ± s<sub>b</sub></i>) ,<br />
 - Multiplication (<i>&mu;<sub>a</sub> ± s<sub>a</sub></i>)<i> &middot; </i>(<i>&mu;<sub>b</sub> ± s<sub>b</sub></i>) ,<br />
 - Division (<i>&mu;<sub>a</sub> ± s<sub>a</sub></i>)<i> / </i>(<i>&mu;<sub>b</sub> ± s<sub>b</sub></i>) and<br />
 - Exponentiation (<i>&mu;<sub>a</sub> ± s<sub>a</sub></i>)<i> ^ </i>(<i>&mu;<sub>b</sub> ± s<sub>b</sub></i>).

Also, rounding has different effects on the mean value and the worst-case error.
The mean value behaves as expected (round to nearest)
while the worst-case error does round to the next value.
Also, the worst-case error factors in the change of the mean value due to rounding before rounding to the next value,
i.e. <i>s<sub>mod</sub> = s + |&mu; - </i>round(<i>&mu;</i>)<i>|</i>.
So rounding the result 3.9980544 ±0.1083883 gives the results shown in the following table.


| Num. digits  | Result               | Note                      |
| ------------ | -------------------- | ------------------------- |
| 7            | 3.9980544 ±0.1083883 | -                         |
| 6            | 3.998054 ±0.108389   | -                         |
| 5            | 3.99805 ±0.1084      | next (mean contribution)  |
| 4            | 3.9981 ±0.1085       | next                      |
| 3            | 3.998 ±0.109         | next <sup>m</sup>         |
| 2            | 4.00 ±0.11           | -                         |
| 1            | 4.0 ±0.2             | next                      |
| 0            | 4 ±1                 | next                      |
| -1           | 0 ±10                | next                      |


Entries marked with _next_ were rounded to the next value.
This is mostly influenced by the worst-case error itself,
but can also occur due to contribution of the mean value rounding (one example is marked with _mean contribution_).
Rounding to less digits will never result in a lower worst-case error
but the absolute bounds given by mean value plus/minus worst-case-error might not always increase in both directions
(e.g for the lower bound at <sup>m</sup> and the next value).


**Addition and Subtraction**

The worst-case error for addition and subtraction can be bounded by

<i>&mu;<sub>a</sub> + &mu;<sub>b</sub> - </i>(<i>s<sub>a</sub> + s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; &#8804; &nbsp;&nbsp;&nbsp;
</i>(<i>&mu;<sub>a</sub> ± s<sub>a</sub></i>)<i> + </i>(<i>&mu;<sub>b</sub> ± s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; &#8804; &nbsp;&nbsp;&nbsp;
&mu;<sub>a</sub> + &mu;<sub>b</sub> + </i>(<i>s<sub>a</sub> + s<sub>b</sub></i>) and<br />
<i>&mu;<sub>a</sub> - &mu;<sub>b</sub> - </i>(<i>s<sub>a</sub> + s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; &#8804; &nbsp;&nbsp;&nbsp;
</i>(<i>&mu;<sub>a</sub> ± s<sub>a</sub></i>)<i> - </i>(<i>&mu;<sub>b</sub> ± s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; &#8804; &nbsp;&nbsp;&nbsp;
&mu;<sub>a</sub> - &mu;<sub>b</sub> + </i>(<i>s<sub>a</sub> + s<sub>b</sub></i>)

and therefore yielding the sum of the individual errors as new value after the operation.
We assume <i>&mu;<sub>a</sub> &#8805; 0</i> and <i>&mu;<sub>b</sub> &#8805; 0</i> (otherwise factor -1 out).


**Multiplication**

For multiplication the following possibilities have to be considered:

(<i>&mu;<sub>a</sub> + s<sub>a</sub></i>)<i> &middot; </i>(<i>&mu;<sub>b</sub> + s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; = &nbsp;&nbsp;&nbsp; &mu;<sub>a</sub>&mu;<sub>b</sub> + </i>(<i>&mu;<sub>a</sub>s<sub>b</sub> + &mu;<sub>b</sub>s<sub>a</sub> + s<sub>a</sub>s<sub>b</sub></i>) ,<br />
(<i>&mu;<sub>a</sub> + s<sub>a</sub></i>)<i> &middot; </i>(<i>&mu;<sub>b</sub> - s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; = &nbsp;&nbsp;&nbsp; &mu;<sub>a</sub>&mu;<sub>b</sub> + </i>(<i>-&mu;<sub>a</sub>s<sub>b</sub> + &mu;<sub>b</sub>s<sub>a</sub> - s<sub>a</sub>s<sub>b</sub></i>) ,<br />
(<i>&mu;<sub>a</sub> - s<sub>a</sub></i>)<i> &middot; </i>(<i>&mu;<sub>b</sub> + s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; = &nbsp;&nbsp;&nbsp; &mu;<sub>a</sub>&mu;<sub>b</sub> + </i>(<i>&mu;<sub>a</sub>s<sub>b</sub> - &mu;<sub>b</sub>s<sub>a</sub> - s<sub>a</sub>s<sub>b</sub></i>) and<br />
(<i>&mu;<sub>a</sub> - s<sub>a</sub></i>)<i> &middot; </i>(<i>&mu;<sub>b</sub> - s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; = &nbsp;&nbsp;&nbsp; &mu;<sub>a</sub>&mu;<sub>b</sub> + </i>(<i>-&mu;<sub>a</sub>s<sub>b</sub> - &mu;<sub>b</sub>s<sub>a</sub> + s<sub>a</sub>s<sub>b</sub></i>) .

For any values <i>&mu;<sub>a</sub></i> and <i>&mu;<sub>b</sub></i>,
the worst-case error is
<i>|&mu;<sub>a</sub>|s<sub>b</sub> + |&mu;<sub>b</sub>|s<sub>a</sub> + s<sub>a</sub>s<sub>b</sub></i>.


**Division**

Division has the following cases

(<i>&mu;<sub>a</sub> + s<sub>a</sub></i>)<i> / </i>(<i>&mu;<sub>b</sub> + s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; = &nbsp;&nbsp;&nbsp; &mu;<sub>a</sub> / </i>(<i>&mu;<sub>b</sub> + s<sub>b</sub></i>)<i> + s<sub>a</sub>/ </i>(<i>&mu;<sub>b</sub> + s<sub>b</sub></i>) ,<br />
(<i>&mu;<sub>a</sub> + s<sub>a</sub></i>)<i> / </i>(<i>&mu;<sub>b</sub> - s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; = &nbsp;&nbsp;&nbsp; &mu;<sub>a</sub> / </i>(<i>&mu;<sub>b</sub> - s<sub>b</sub></i>)<i> + s<sub>a</sub>/ </i>(<i>&mu;<sub>b</sub> - s<sub>b</sub></i>) ,<br />
(<i>&mu;<sub>a</sub> - s<sub>a</sub></i>)<i> / </i>(<i>&mu;<sub>b</sub> + s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; = &nbsp;&nbsp;&nbsp; &mu;<sub>a</sub> / </i>(<i>&mu;<sub>b</sub> + s<sub>b</sub></i>)<i> - s<sub>a</sub>/ </i>(<i>&mu;<sub>b</sub> + s<sub>b</sub></i>) and<br />
(<i>&mu;<sub>a</sub> - s<sub>a</sub></i>)<i> / </i>(<i>&mu;<sub>b</sub> - s<sub>b</sub></i>)<i> &nbsp;&nbsp;&nbsp; = &nbsp;&nbsp;&nbsp; &mu;<sub>a</sub> / </i>(<i>&mu;<sub>b</sub> - s<sub>b</sub></i>)<i> - s<sub>a</sub>/ </i>(<i>&mu;<sub>b</sub> - s<sub>b</sub></i>) .

Considering the cases for positive <i>&mu;<sub>a</sub>, &mu;<sub>b</sub></i>
(and optionally factoring −1 out),
the worst-case error is the absolute value of
(<i>|&mu;<sub>a</sub>| + s<sub>a</sub></i>)<i> / </i>(<i>|&mu;<sub>b</sub>| - s<sub>b</sub></i>)<i> - |&mu;<sub>a</sub> / &mu;<sub>b</sub>|</i>.


**Exponentiation**

Raising to the power has the following cases

(<i>&mu;<sub>a</sub> + s<sub>a</sub></i>)<i> ^ </i>(<i>&mu;<sub>b</sub> + s<sub>b</sub></i>) ,<br />
(<i>&mu;<sub>a</sub> + s<sub>a</sub></i>)<i> ^ </i>(<i>&mu;<sub>b</sub> - s<sub>b</sub></i>) ,<br />
(<i>&mu;<sub>a</sub> - s<sub>a</sub></i>)<i> ^ </i>(<i>&mu;<sub>b</sub> + s<sub>b</sub></i>) and<br />
(<i>&mu;<sub>a</sub> - s<sub>a</sub></i>)<i> ^ </i>(<i>&mu;<sub>b</sub> - s<sub>b</sub></i>) .

where <i>&mu;<sub>a</sub> - s<sub>a</sub> &#8805; 0</i>.
The worst-case error depends on whether
<i>&mu;<sub>b</sub> - s<sub>b</sub> &lt; 0</i> and <i>&mu;<sub>1</sub> - s<sub>1</sub> &lt; 1</i>,
so that the maximum (absolute) value of all four cases is used.



Contributing
------------

**Bug reports**

If you found a bug, make sure you can reproduce it with the latest version of Deviation.
Please check that the expected results can actually be achieved by other means
and are not considered invalid operations.
Please give detailed and reproducible instructions in your report including

 - the Deviation version
 - the expected result
 - the result you received
 - the command(s) used as a _minimal working example_

Note: The bug should ideally be reproducible by the _minimal working example_ alone.
Please keep the example code as short as possible (minimal).


**Feature requests**

If you have an idea for a new feature, consider searching the
[open issues](https://github.com/d-zo/Deviation/issues) and
[closed issues](https://github.com/d-zo/Deviation/issues?q=is%3Aissue+is%3Aclosed) first.
Afterwards, please submit a report in the
[Issue tracker](https://github.com/d-zo/Deviation/issues) explaining the feature and especially

 - why this feature would be useful (use cases)
 - what could possible drawbacks be (e.g. compatibility, dependencies, ...)



License
-------

Deviation is released under the
[GPL](https://www.gnu.org/licenses/gpl-3.0.html "GNU General Public License"),
version 3 or greater (see als [LICENSE](https://github.com/d-zo/Deviation/blob/master/LICENSE) file).
It is provided without any warranty.

