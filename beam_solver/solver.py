import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from beam_solver import beam_exceptions
from beam_solver.definitions import *

X, C1, C2, C3, C4, E, I = sp.symbols('X, C1, C2, C3, C4, E, I')


class MacaulayBracket:
    def __init__(self, magnitude, distance, exponent, is_contour=False):
        """

        :param distance: w*(x - a)^n
        :param exponent:
        """
        self.is_contour = is_contour

        self.magnitude = magnitude
        self.pos = distance
        self.exp = exponent

    def eval(self, x, sym=False):
        if self.exp < 0 or x < self.pos or self.is_contour:
            return 0
        else:
            if not sym:
                return self.magnitude * (x - self.pos) ** self.exp
            else:
                return self.magnitude * (X - self.pos) ** self.exp
                pass

    @property
    def integrated(self):
        """
        Return Macaulay Integrated

        :return: MacaulayBracket
        """
        if self.exp > 0:
            n = self.exp + 1
            a = self.pos
            w = self.magnitude / n

        else:
            n = self.exp + 1
            a = self.pos
            w = self.magnitude

        return MacaulayBracket(w, a, n, self.is_contour)

    def __str__(self):
        return None
        return "%f <x - %f>^%d" % (self.w, self.pos, self.n)


class Beam:


    def __init__(self, E, I, length):
        ## Attributes
        """

        :rtype:
        """
        self.__E = 0
        self.__I = 0
        self.__length = 0

        self.young_modulus = E
        self.inertia_moment = I
        self.beam_length = length

        self.__max_values = dict()

        self.loads = []

        self.load_brackets = []
        self.__supports = []
        self.pivots = []

        self.boundary = [0, 0]

        #### POST PROCESSING

        self.calculated_beam = False

        self.V_brackets = []
        self.M_brackets = []
        self.theta_brackets = []
        self.disp_brackets = []

        self.V_equations = []
        self.M_equations = []

        self.V_boundary = []
        self.M_boundary = []
        self.theta_boundary = []
        self.disp_boundary = []





    @property
    def young_modulus(self):
        return self.__E

    @young_modulus.setter
    def young_modulus(self, E):
        if not E > 0: raise  beam_exceptions.InvalidInput("Young Module should be greater than zero")
        self.calculated_beam = False

        self.__E = E

    @property
    def beam_length(self):
        return self.__length

    @beam_length.setter
    def beam_length(self, length):
        if not length > 0: raise  beam_exceptions.InvalidInput("beam_length should be greater than zero")
        self.calculated_beam = False

        self.__length = length

    @property
    def inertia_moment(self):
        return self.__I

    @inertia_moment.setter
    def inertia_moment(self, I):
        if not I > 0: raise beam_exceptions.InvalidInput("inertia_moement should be greater than zero")
        self.calculated_beam = False

        self.__I = I

    @property
    def beam_supports(self):
        return self.__supports

    @beam_supports.setter
    def beam_supports(self, support_list=[]):

        if not support_list:
            self.__supports =[]

            return

        if not min(support_list) >= 0: raise beam_exceptions.OutOfBounds("Support must be greater than zero")
        if not max(support_list) <= self.beam_length: raise beam_exceptions.OutOfBounds("Support must be lower than beam length")

        if (self.boundary[0] is simply_support and 0 in support_list):  raise beam_exceptions.SuperImposedSupports
        if (self.boundary[1] is simply_support and self.beam_length in support_list):  raise beam_exceptions.SuperImposedSupports
        if (self.boundary[0] is fixed_support and 0 in support_list):  raise beam_exceptions.SuperImposedSupports
        if (self.boundary[1] is fixed_support and self.beam_length in support_list):  raise beam_exceptions.SuperImposedSupports


        self.__supports = list(set(support_list))

    def setBoundary(self, left_support_type: str, right_support_type: str) -> None:
        """
        Set left and right boundary to Beam. Input: free, simply, fixed

        :param left_support_type: string
        :param right_support_type: string
        :return: none
        """

        support_list = self.beam_supports

        if not isinstance(left_support_type, SupportObject): raise beam_exceptions.InvalidInput("Invalid left support")
        if not isinstance(right_support_type, SupportObject): raise beam_exceptions.InvalidInput("Invalid right support")

        #
        # if (self.boundary[0] is simply_support and 0 in support_list):  raise beam_exceptions.SuperImposedSupports
        # if (self.boundary[1] is simply_support and self.beam_length in support_list):  raise beam_exceptions.SuperImposedSupports
        # if (self.boundary[0] is fixed_support and 0 in support_list):  raise beam_exceptions.SuperImposedSupports
        # if (self.boundary[1] is fixed_support and self.beam_length in support_list):  raise beam_exceptions.SuperImposedSupports
        #


        if (self.boundary[0] is simply_support and 0 in support_list):  support_list.remove(0)
        if (self.boundary[
                1] is simply_support and self.beam_length in support_list):  support_list.remove(0)
        if (self.boundary[0] is fixed_support and 0 in support_list):  support_list.remove(0)
        if (self.boundary[
                1] is fixed_support and self.beam_length in support_list):  support_list.remove(0)

        self.beam_supports = support_list
        self.boundary = [left_support_type, right_support_type]

    def resetLoads(self):
        self.loads = []

    def __addBracket(self, magnitude, distance, exponent):
        assert type(exponent) is int, "Exponent should be an integer"

        is_contour = False

        self.calculated_beam = False

        if distance == self.beam_length or (distance == 0 and exponent < 0):
            is_contour = True

        bracket = MacaulayBracket(magnitude, distance, exponent, is_contour)
        self.load_brackets.append(bracket)

    def __addLoadBrackets(self):
        self.load_brackets = []

        for load in self.loads:
            if load[0] == "moment":
                self.__addMoment(load[1], load[2])

            elif load[0] == "point_load":
                self.__addPointLoad(load[1], load[2])

            elif load[0] == "dist_load":
                self.__addDistLoad(load[1], load[2], load[3], load[4])

        reaction_array = sp.symbols("R1:10")
        for index in range(0, len(self.beam_supports)):
            self.__addPointLoad(reaction_array[index], self.beam_supports[index])

    def applyMoment(self, magnitude, distance):
        """
        
        :param magnitude: 
        :param distance: 
        :return: 
        """
        if not distance >= 0: raise beam_exceptions.OutOfBounds("Load out of boundaries")
        if not distance <= self.beam_length: raise beam_exceptions.OutOfBounds("Load out of boundaries")

        self.loads.append(["moment", magnitude, distance])

    def applyPointLoad(self, magnitude, distance):
        if not distance >= 0: raise beam_exceptions.OutOfBounds("Load out of boundaries")
        if not distance <= self.beam_length: raise beam_exceptions.OutOfBounds("Load out of boundaries")

        self.loads.append(["point_load", magnitude, distance])

    def applyDistLoad(self, magnitude_1, distance_1, magnitude_2, distance_2):
        """
        
        :param magnitude_1: 
        :param distance_1: 
        :param magnitude_2: 
        :param distance_2: 
        :return: 
        """

        if not distance_1 >= 0: raise beam_exceptions.OutOfBounds("Load out of boundaries")
        if not distance_2 > distance_1: raise beam_exceptions.InvalidInput("End load position must be > than star load position")
        if not distance_2 <= self.beam_length: raise beam_exceptions.OutOfBounds("Load out of boundaries")
        if not magnitude_1 * magnitude_2 >= 0: raise beam_exceptions.InvalidInput("Both magnitudes must have same sign")
        if not abs(magnitude_1) + abs(magnitude_2) > 0: raise beam_exceptions.InvalidInput("At least one magnitude must be greater than zero")

        self.loads.append(["dist_load", magnitude_1, distance_1, magnitude_2, distance_2])

    def __addMoment(self, magnitude, distance):
        n = -2
        self.__addBracket(magnitude, distance, n)

    def __addPointLoad(self, magnitude, distance):
        n = -1
        self.__addBracket(magnitude, distance, n)

    def __addDistLoad(self, magnitude_1, distance_1, magnitude_2, distance_2):
        """

        :param magnitude_1:
        :param distance_1:
        :param magnitude_2:
        :param distance_2:
        :return:
        """

        if magnitude_1 == magnitude_2:
            n = 0
            w = magnitude_1
            self.__addBracket(w, distance_1, n)

            if distance_2 < self.beam_length:
                self.__addBracket(-w, distance_2, n)

            return

            # self.load_brackets.append(MacaulayBracket(magnitude, distance, -1))

        if abs(magnitude_2) > abs(magnitude_1):
            n = 1
            w = (magnitude_2 - magnitude_1) / (distance_2 - distance_1)
            self.__addBracket(w, distance_1, n)
            # self.load_brackets.append(MacaulayBracket(magnitude, distance, -1))

            if distance_2 < self.beam_length:
                self.__addBracket(-w, distance_2, n)
                self.__addBracket(-(magnitude_2 - magnitude_1), distance_2, 0)

            if magnitude_1 != 0:
                self.__addBracket(magnitude_1, distance_1, 0)

                if distance_2 < self.beam_length:
                    self.__addBracket(-magnitude_1, distance_2, 0)

            return

        else:
            n = 1
            w = (magnitude_1 - magnitude_2) / (distance_2 - distance_1)

            self.__addBracket((magnitude_1 - magnitude_2), distance_1, 0)
            self.__addBracket(-w, distance_1, n)

            if distance_2 < self.beam_length:
                self.__addBracket(w, distance_2, n)
                # self.__addBracket(-(magnitude_2 - magnitude_1), distance_2, 0)

            if magnitude_2 != 0:
                self.__addBracket(magnitude_2, distance_1, 0)

                if distance_2 < self.beam_length:
                    self.__addBracket(-magnitude_2, distance_2, 0)

            return

    @staticmethod
    def evalBrackets(bracket_list, position, sym=False):
        """
        Find the sum of an input bracket_list and returns a value
        sym == true is for the case when the symbolic equation is evaluated for each section.

        :param bracket_list: list
        :param position: float
        :param sym: symbolic
        :return: expression
        """
        sum = 0

        for bracket in bracket_list:
            sum += bracket.eval(position, sym)

        return sum

    def findSections(self):
        """
        Find where the discontinuities are

        :return: set of discontinuities
        """

        section_pos = [0]
        for load in self.load_brackets:
            section_pos.append(load.pos)

        try:
            section_pos.remove(self.beam_length)
        except ValueError:
            pass

        return sorted(set(section_pos))

    def __determineSectionsEquations(self):
        """

        Post-processing Method

        :return:
        """
        assert self.calculated_beam

        sections = self.findSections()

        self.V_equations = []
        self.M_equations = []
        self.theta_equations = []
        self.disp_equations = []

        equations = (self.V_equations, self.M_equations, self.theta_equations, self.disp_equations)
        brackets = (self.V_brackets, self.M_brackets, self.theta_brackets, self.disp_brackets)

        for equation_list, bracket_list in zip(equations, brackets):
            for section in sections:
                equation_list.append(sp.expand(self.evalBrackets(bracket_list, section, sym=True)))

    def __calculateValues(self):

        self.__beam_span = np.linspace(0, self.beam_length, 500)

        self.__V_values = np.array([])
        self.__M_values = np.array([])
        self.__theta_values = np.array([])
        self.__disp_values = np.array([])

        for pos in self.__beam_span:
            self.__V_values = np.append(self.__V_values, np.float(self.evalBrackets(self.V_brackets, pos)))
            self.__M_values = np.append(self.__M_values, np.float(self.evalBrackets(self.M_brackets, pos)))
            self.__theta_values = np.append(self.__theta_values,
                                            np.float(self.evalBrackets(self.theta_brackets, pos) / (
                                                self.young_modulus * self.inertia_moment)))
            self.__disp_values = np.append(self.__disp_values, np.float(self.evalBrackets(self.disp_brackets, pos) / (
                self.young_modulus * self.inertia_moment)))

        self.__max_values['shear'] = max(self.__V_values, key=abs)
        self.__max_values['moment'] = max(self.__M_values, key=abs)
        self.__max_values['theta'] = max(self.__theta_values, key=abs)
        self.__max_values['displacement'] = max(self.__disp_values, key=abs)

    def plotEquations(self, fig, ax):
        """
        Post-processing Method
        Evaluate the values of V, M, theta and v for the beam and plot.

        :return:
        """
        if not self.calculated_beam: raise beam_exceptions.BeamNotCalculated("Beam has not been calculated or has been modified")

        # fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)
        # plt.subplots_adjust(top=.98, bottom=.04, right=.95, left=.13, hspace=0.12)
        plt.figure(fig.number)
        ax1 = ax[0]
        ax2 = ax[1]
        ax3 = ax[2]
        ax4 = ax[3]

        ax1.fill_between(self.__beam_span, 0, self.__V_values, hatch="//", facecolor="none")
        ax1.set_ylabel("V")
        # ax1.set_title("Esforço Cortante")
        ax1.grid()

        ax2.fill_between(self.__beam_span, 0, self.__M_values, hatch="//", facecolor="none")
        ax2.set_ylabel("M")
        # ax2.set_title("Momento Fletor")
        ax2.grid()

        ax3.fill_between(self.__beam_span, 0, self.__theta_values, hatch="//", facecolor="none")
        ax3.set_ylabel("Theta")
        # ax3.set_title("Angulo")
        ax3.grid()

        ax4.fill_between(self.__beam_span, 0, self.__disp_values, hatch="//", facecolor="none")
        ax4.set_xlabel("x")
        ax4.set_ylabel("v")
        # ax4.set_title("Deslocamento")
        ax4.grid()


        return fig, (ax1, ax2, ax3, ax4)

    def __defineConditions(self):
        """
        
        :return: 
        """

        conload_boundary = [0, 0]
        momment_boundary = [0, 0]

        self.V_boundary = []
        self.M_boundary = []
        self.theta_boundary = []
        self.disp_boundary = []

        boundary = self.boundary

        for load in self.load_brackets:
            if load.exp == -2:  # Moment loads
                if load.pos == 0:
                    momment_boundary[0] = load.magnitude

                elif load.pos == self.beam_length:
                    momment_boundary[1] = load.magnitude

            if load.exp == -1:  # Moment loads
                if load.pos == 0:
                    conload_boundary[0] = load.magnitude

                elif load.pos == self.beam_length:
                    conload_boundary[1] = load.magnitude

        if boundary[0] is free_support:
            self.V_boundary.append([0, conload_boundary[0]])
            self.M_boundary.append([0, momment_boundary[0]])

        elif boundary[0] is simply_support:
            self.M_boundary.append([0, momment_boundary[0]])
            self.disp_boundary.append([0, 0])

        elif boundary[0] is fixed_support:
            self.disp_boundary.append([0, 0])
            self.theta_boundary.append([0, 0])

            pass

        if boundary[1] == free_support:
            self.V_boundary.append([self.beam_length, -conload_boundary[1]])
            self.M_boundary.append([self.beam_length, -momment_boundary[1]])

        elif boundary[1] is simply_support:
            self.disp_boundary.append([self.beam_length, 0])
            self.M_boundary.append([self.beam_length, -momment_boundary[1]])

        elif boundary[1] is fixed_support:
            self.disp_boundary.append([self.beam_length, 0])
            self.theta_boundary.append([self.beam_length, 0])

        for index in range(len(self.beam_supports)):
            self.disp_boundary.append([self.beam_supports[index], 0])

    def printEquations(self):

        sections = self.findSections()

        for index in range(len(sections)):

            if index == len(sections) - 1:
                print("%.2f < X < %.2f" % (sections[index], self.beam_length))
                print
            else:
                print("%.2f < X < %.2f" % (sections[index], sections[index + 1]))

            print("V = %s" % self.V_equations[index])
            print("M = %s" % self.M_equations[index])
            print("teta = %s" % self.theta_equations[index])
            print("v = %s\n" % self.disp_equations[index])

    def evalPoint(self, plot, point):


        if plot == "shear":
            return self.evalBrackets(self.V_brackets, point)
        elif plot == "moment":
            return self.evalBrackets(self.M_brackets, point)
        elif plot == "theta":
            return self.evalBrackets(self.theta_brackets, point) / (self.young_modulus * self.inertia_moment)
        elif plot == "displacement":
            return self.evalBrackets(self.disp_brackets, point) / (self.young_modulus * self.inertia_moment)

    def evalMax(self, plot):
        return self.__max_values[plot]

    def calculate(self):

        self.V_brackets = []
        self.M_brackets = []
        self.theta_brackets = []
        self.disp_brackets = []

        self.__addLoadBrackets()
        self.__defineConditions()

        for item in self.load_brackets:
            self.V_brackets.append(item.integrated)

        self.V_brackets.append(MacaulayBracket(C1, 0, 0))

        for item in self.V_brackets:
            self.M_brackets.append(item.integrated)

        self.M_brackets.append(MacaulayBracket(C2, 0, 0))

        for item in self.M_brackets:
            self.theta_brackets.append(item.integrated)

        self.theta_brackets.append(MacaulayBracket(C3, 0, 0))

        for item in self.theta_brackets:
            self.disp_brackets.append(item.integrated)

        self.disp_brackets.append(MacaulayBracket(C4, 0, 0))

        equation_set = []

        boundaries = (self.V_boundary, self.M_boundary, self.theta_boundary, self.disp_boundary)
        brackets = (self.V_brackets, self.M_brackets, self.theta_brackets, self.disp_brackets)

        for boundary_list, bracket_list in zip(boundaries, brackets):
            for boundary in boundary_list:
                equation_set.append(self.evalBrackets(bracket_list, boundary[0]) - boundary[1])

        solutions = sp.solve(equation_set)
        for brackets in (self.V_brackets, self.M_brackets, self.theta_brackets, self.disp_brackets):
            for bracket in brackets:
                try:
                    bracket.magnitude = bracket.magnitude.subs(solutions)
                except AttributeError:
                    pass

        self.__calculateValues()

        self.calculated_beam = True

        self.__determineSectionsEquations()


if __name__ == "__main__":
    L = 4
    I = 1234
    E = 1

    L = 4
    I = 1234
    E = 200e9
    P = -10

    beam = Beam(E, I, L)
    beam.setBoundary(simply_support, simply_support)
    beam.applyPointLoad(-10, 2)
    beam.calculate()


    beam.calculate()
    beam.printEquations()

    beam.calculate()
    beam.printEquations()


    beam.printEquations()

    ## beam.plotEquations()

