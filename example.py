class People():
    def __init__(self, name):
        self.name = name


arr2 = [
    {
        "age": 12,
    },
    {
        "age": 13,
    },
    {   
        "age": 14,
    }
]

person_1 = People(name="ahmed")
person_2 = People(name="shaikh")
person_3 = People(name="khan")

people = []

arr = ["shaikh"]

filtered_data = filter(lambda person: print(person.name), )

