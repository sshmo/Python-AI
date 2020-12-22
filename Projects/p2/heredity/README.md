# Heredity

Write an AI to assess the likelihood that a person will have a particular genetic trait.

    $ python heredity.py data/family0.csv
    Harry:
      Gene:
        2: 0.0092
        1: 0.4557
        0: 0.5351
      Trait:
        True: 0.2665
        False: 0.7335
    James:
      Gene:
        2: 0.1976
        1: 0.5106
        0: 0.2918
      Trait:
        True: 1.0000
        False: 0.0000
    Lily:
      Gene:
        2: 0.0036
        1: 0.0136
        0: 0.9827
      Trait:
        True: 0.0000
        False: 1.0000

### The problem solving approch:

The problem was solved using Bayesian Networks.

A short video demonstrating my implementation of this project can be found [here](https://youtu.be/LEl4KzX1NEk).

### Specification

Specification for this project can be found [here](https://cs50.harvard.edu/ai/2020/projects/2/heredity/#specification).
