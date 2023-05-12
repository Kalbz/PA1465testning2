# Assigment 2: Fuzzing

## 1. Introduction

In this assignment, we will apply differential fuzzing to the JSON encoding of three different Python libraries. Those are in detail

- [`json`](https://docs.python.org/3/library/json.html)
- [`orjson`](https://github.com/ijl/orjson)
- [`msgspec`](https://github.com/jcrist/msgspec)

The fuzzer shall find

1. all differences in the resulting encoded data
2. all (valid) input data that raise exceptions

for each of the JSON libraries. You can install `orjson` and `msgspec` libraries via `pip3 install orjson msgspec`.

Create a single file named `fuzzing_json.py`. This file must contain the function `random_data_generator()` that generates the input for the differential fuzzing of all three libraries. Of course, you can add other (helper) functions or customize `main()` and the comparison as needed.

## Constraints

- No external dependencies outside the standard library (that means no components via `pip install`)
- Don't use parallelization (i.e., threads or processes).
- Only valid data structures that should be JSON-serializable count! Therefore, make yourself familiar with the [specification of JSON and its data types](https://www.ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf)

## Some hints

- Make yourself familiar with the `main()` function and the parametrization of the libraries.
- The ChatGPT solution is a slippery slope. Why?
- We recommend having an eye on performance: The more checks the fuzzer can compute, the better. There may be smarter ways to create edge cases for data generation other than brute force.

## The Best JSON Fuzzer Award

The fuzzer that identifies the most potential bugs in the shortest run-time will receive the **Best JSON Fuzzer Award** and, of course, glory and honor!

How we will find the best fuzzer:

1. We use your random input generator (via its name `random_data_generator()`) to compare the three components on our servers for a certain timespan in a separate and parallelized checking routine to make it fair and comparable.
2. We evaluate and double-check the findings.
3. We award the fuzzer that identified the most issues.

## Submit

Please submit

- `fuzzing_json.py` with the customized function `random_data_generator()`
- a description in a separate file named `description.md` on your design decisions on the random data generator and a short discussion of your findings.
