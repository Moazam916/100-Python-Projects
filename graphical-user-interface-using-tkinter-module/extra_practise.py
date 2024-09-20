def add(*args):
    sum = 0
    for i in args:
        print(i)
        sum += i
    return sum
function_output= add(1, 2, 2, 3)
print(function_output)


class Car:
    def __init__(self, **kwarg):
        self.make = kwarg.get("make")
        self.model = kwarg.get("model")

my_car= Car(make="Nissan")
print(my_car.model)