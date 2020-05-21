# Spaces

Spaces are a way to represent the environment it's action and observation space. An observation can for example be a discrete observation in the range of numbers between 0 and 1, but it could also be an image that was captured.

## Discrete

[https://github.com/openai/gym/blob/master/gym/spaces/discrete.py](https://github.com/openai/gym/blob/master/gym/spaces/discrete.py)

A discrete space will allow you to represent a linear space (e.g. `0, 1, 2, ..., n - 1` for a given `n`), this can be used in situations where you would need to represent 4 actions, which would be written as `Discrete(4)`.

## Box

[https://github.com/openai/gym/blob/master/gym/spaces/box.py](https://github.com/openai/gym/blob/master/gym/spaces/box.py)

As defined by OpenAI, a box represents the Cartesian product of $n$ closed intervals, which have the form of one of $[a, b]$, $(-\infty , b]$, $[a, \infty )$ or $(-\infty , \infty )$.

A square would thus be represented as `Box(2, )` where we would observe 2 values (e.g. {x, y} values). Similar, `Box(3, )` would represent 3 values (e.g. {x, y, z}).

In the definition of our box, we include a parameter to define the boundaries of the dimensions.

For optimality, we include a Box implementation for Float and Int datatypes.

## Tuple

[https://github.com/openai/gym/blob/master/gym/spaces/tuple.py](https://github.com/openai/gym/blob/master/gym/spaces/tuple.py)

The Tuple space is a combination of other spaces, this allows you to represent more complex states that exist out of multiple substate.

Example:
Let's say that we want to represent the following state:

- Image (64x64 px RGB)
- {x, y, z} coordinates in a cube between -50 and 50
- { Dead, Alive, Resurrecting } represented as { 0, 1, 2 }

We could write this as: `Tuple([ Box(0, 255, shape=(64, 64, 3)), Box(-50, 50, shape=(3, )) ])`