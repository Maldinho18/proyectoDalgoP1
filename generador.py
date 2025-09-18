import random

def main():
    T = 300  # número de casos
    print(T)
    for _ in range(T):
        k = random.randint(1, 10**4)        # celdas pequeñas
        n = random.randint(1, 10**5)       # energía total no muy grande
        P = [random.randint(1, 10**5) for _ in range(5)]  # pesos pequeños
        print(k, n, *P)

if __name__ == "__main__":
    main()
