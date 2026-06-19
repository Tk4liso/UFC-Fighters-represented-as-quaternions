class Quaternion:

    # CONSTRUCCIÓN
    def __init__(self, a, b, c, d):
        """
        Crea un cuaternión  q = a + bi + cj + dk

        Parámetros
        ----------
        a : parte escalar  (real)
        b : coeficiente de i
        c : coeficiente de j
        d : coeficiente de k
        """
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)

    # REPRESENTACIÓN LEGIBLE
    # __repr__ se llama automáticamente cuando se hace print(q) o se escribe q en la consola.
    def __repr__(self):
        def _term(val, symbol):
            sign = "+" if val >= 0 else "-"
            return f" {sign} {abs(val):.4g}{symbol}"
        return f"({self.a:.4g}{_term(self.b,'i')}{_term(self.c,'j')}{_term(self.d,'k')})"

    
    # SUMA Y RESTA  —  componente a componente, igual que los complejos
    # (a1+b1i+c1j+d1k) + (a2+b2i+c2j+d2k) = (a1+a2) + (b1+b2)i + ...
    def __add__(self, other):
        return Quaternion(self.a + other.a, self.b + other.b,
                          self.c + other.c, self.d + other.d)

    def __sub__(self, other):
        return Quaternion(self.a - other.a, self.b - other.b,
                          self.c - other.c, self.d - other.d)

    # Negación unaria: -q
    def __neg__(self):
        return Quaternion(-self.a, -self.b, -self.c, -self.d)


    # MULTIPLICACIÓN POR ESCALAR  (número real × cuaternión)
    def __rmul__(self, scalar):
        """Permite escribir  3 * q  (escalar a la izquierda)."""
        return Quaternion(scalar * self.a, scalar * self.b,
                          scalar * self.c, scalar * self.d)

    def __truediv__(self, scalar):
        """Permite escribir  q / 2."""
        return Quaternion(self.a / scalar, self.b / scalar,
                          self.c / scalar, self.d / scalar)

    
    # MULTIPLICACIÓN CUATERNIÁTICA  —  NO es conmutativa: p*q ≠ q*p
    def __mul__(self, other):
        # Si 'other' es un número real, delegar a __rmul__ del escalar
        if isinstance(other, (int, float)):
            return Quaternion(self.a * other, self.b * other,
                              self.c * other, self.d * other)

        a1, b1, c1, d1 = self.a, self.b, self.c, self.d
        a2, b2, c2, d2 = other.a, other.b, other.c, other.d

        return Quaternion(
            a1*a2 - b1*b2 - c1*c2 - d1*d2,   # parte real
            a1*b2 + b1*a2 + c1*d2 - d1*c2,   # coef. i
            a1*c2 - b1*d2 + c1*a2 + d1*b2,   # coef. j
            a1*d2 + b1*c2 - c1*b2 + d1*a2    # coef. k
        )

    # -------------------------------------------------------------------------
    # CONJUGADO, NORMA Y NORMALIZACIÓN
    def conjugate(self):
        """
        q* = a − bi − cj − dk
        Propiedad clave: q · q* = ||q||²  (siempre un número real positivo)
        """
        return Quaternion(self.a, -self.b, -self.c, -self.d)

    def norm(self):
        """
        ||q|| = sqrt(a² + b² + c² + d²)
        Es la "longitud" del cuaternión en ℝ⁴.
        """
        return (self.a**2 + self.b**2 + self.c**2 + self.d**2) ** 0.5

    def normalize(self):
        """
        Devuelve el cuaternión unitario:  q / ||q||
        Los cuaterniones unitarios (norma = 1) representan rotaciones 3D.
        """
        n = self.norm()
        if n == 0:
            raise ValueError("El cuaternión cero no se puede normalizar.")
        return self / n

    
    # INVERSO  —  q⁻¹ = q* / ||q||² | Útil porque q * q⁻¹ = 1  (cuaternión identidad)
    def inverse(self):
        n2 = self.norm() ** 2
        if n2 == 0:
            raise ValueError("El cuaternión cero no tiene inverso.")
        return self.conjugate() / n2


    # IGUALDAD (con tolerancia numérica para floats)
    def __eq__(self, other, tol=1e-9):
        return (abs(self.a - other.a) < tol and
                abs(self.b - other.b) < tol and
                abs(self.c - other.c) < tol and
                abs(self.d - other.d) < tol)

    
    # DESEMPAQUETADO  —  permite escribir  a, b, c, d = q
    def __iter__(self):
        return iter((self.a, self.b, self.c, self.d))



# =============================================================================
# TESTS  —  ejecuta este archivo directamente para verificar que todo funciona
# =============================================================================

if __name__ == "__main__":

    print("= TEST 1 — Representación =")
    q = Quaternion(1, 2, -3, 4)
    print(f"  q = {q}")                          # (1 + 2i - 3j + 4k)


    print("\n= TEST 2 — Suma y resta =")
    p = Quaternion(1, 0,  2, -1)
    q = Quaternion(0, 1, -1,  3)
    print(f"  p     = {p}")
    print(f"  q     = {q}")
    print(f"  p + q = {p + q}")                  # (1 + 1i + 1j + 2k)
    print(f"  p - q = {p - q}")                  # (1 - 1i + 3j - 4k)


    print("\n= TEST 3 — Multiplicación  (verifica no-conmutatividad) =")
    i = Quaternion(0, 1, 0, 0)
    j = Quaternion(0, 0, 1, 0)
    k = Quaternion(0, 0, 0, 1)

    print(f"  i·j = {i * j}   → debe ser (0 + 0i + 0j + 1k) = k")
    print(f"  j·i = {j * i}   → debe ser (0 + 0i + 0j - 1k) = -k")
    print(f"  j·k = {j * k}   → debe ser i")
    print(f"  k·i = {k * i}   → debe ser j")
    print(f"  i·i = {i * i}   → debe ser -1  (0 - 1i + 0j + 0k = -1)")


    print("\n= TEST 4 — Conjugado y norma =")
    q = Quaternion(1, 2, 3, 4)
    print(f"  q      = {q}")
    print(f"  q*     = {q.conjugate()}")
    print(f"  ||q||  = {q.norm():.6f}   → debe ser sqrt(30) ≈ 5.477226")
    print(f"  q·q*   = {q * q.conjugate()}   → parte real = ||q||² = 30, resto = 0")


    print("\n= TEST 5 — Normalización =")
    q_unit = q.normalize()
    print(f"  q normalizado = {q_unit}")
    print(f"  norma         = {q_unit.norm():.10f}   → debe ser exactamente 1.0")


    print("\n= TEST 6 — Inverso  (q · q⁻¹ debe dar el cuaternión identidad) =")
    q     = Quaternion(1, 2, 3, 4)
    q_inv = q.inverse()
    identidad = q * q_inv
    print(f"  q⁻¹    = {q_inv}")
    print(f"  q·q⁻¹  = {identidad}   → debe ser (1 + 0i + 0j + 0k)")


    print("\n= TEST 7 — Desempaquetado =")
    q = Quaternion(1, 2, 3, 4)
    a, b, c, d = q
    print(f"  a={a}, b={b}, c={c}, d={d}")


    print("\nTodos los tests completados.")