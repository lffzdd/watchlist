class Animal:
    def __init__(self, breed):
        self.breed = breed

    def make_sound(self):
        pass

class Dog(Animal):
    def __init__(self,breed,name):
        super().__init__(breed)
        self.name=name

    def make_sound(self):
        return 'Woof!'

class Cat(Animal):
    def __init__(self,breed,color):
        super().__init__(breed)
        self.color=color

    def make_sound(self):
        return 'Meow!'

dog=Dog('中华田园犬','小黑')
cat=Cat('橘猫','橙色')