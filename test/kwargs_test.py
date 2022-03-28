class Base:
    def __init__(self, y):
        print("Base:", y)

class A(Base):
    def __init__(self, z, **kwargs):
        super(A, self).__init__(**kwargs)
        # print(type(kwargs))
        print("A:", z)

class B(A):
    def __init__(self, x, **kwargs):
        super(B, self).__init__(**kwargs)
        print("B:", x)

b = B(1, y=2, z=3)