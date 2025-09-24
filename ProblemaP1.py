import sys
from math import ceil, floor

INF_NEG = -10**30

def construir(arr):
    n = len(arr)
    if n == 0:
        return [], []
    tabla_maximos = [arr[:] ]
    nivel = 1
    while (1 << nivel) <= n:
        nivel_anterior = tabla_maximos[nivel-1]
        tamano = n - (1<<nivel) + 1
        nivel_actual = [0]*tamano
        mitad = 1 << (nivel-1)
        for i in range(tamano):
            a = nivel_anterior[i]
            b = nivel_anterior[i + mitad]
            nivel_actual[i] = a if a >= b else b
        tabla_maximos.append(nivel_actual)
        nivel += 1
    lg = [0]*(n+1)
    for i in range(2, n+1):
        lg[i] = lg[i//2] + 1
    return tabla_maximos, lg

def max(tabla_maximos, lg, inicio, fin):
    if inicio > fin:
        return INF_NEG
    k = lg[fin - inicio + 1]
    a = tabla_maximos[k][inicio]
    b = tabla_maximos[k][fin - (1<<k) + 1]
    return a if a >= b else b

def resolver_caso(k, n, pesos_base):
    pesos = pesos_base + [0]
    digitos = []
    x = n
    for _ in range(6):
        digitos.append(x % 10)
        x //= 10
    siguiente = [0]
    max_siguiente = 0
    
    for p in range(5, -1, -1):
        peso_actual = pesos[p]
        digito_actual = digitos[p]
        max_in = digito_actual + 10 * max_siguiente
        resultado_actual = [INF_NEG] * (max_in + 1)
        valores_transformados = [siguiente[c] + 3*peso_actual*c for c in range(max_siguiente + 1)]
        listas_r = []
        tablas = []
        LG = []
        for residuo in range(3):
            arr = []
            q = 0
            while 3*q + residuo <= max_siguiente:
                arr.append(valores_transformados[3*q + residuo] + peso_actual*q)
                q += 1
            listas_r.append(arr)
            tabla_maximos, lg = construir(arr)
            tablas.append(tabla_maximos)
            LG.append(lg)
        
        for c_in in range(max_in + 1):
            limite_inferior = ceil((c_in - digito_actual) / 10) if (c_in > digito_actual) else 0
            if limite_inferior < 0: limite_inferior = 0
            limite_superior = floor((9*k + c_in - digito_actual) / 10)
            if limite_superior > max_siguiente: limite_superior = max_siguiente
            if limite_inferior > limite_superior:
                continue
            best = INF_NEG
            for residuo in range(3):
                inicio_q = (limite_inferior - residuo + 2) // 3
                fin_q = (limite_superior - residuo) // 3
                if inicio_q < 0: inicio_q = 0
                if fin_q >= 0 and inicio_q <= fin_q and len(listas_r[residuo]) > 0:
                    part = max(tablas[residuo], LG[residuo], inicio_q, fin_q)
                    part += peso_actual * ((digito_actual - c_in + residuo) // 3)
                    if part > best:
                        best = part
            resultado_actual[c_in] = best
        siguiente = resultado_actual
        max_siguiente = max_in
    return siguiente[0]

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        k = int(next(it)); n = int(next(it))
        P0 = int(next(it)); P1 = int(next(it)); P2 = int(next(it)); P3 = int(next(it)); P4 = int(next(it))
        ans = resolver_caso(k, n, [P0, P1, P2, P3, P4])
        print(ans)
        sys.stdout.flush()

if __name__ == "__main__":
    main()