
class Command():
    def __init__(self, data):
        self.data = data
        print(self.__dict__)

    def func(self, value):
        print(value)

    def direct(self):
        def oui(self):
            print("yeye")
        print(self.data)

test = Command(10)
for i in dir(test):
    print(i, type(i))
