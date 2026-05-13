def gerar_f(n):
    """
    Gera a lista de valores da função f desde f(0) até f(n).

    >>> gerar_f(0)
    [0]
    >>> gerar_f(1)
    [0, 1]
    >>> gerar_f(5)
    [0, 1, 1, 3, 5, 11]
    """
    if not isinstance(n, int):
        raise TypeError("n deve ser um inteiro")
    if n < 0:
        raise ValueError("n deve ser não negativo")

    if n == 0:
        return [0]

    lista = [0, 1]

    for i in range(2, n + 1):
        lista.append(2 * lista[i-2] + lista[i-1])

    return lista


import unittest

class TestGerarF(unittest.TestCase):

    # Teste de número negativo
    def test_negativo(self):
        with self.assertRaises(ValueError):
            gerar_f(-1)

    # Caso base n = 0
    def test_n_zero(self):
        self.assertEqual(gerar_f(0), [0])

    # Caso base n = 1
    def test_n_um(self):
        self.assertEqual(gerar_f(1), [0, 1])

    # Teste da fórmula (caso geral)
    def test_n_cinco(self):
        self.assertEqual(gerar_f(5), [0, 1, 1, 3, 5, 11])


if __name__ == '__main__':
    unittest.main()