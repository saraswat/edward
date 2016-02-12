import numpy as np
import tensorflow as tf

def set_seed(x):
    """
    Set seed for both NumPy and TensorFlow.
    """
    np.random.seed(x)
    tf.set_random_seed(x)

def dot(x, y):
    """
    x is M x N matrix and y is N-vector, or
    x is M-vector and y is M x N matrix
    """
    if len(x.get_shape()) == 1:
        vec = x
        mat = y
        d = vec.get_shape()[0].value
        return tf.matmul(tf.reshape(vec, [1, d]), mat)
    else:
        mat = x
        vec = y
        d = vec.get_shape()[0].value
        return tf.matmul(mat, tf.reshape(vec, [d, 1]))

def trace(X):
    # assumes square
    n = X.get_shape()[0].value
    mask = tf.diag(tf.ones([n], dtype=X.dtype))
    X = tf.mul(mask, X)
    return tf.reduce_sum(X)

def get_dims(x):
    """
    Get values of each dimension.

    Arguments
    ----------
    x: tensor scalar or array
    """
    dims = x.get_shape()
    if len(dims) == 0: # scalar
        return [1]
    else: # array
        return [dim.value for dim in dims]

def log_gamma(x):
    """
    use an approximation avoiding special functions, because
    TensorFlow doesn't currently support them
    http://www.machinedlearnings.com/2011/06/faster-lda.html
    """
    logterm = tf.log(x * (1.0 + x) * (2.0 + x))
    xp3 = 3.0 + x
    return -2.081061466 - x + 0.0833333 / xp3 - logterm + (2.5 + x) * tf.log (xp3)

def log_beta(x, y):
    """
    use an approximation avoiding special functions, because
    TensorFlow doesn't currently support them
    """
    return log_gamma(x) + log_gamma(y) - log_gamma(x+y)
