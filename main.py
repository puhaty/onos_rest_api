from routing import the_shorthest_path

if __name__ == '__main__':
    print("Enter first host address:")
    h1 = input()
    print("Enter dst host address:")
    h2 = input()
    the_shorthest_path(h1, h2)