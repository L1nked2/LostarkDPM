class Base:
    def __init__(self):
        self.base_num = 1
        print("Init Base...")
    
    def method_Base(self):
        print("Call method_Base...")
    
    def increase(self):
        self.base_num += 1

class A(Base):
    def __init__(self):
        super(A, self).__init__()
        print("Init A...")
    
    def method_A(self):
        print("Call method_A...")

class B(A):
    def __init__(self):
        super(B, self).__init__()
        super(A, self).method_Base()
        print("Init B...")
    
    def method_A(self):
        print("Call overridded method_A...")

class C(B):
    def __init__(self):
        super(C, self).__init__()
        print("Init C...")
    
    def method_C(self):
        super(A, self).increase()
        
        print("Call method_C...")
        print(self.base_num)


my_class = C()
my_class.method_C()