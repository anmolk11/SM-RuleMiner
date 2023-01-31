a = 1
def F():
    global a
    a = 8

if __name__ == "__main__":
    F()
    print(a)