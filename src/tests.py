from main import isIntersect_pro
from Parlgram import Parlgram
from Cylinder import Cylinder

def test(function_to_decorate):
    def try_except_wrapper():
        try:
            function_to_decorate()
        except AssertionError:
            print(f"{function_to_decorate.__name__} Failed")
            raise
        except:
            print(f"{function_to_decorate.__name__} unknown error")
            raise
        print(f"{function_to_decorate.__name__} Success")
    return try_except_wrapper

@test
def test_isIntersect_pro():
    p = Parlgram([2, 2, 2], [1, 1, 1])
    c = Cylinder([0, 0, 0], 1, 1)
    assert isIntersect_pro(c, p) == False
    assert isIntersect_pro(p, c) == False
    p = Parlgram([0, 0, 0], [1, 1, 1])
    c = Cylinder([0, 0, 0], 1, 1)
    assert isIntersect_pro(c, p) == True
    assert isIntersect_pro(p, c) == True
    p = Parlgram([1, 1, 1], [1, 1, 1])
    c = Cylinder([0, 0, 0], 1, 1)
    assert isIntersect_pro(c, p) == True
    assert isIntersect_pro(p, c) == True

if __name__ == '__main__':
    test_isIntersect_pro()