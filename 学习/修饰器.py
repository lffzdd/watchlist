def decorator1(func):
    def wrapper1(*args, **kwargs):
        print("Decorator 1 executed")
        return func(*args, **kwargs)

    return wrapper1


def decorator2(func):
    def wrapper2(*args, **kwargs):
        print("Decorator 2 executed")
        return func(*args, **kwargs)

    return wrapper2


@decorator1
@decorator2
def example_func(name='hh', age=23):
    print(name, age)


example_func('刘非凡', 23)
