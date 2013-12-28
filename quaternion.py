import math


class Vector:
    """

    """

    def __init__(self, i, j=0, k=0):
        """

        """
        if isinstance(i, Vector):
            self.v = i.v[:]
        else:
            assert isinstance(i, float)
            assert isinstance(j, float)
            assert isinstance(k, float)
            self.v = [0.0] * 3
            self.v[0] = i
            self.v[1] = j
            self.v[2] = k

    @property
    def norm2(self):
        return self.v[0] ** 2.0 + self.v[1] ** 2.0 + self.v[2] ** 2.0

    @property
    def norm(self):
        return math.sqrt(self.norm2)

    def __getitem__(self, item):
        return self.v[item]

    def __eq__(self, other):
        return self[0] == other[0] and self[1] == other[1] and self[2] == other[2]

    def __str__(self):
        return " i * %lf + j * %lf  + k * %lf " % (self[0], self[1], self[2])

    def __repr__(self):
        return self.__str__()


class Quaternion:
    """
        A quaternion is defined as a sum of four terms:

            Q = 1.q1 + i.q2 + j.q3 + k.q4

        where q1,q2,q3,q4 are real.

        and i,j,k are symbolic elements having the following properties:

            i*i = -1  , j*j = -1 , k*k = -1
            i*j =  k  , j*k =  i , k*i =  j
            j*i = -k  , k*j = -i , i*k = -j
    """

    def __init__(self, q1=0, q2=0, q3=0, q4=0):

        if isinstance(q1, Vector):
            self.q1 = 0.0
            v = q1
            self.q2 = v[0]
            self.q3 = v[1]
            self.q4 = v[2]
        else:
            self.q1 = q1
            self.q2 = q2
            self.q3 = q3
            self.q4 = q4

    @property
    def norm2(self):
        return self.q1 ** 2.0 + self.q2 ** 2.0 + self.q3 ** 2.0 + self.q4 ** 2.0

    def __getitem__(self, item):
        if item == 0:
            return self.q1
        elif item == 1:
            return self.q2
        elif item == 2:
            return self.q3
        elif item == 3:
            return self.q4
        raise Exception("QuaternionException")

    @property
    def norm(self):
        return math.sqrt(self.norm2)

    @staticmethod
    def Rotation(v, angle):

        n = Vector(v).norm
        i = v[0] / n
        j = v[1] / n
        k = v[2] / n

        sin_ha = math.sin(angle / 2.0)
        cos_ha = math.cos(angle / 2.0)
        return Quaternion(q1=cos_ha, q2=i * sin_ha, q3=j * sin_ha, q4=k * sin_ha)

    def __eq__(self, other):
        return self[0] == other[0] and (self[1] == other[1]) and self[2] == other[2]

    def __add__(self, other):
        return Quaternion(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])

    def __mul__(self, other):
        if type(other) is float:
            return Quaternion(self.q1 * other, self.q2 * other, self.q3 * other, self.q3 * other)
        elif isinstance(other, Quaternion):
            # P = 1.p1 + i.p2 + j.p3 + k.p4
            # Q = 1.q1 + i.q2 + j.q3 + k.q4
            # P.Q = (1.p1 + i.p2 + j.p3 + k.p4)(1.q1 + i.q2 + j.q3 + k.q4)
            #     = 1.p1*(1.q1 + i.q2 + j.q3 + k.q4)+
            #       i.p2*(1.q1 + i.q2 + j.q3 + k.q4)+
            #       j.p3*(1.q1 + i.q2 + j.q3 + k.q4)+
            #       k.p4*(1.q1 + i.q2 + j.q3 + k.q4)
            #
            #     =   p1.q1  + i.p1.q2 + j.p1.q3 + k.p1.q4
            #     +  -p2.q2  + i.p2.q1 - j.p2.q4 + k.p2.q3
            #     +  -p3.q3  + i.p3.q4 + j.p3.q1 - k.p3.q2
            #     +  -p4.q4  - i.p4.q3 + j.p4.q2 + k.p4.q1
            #
            #     = 1.(p1.q1 - p2.q2 -p3.q3 -p4.q4) +
            #       i.(p1.q2 + p2.q1 +p3.q4 -p4.q3) +
            #       j.(p1.q3 + p3.q1 +p4.q2 -p2.q4) +
            #       k.(p1.q4 + p4.q1 +p2.q3 -p3.q2)
            p1 = self.q1
            p2 = self.q2
            p3 = self.q3
            p4 = self.q4
            q1 = other.q1
            q2 = other.q2
            q3 = other.q3
            q4 = other.q4

            r1 = (p1 * q1 - p2 * q2 - p3 * q3 - p4 * q4)
            ri = (p1 * q2 + p2 * q1 + p3 * q4 - p4 * q3)
            rj = (p1 * q3 + p3 * q1 + p4 * q2 - p2 * q4)
            rk = (p1 * q4 + p4 * q1 + p2 * q3 - p3 * q2)
            return Quaternion(r1, ri, rj, rk)
        else:
            raise Exception("Not implemented")


    def __neg__(self):
        return Quaternion(-self.q1, -self.q2, -self.q3, -self.q4)


    def __div__(self, other):
        if type(other) is float:
            return Quaternion(self.q1 / other, self.q2 / other, self.q3 / other, self.q3 / other)
        raise Exception("Not implemented")

    def __invert__(self):
        return self.conjugate / self.norm2

    def transform(self, coord):

        assert self.norm2 - 1.0 < 1E-9

        S = coord if isinstance(coord, Quaternion) else Quaternion(coord)
        q = self * S * ~self
        return q if isinstance(coord,Quaternion) else Vector(q.q2, q.q3, q.q4) \

    def __str__(self):
        return "1 * %lf + i * %lf + j * %lf  + k * %lf " % (self.q1, self.q2, self.q3, self.q4)

    def __repr__(self):
        return self.__str__()

    @property
    def conjugate(self):
        return Quaternion(self.q1, -self.q2, -self.q3, -self.q4)
