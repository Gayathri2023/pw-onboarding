import pytest
class maths:
    def __init__(self,a,b):
        self.a=a
        self.b=b
    def add(self):
        return self.a+self.b
    def sub(self):
        return self.a-self.b
    def mul(self):
        return self.a*self.b
    def div(self):
        return self.a/self.b
    def floor_div(self):
        return self.a//self.b
    def mod(self):
        return self.a%self.b
 


# Test case
def test_add():
    assert maths(2,3).add() == 5
    assert maths(-1, 1).add() == 0
def test_add_negative():  
    with pytest.raises(AssertionError):
        assert maths(-1, 1).add() == 6
        
def test_sub():
    assert maths(5,2).sub()== 3
    assert maths(-5,2).sub()== -7
def test_sub_negative():
       with pytest.raises(TypeError):
        assert maths(-5, "").sub() == 7
    
def test_mul():
    assert maths(10,2).mul()== 20
    assert maths(-10,2).mul()== -20
def test_mul_negative():
       with pytest.raises(TypeError):
        assert maths(-10,).mul() == 20
        
def test_div():
    assert maths(10,2).div()== 5
    assert maths(-10,2).div()== -5
def test_div_negative():
       with pytest.raises(ZeroDivisionError):
        assert maths(-10,0).div()
        
def test_floor_div():
    assert maths(100,10).floor_div()== 10
    assert maths(-100,10).floor_div()== -10
def test_floor_div_negative():
    with pytest.raises(ZeroDivisionError):
        assert maths(100,0).floor_div()
        
def test_mod():
    assert maths(100,10).mod()== 0
    assert maths(-100,10).mod()== 0
def test_floor_div_negative():
    with pytest.raises(ZeroDivisionError):
        assert maths(100,0).mod()       