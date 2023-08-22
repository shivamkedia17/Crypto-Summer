from eclib import *
from pathlib import Path
import sys
import io

def read_params(file_path):
    # check if it's a file of the correct type
    if not (Path(file_path).is_file() and (Path(file_path).suffix == '.txt')):
        sys.exit("Incorrect file format.")

    with open(file=file_path) as file:
        # (P, a, b)
        return tuple( file.readline().split(' ')[:3] ) 
        

def read_point(iostream, ec):
    if not (
        isinstance(iostream, io.TextIOBase) 
        # or isinstance(iostream, io.BufferedIOBase) 
        # or isinstance(iostream, io.RawIOBase) 
        # or isinstance(iostream, io. IOBase)
    ):
        raise TypeError("Can't Read Point from Non-IOStream.")

    if not isinstance(ec, EC):
        raise TypeError("Provide an elliptic curve to check if point belongs.")

    pt = tuple( iostream.readline().split(' ')[:2] )
    (x, y) = (Bn.from_decimal(pt[0]),  Bn.from_decimal(pt[1]))
    
    if ec.check_point(x, y):
        return (x, y)
    else:
        raise ValueError("Point doesn't belong to given elliptic curve group.")


def write_point(iostream, point):
    if not (isinstance(iostream, io.TextIOBase)):
        raise TypeError("Can't Write Point to Non-IOStream.")

    iostream.write(f"{point.x} {point.y}")


def main():
    # Read file containing EC params
    n_args = len(sys.argv)

    if n_args == 1:
        filename = "param.txt"
    elif n_args == 2:
        # sys.argv[0] = "test_eclib.py"
        filename = sys.argv[1]
    else:
        sys.exit("Usage: python3 test_eclib.py [param_file]")

    # 1: Read file of EC domain params
    params = read_params(file_path=filename)
    p = Bn.from_decimal(params[0])
    a = Bn.from_decimal(params[1])
    b = Bn.from_decimal(params[2])

    # create curve using params
    ec = EC(p, a, b)

    # Read generator point from stream
    # TODO
    some_stream = None
    Gx,Gy = read_point(some_stream)

    # Testing Addition
    # TODO
    Ax, Ay = read_point(some_stream)
    Bx, By = read_point(some_stream)

    # Associativity
    assert(ec.add(Ax, Ay, Bx, By) == ec.add(Bx, By, Ax, Ay))

    # Identity
    assert(ec.add(Ax, Ay, *ec.zero) == ec.add(*ec.zero, Ax, Ay) == (Ax, Ay))

    # Inverse
    assert(ec.add(*(ec.negate(Ax, Ay)), Ax, Ay) == ec.zero)

    # Infinity
    assert(ec.add(*ec.zero, *ec.zero) == ec.zero)

    # Subtract
    Cx, Cy = ec.subtract(Ax, Ay, Bx, By)
    assert((Ax, Ay) == ec.add(Cx, Cy, Bx, By))

    # Multiplication
    k = 5
    ans_add = ec.zero
    for _ in range(k):
        ans_add = ec.add(*(ans_add), Ax, Ay)
    ans_mult = ec.mult_pt(Ax, Ay, k)
    assert(ans_add == ans_mult)

    k = Bn(2**64).random()
    m = Bn(2**64).random()
    assert(ec.mult_pt(*(ec.mult_pt(Ax, Ay, m), k)) == ec.mult_pt(Ax, Ay, k*m))

    # verify point on curve

if __name__ == "__main__":
    main()