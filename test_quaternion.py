import unittest
import math

from quaternion import Quaternion, Vector


class TestQuaternion(unittest.TestCase):
    def test_empty(self):
        q = Quaternion()
        self.assertEqual(q.norm, 0.0)

    def test_scalar_quaternion(self):
        q = Quaternion(q1=2.0)
        self.assertEqual(q.norm, 2.0)

    def test_vector_quaternion(self):
        q = Quaternion(Vector(2.0, 3.0, 4.0))
        self.assertEqual(q.q1, 0.0)
        self.assertEqual(q.q2, 2.0)
        self.assertEqual(q.q3, 3.0)
        self.assertEqual(q.q4, 4.0)

    def test_addition_scalar_quaternion(self):
        q1 = Quaternion(1.0, 0.0, 0.0, 0.0)
        q2 = Quaternion(2.0, 0.0, 0.0, 0.0)
        q3 = q1 + q2
        self.assertEqual(Quaternion(3.0), q3)

    def test_norm(self):
        one = Quaternion(1.0, 0.0, 0.0, 0.0)
        i = Quaternion(0.0, 1.0, 0.0, 0.0)
        j = Quaternion(0.0, 0.0, 1.0, 0.0)
        k = Quaternion(0.0, 0.0, 0.0, 1.0)

        self.assertEqual(one.norm, 1.0)
        self.assertEqual(i.norm, 1.0)
        self.assertEqual(j.norm, 1.0)
        self.assertEqual(k.norm, 1.0)

        self.assertEqual(i * j, k)
        self.assertEqual(i * i, -one)
        self.assertEqual(i * k, -j)
        self.assertEqual(j * i, -k)
        self.assertEqual(j * j, -one)
        self.assertEqual(j * k, i)
        self.assertEqual(k * i, j)
        self.assertEqual(k * j, -i)
        self.assertEqual(k * k, -one)

    def test_multiply_quaternion(self):
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(2, 3, 4, 5)
        q3 = q1 * q2
        self.assertEqual(q3, Quaternion(-36, 6, 12, 12))

        r1 = Quaternion(4)
        r2 = Quaternion(8)
        self.assertEqual(r1 * r2, Quaternion(4 * 8))

    def test_conjugate(self):
        q = Quaternion(2, 3, 4, 5)
        self.assertEqual(q.conjugate, Quaternion(2, -3, -4, -5))

        self.assertEqual(Quaternion(q.norm2), q * q.conjugate)
        self.assertEqual(Quaternion(q.norm2), q.conjugate * q)

        p = Quaternion(4, 5, 6, 7)
        self.assertEqual(( p + q ).conjugate, p.conjugate + q.conjugate)

    def test_addition_quaternion(self):
        q1 = Quaternion(1.0, 2.0, 3.0, 4.0)
        q2 = Quaternion(2.0, 1.2, 0.5, 0.6)
        q3 = q1 + q2
        self.assertEqual(Quaternion(3.0, 3.2, 3.5, 4.6), q3)

    def test_multiplication_is_distributive_over_addition(self):
        p = Quaternion(5, 6, 7, 8)
        q = Quaternion(1, 2, 3, 4)
        r = Quaternion(3, 5, 6, 7)
        self.assertEqual(p * ( q + r ), p * q + p * r)

    def test_rotation_quaternion(self):

        q = Quaternion.Rotation(Vector(0., 1.0, 0.0), math.pi / 3.0)

        v1 = q.transform(Vector(0.0, 1.0, 0.0))

        self.assertEqual(Vector(0.0,1.0,0.0),v1)


    def test_vector_quaternion(self):
        # test with two perpendicular vector
        v1 = Quaternion(0.0, 0.0, 2.0, 0.0)
        v2 = Quaternion(0.0, 1.0, 0.0, 3.0)

        dot_product = (v1 * v2 ).q1
        self.assertEqual(dot_product, 0.0)
        cross_product = Vector((v1 * v2 ).q2, (v1 * v2 ).q3, (v1 * v2 ).q4)

        self.assertEqual(cross_product, Vector(6.0, 0.0, -2.0))

    def test_invert_quaternion(self):
        q = Quaternion(1, 2, 3, 4)

        self.assertEqual(~q, q.conjugate / q.norm2)

        q1 = Quaternion(0, 2, 0, 0)
        self.assertEqual(~q1, Quaternion(0.0, -0.5, 0.0, 0.0))

