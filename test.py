import copy


class Test:
    a = 2

    def change_a(self):
        self.a += 1


def edit_a(test):
    test = copy.copy(test)
    test.change_a()
    print("1", test.a)

test = Test()
edit_a(test)
print(test.a)
