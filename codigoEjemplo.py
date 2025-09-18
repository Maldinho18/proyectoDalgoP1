#!/usr/bin/env python3
# ProblemaP1.py
# Autores: <TU NOMBRE(S) AQUÍ>
# Descripción: DP por dígitos con acarreo + aceleración por clases mod 3 y RMQ.
# Cumple: 1 ≤ k ≤ 1e4, 1 ≤ n ≤ 1e5, 1 ≤ Pi ≤ 1e5, múltiples casos, salida "streaming".

import sys
from math import ceil, floor, log2

INF_NEG = -10**30

def build_sparse(arr):
    """RMQ (máximo) con Sparse Table. Devuelve (st, log) donde:
       st[j][i] = max en arr[i .. i+2^j-1]"""
    n = len(arr)
    if n == 0:
        return [], []
    K = int(log2(n)) + 1
    st = [arr[:] ]  # nivel 0
    j = 1
    while (1 << j) <= n:
        prev = st[j-1]
        size = n - (1 << j) + 1
        cur = [0]*size
        half = 1 << (j-1)
        for i in range(size):
            a = prev[i]
            b = prev[i + half]
            cur[i] = a if a >= b else b
        st.append(cur)
        j += 1
    # logs para longitudes
    lg = [0]*(n+1)
    for i in range(2, n+1):
        lg[i] = lg[i//2] + 1
    return st, lg

def rmq_max(st, lg, L, R):
    """Máximo en arr[L..R] en O(1). Si L>R => -inf."""
    if L > R:
        return INF_NEG
    k = lg[R - L + 1]
    a = st[k][L]
    b = st[k][R - (1<<k) + 1]
    return a if a >= b else b

def solve_case(k, n, P):
    # P es lista [P0..P4]; para p>=5, peso 0
    weights = P + [0]  # p=5 con 0

    # Dígitos de n hasta p=5
    nd = []
    x = n
    for _ in range(6):
        nd.append(x % 10)
        x //= 10
    # nd[p] = dígito de n en 10^p

    # DP hacia atrás: F_{6}(0)=0; F_{6}(c>0)=-inf
    # Representamos F como lista de valores para c_in en un dominio [0..C_in_max]
    F_next = [0]  # solo c_in=0 es válido al final
    Cmax_next = 0  # dominio de índices de F_next

    # Procesamos p = 5,4,3,2,1,0
    for p in range(5, -1, -1):
        Pp = weights[p]
        np_ = nd[p]

        # Dominio posible de c_in en esta posición:
        # Para que exista c_out en [0..Cmax_next], debe cumplirse:
        # ceil((c_in - np_)/10) <= Cmax_next  => c_in <= np_ + 10*Cmax_next
        Cmax_in = np_ + 10 * Cmax_next
        # F_p tendrá tamaño Cmax_in+1 (c in 0..Cmax_in)
        F_cur = [INF_NEG] * (Cmax_in + 1)

        # Prepara H[c_out] = F_{p+1}(c_out) + 3*Pp*c_out en 0..Cmax_next
        H = [F_next[c] + 3*Pp*c for c in range(Cmax_next + 1)]

        # Para cada residuo r, construimos A_r[q] = H[3q+r] + Pp*q
        # con índices válidos 3q+r <= Cmax_next
        A = []
        ST = []
        LG = []
        for r in range(3):
            arr = []
            q = 0
            while 3*q + r <= Cmax_next:
                arr.append(H[3*q + r] + Pp*q)
                q += 1
            A.append(arr)
            st, lg = build_sparse(arr)
            ST.append(st)
            LG.append(lg)

        # Para cada c_in calculamos su mejor valor con RMQ por residuos
        # c_out factible depende de c_in:
        # L = ceil((c_in - np_)/10), U = floor((9k + c_in - np_)/10)
        # y además 0 <= c_out <= Cmax_next.
        for c_in in range(Cmax_in + 1):
            L = ceil((c_in - np_) / 10) if (c_in > np_) else 0
            if L < 0: L = 0
            U = floor((9*k + c_in - np_) / 10)
            if U > Cmax_next: U = Cmax_next
            if L > U:
                continue  # imposible

            best = INF_NEG
            # Para cada r = 0,1,2:
            for r in range(3):
                # c_out = 3q + r in [L..U]  => q in [ceil((L-r)/3) .. floor((U-r)/3)]
                qL = (L - r + 2) // 3  # ceil
                qU = (U - r) // 3      # floor
                if qL < 0: qL = 0
                if qU >= 0 and qL <= qU and len(A[r]) > 0:
                    part = rmq_max(ST[r], LG[r], qL, qU)
                    # + Pp * floor((np_ - c_in + r)/3)
                    part += Pp * ((np_ - c_in + r) // 3)
                    if part > best:
                        best = part
            F_cur[c_in] = best

        # Avanza
        F_next = F_cur
        Cmax_next = Cmax_in

    # La respuesta es F_0(0)
    return F_next[0]

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    # Para salida "streaming": imprimimos y flush en cada caso
    for _ in range(t):
        k = int(next(it)); n = int(next(it))
        P0 = int(next(it)); P1 = int(next(it)); P2 = int(next(it)); P3 = int(next(it)); P4 = int(next(it))
        ans = solve_case(k, n, [P0, P1, P2, P3, P4])
        print(ans)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
