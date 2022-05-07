from routing import Routing
if __name__ == '__main__':
    r = Routing()
    while True:
        print("exit: exit")
        print("Enter first host address:")
        h1 = input()
        if h1 == "exit":
            break
        else:
            print("Enter dst host address:")
            h2 = input()
            r.the_shorthest_path(h1, h2)

