import unittest

from beam_solver.solver import *


# noinspection PyShadowingNames
class MyTestCase(unittest.TestCase):

    def test_simply_middle_load(self):
        L = 4
        I = 1234
        E = 200e9
        P = -10

        beam = Beam(E, I, L)
        beam.setBoundary(simply_support, simply_support)
        beam.applyPointLoad(-10, 2)
        beam.calculate()

        v_max = P * L ** 3 / (48 * E * I)
        theta_max = P * L ** 2 / (16 * E * I)

        self.assertAlmostEqual(v_max, beam.evalMax("displacement"), delta=(abs(v_max) * 1e-3))
        self.assertAlmostEqual(theta_max, beam.evalPoint("theta", 0), delta=(abs(v_max) * 1e-3))

    def test_simply_load_manual_supports(self):
        a = 3
        b = 1
        L = a + b
        I = 1234
        E = 200e9
        P = -10

        beam = Beam(E, I, L)
        beam.setBoundary(free_support, free_support)
        beam.beam_supports = [0, 4]
        beam.applyPointLoad(P, a)
        beam.calculate()

        v_a = P * b * a * (L ** 2 - b ** 2 - a ** 2) / (6 * E * I * L)
        theta_1 = P * a * b * (L + b) / (6 * E * I * L)
        theta_2 = - P * a * b * (L + a) / (6 * E * I * L)

        self.assertAlmostEqual(v_a, beam.evalPoint("displacement", a), delta=(abs(v_a) * 1e-3))
        self.assertAlmostEqual(theta_1, beam.evalPoint("theta", 0), delta=(abs(theta_1) * 1e-3))
        self.assertAlmostEqual(theta_2, beam.evalPoint("theta", L), delta=(abs(theta_2) * 1e-3))

    def test_moment_in_support(self):
        L = 4
        I = 1234
        E = 200e9
        M = 10

        beam = Beam(E, I, L)
        beam.setBoundary(simply_support, simply_support)
        beam.applyMoment(M, 0)
        beam.calculate()

        theta_1 = - M * L / (3 * E * I)
        theta_2 = M * L / (6 * E * I)

        v_max = - M * L ** 2 / (243 ** (1 / 2) * E * I)

        self.assertAlmostEqual(v_max, beam.evalMax("displacement"), delta=(abs(v_max) * 1e-3))

        self.assertAlmostEqual(theta_1, beam.evalPoint("theta", 0), delta=(abs(theta_1) * 1e-3))
        self.assertAlmostEqual(theta_2, beam.evalPoint("theta", L), delta=(abs(theta_2) * 1e-3))

    def test_simply_dist_load_before_end(self):
        L = 4
        I = 1234
        E = 200e9
        w = -10
        beam = Beam(E, I, L)
        beam.setBoundary(simply_support, simply_support)
        beam.applyDistLoad(w, 0, w, 2)
        beam.calculate()

        theta_1 = 3 * w * L ** 3 / (128 * E * I)
        theta_2 = -7 * w * L ** 3 / (384 * E * I)

        v_max = 0.006563 * w * L ** 4 / (E * I)

        self.assertAlmostEqual(theta_1, beam.evalPoint("theta", 0), delta=(abs(theta_1) * 1e-3))
        self.assertAlmostEqual(theta_2, beam.evalPoint("theta", L), delta=(abs(theta_2) * 1e-3))

    def test_tri_load(self):
        L = 4
        I = 1234
        E = 200e9
        w = -10
        beam = Beam(E, I, L)
        beam.setBoundary(simply_support, simply_support)
        beam.applyDistLoad(0, 0, w, 4)
        beam.calculate()

        theta_1 = 7 * w * L ** 3 / (360 * E * I)
        theta_2 = - w * L ** 3 / (45 * E * I)

        self.assertAlmostEqual(theta_1, beam.evalPoint("theta", 0), delta=(abs(theta_1) * 1e-3))
        self.assertAlmostEqual(theta_2, beam.evalPoint("theta", L), delta=(abs(theta_2) * 1e-3))

    def test_cantilever_dist_load(self):
        L = 4
        I = 1234
        E = 200e9
        w = -10
        beam = Beam(E, I, L)
        beam.setBoundary(fixed_support, free_support)
        beam.applyDistLoad(w, 0, w, 4)
        beam.calculate()

        theta_max = w * L ** 3 / (6 * E * I)
        v_max = w * L ** 4 / (8 * E * I)

        self.assertAlmostEqual(theta_max, beam.evalMax("theta"), delta=(abs(theta_max) * 1e-3))
        self.assertAlmostEqual(v_max, beam.evalMax("displacement"), delta=(abs(v_max) * 1e-1))

    def test_cantilever_dist_load_before_end(self):
        L = 4
        I = 1234
        E = 200e9
        w = -10
        beam = Beam(E, I, L)
        beam.setBoundary(fixed_support, free_support)
        beam.applyDistLoad(w, 0, w, 2)
        beam.calculate()

        theta_max = w * L ** 3 / (48 * E * I)
        v_max = 7 * w * L ** 4 / (384 * E * I)

        self.assertAlmostEqual(theta_max, beam.evalMax("theta"), delta=(abs(theta_max) * 1e-3))
        self.assertAlmostEqual(v_max, beam.evalMax("displacement"), delta=(abs(v_max) * 1e-1))

    def test_cantilever_tri_load(self):
        L = 4
        I = 1234
        E = 200e9
        w = -10
        beam = Beam(E, I, L)
        beam.setBoundary(fixed_support, free_support)
        beam.applyDistLoad(w, 0, 0, 4)
        beam.calculate()

        theta_max = w * L ** 3 / (24 * E * I)
        v_max = w * L ** 4 / (30 * E * I)

        self.assertAlmostEqual(theta_max, beam.evalMax("theta"), delta=(abs(theta_max) * 1e-3))
        self.assertAlmostEqual(v_max, beam.evalMax("displacement"), delta=(abs(v_max) * 1e-1))

    def test_complex_case(self):
        L = 4
        I = 1234
        E = 1

        beam = Beam(E, I, L)

        beam.applyPointLoad(-30, 2.5)

        beam.applyDistLoad(-20, 0.5, -40, 2.1)
        beam.applyDistLoad(-20, 2.5, -10, 3.9)
        beam.applyDistLoad(20, 0.75, 20, 3.75)

        beam.beam_supports = [1, 2, 3]

        beam.applyMoment(-30, 1)
        beam.applyMoment(20, 2)
        beam.applyMoment(-40, 2.5)
        beam.applyMoment(-10, 3)
        beam.applyMoment(-5, 4)

        beam.setBoundary(fixed_support, simply_support)
        beam.calculate()

        # Values obtained by independent software
        theta_max = -4.6128995e-3
        disp_max = 1.07387e-3
        M_max = 30.8172
        V_max = 53.4156

        ## Points at 2
        V_point = -10.6740
        M_point = -13.5884
        disp_point = 0
        theta_point = -4.61295e-3

        self.assertAlmostEqual(theta_max, beam.evalMax("theta"), delta=(abs(theta_max) * 1e-2))
        self.assertAlmostEqual(disp_max, beam.evalMax("displacement"), delta=(abs(disp_max) * 1e-2))

        self.assertAlmostEqual(M_max, beam.evalMax("moment"), delta=(abs(M_max) * 1e-2))
        self.assertAlmostEqual(V_max, beam.evalMax("shear"), delta=(abs(V_max) * 1e-2))

    def test_cantilever_trap_load_dec_before_end(self):
        L = 4
        I = 1234
        E = 200e9
        beam = Beam(E, I, L)
        beam.setBoundary(fixed_support, free_support)
        beam.applyDistLoad(-20, 1, -10, 3)
        beam.calculate()

        M_max = -56.667
        V_max = 30

        self.assertAlmostEqual(M_max, beam.evalMax("moment"), delta=(abs(M_max) * 1e-3))
        self.assertAlmostEqual(V_max, beam.evalMax("shear"), delta=(abs(V_max) * 1e-1))

    def test_invalid_input(self):
        # Negative Young Modules
        with self.assertRaises(beam_exceptions.InvalidInput) as context:
            L = 4
            I = 1234
            E = -200e9
            beam = Beam(E, I, L)
            beam.setBoundary(fixed_support, free_support)
            beam.applyDistLoad(-20, 1, -10, 3)
            beam.calculate()

        # Negative Length
        with self.assertRaises(beam_exceptions.InvalidInput) as context:
            L = -4
            I = 1234
            E = 200e9
            beam = Beam(E, I, L)
            beam.setBoundary(fixed_support, free_support)
            beam.applyDistLoad(-20, 1, -10, 3)
            beam.calculate()

        # Out of boundaries dist load
        with self.assertRaises(beam_exceptions.OutOfBounds) as context:
            L = 4
            I = 1234
            E = 200e9
            beam = Beam(E, I, L)
            beam.setBoundary(fixed_support, free_support)
            beam.applyDistLoad(-20, 1, -10, 5)

        # Out of boundaries support
        with self.assertRaises(beam_exceptions.OutOfBounds) as context:
            L = 4
            I = 1234
            E = 200e9
            beam = Beam(E, I, L)
            beam.beam_supports = [6]

        # Out of boundaries support
        with self.assertRaises(beam_exceptions.OutOfBounds) as context:
            L = 4
            I = 1234
            E = 200e9
            beam = Beam(E, I, L)
            beam.beam_supports = [-2]

        # Super imposed supports, supports are defined before boundaries
        with self.assertRaises(beam_exceptions.SuperImposedSupports) as context:
            L = 4
            I = 1234
            E = 200e9
            beam = Beam(E, I, L)
            beam.beam_supports = [0]
            beam.setBoundary(simply_support, simply_support)

        # Super imposed supports, supports are defined after boundaries
        with self.assertRaises(beam_exceptions.SuperImposedSupports) as context:
            L = 4
            I = 1234
            E = 200e9
            beam = Beam(E, I, L)
            beam.setBoundary(fixed_support, simply_support)
            beam.beam_supports = [0]


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    unittest.TextTestRunner(verbosity=3).run(suite)
