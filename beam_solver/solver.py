import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from beam_solver import beam_exceptions
from beam_solver.definitions import *

x, C1, C2, C3, C4, E, I = sp.symbols('x, C1, C2, C3, C4, E, I')


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

    def eval(self, x_value, sym=False):
        if self.exp < 0 or x_value < self.pos or self.is_contour:
            return 0
        else:
            if not sym:
                return self.magnitude * (x_value - self.pos) ** self.exp
            else:
                return self.magnitude * (x - self.pos) ** self.exp
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
    def __init__(self, E, length, I=0, height=0, base=0):
        ## Attributes
        """

        :rtype:
        """
        self.__E = 0
        self.__I = 0
        self.__length = 0
        self.__height = 0
        self.base = base
        # self.__nl = 0

        if height == 0:
            self.height = length / 5
        else:
            self.height = height

        if I == 0:
            self.inertia_moment = self.calculateInertia(base, height)
        else:
            self.inertia_moment = I

        # self.__nl = nl

        self.young_modulus = E
        # self.neutral_line = nl
        self.length = length

        self.__max_values = dict()

        self.loads = []

        self.__supports = []
        self.__hinges = []

        self.boundary = [free_support, free_support]

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

    @staticmethod
    def calculateInertia(base, height):
        return (1.0 / 12.0 * base * height ** 3)

    @property
    def young_modulus(self):
        return self.__E

    @young_modulus.setter
    def young_modulus(self, E):
        if not E > 0:
            raise beam_exceptions.InvalidInput("Young Module should be greater than zero")

        self.calculated_beam = False

        self.__E = E

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, l):
        if not l > 0:
            raise beam_exceptions.InvalidInput("beam_length should be greater than zero")

        self.calculated_beam = False

        self.__length = l

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, h):
        if not h > 0:
            raise beam_exceptions.InvalidInput("Beam Height should be greater than zero")
        self.calculated_beam = False

        self.__height = h

    #
    # @property
    # def neutral_line(self):
    #     return self.__nl
    #
    # @neutral_line.setter
    # def neutral_line(self, nl):
    #     if abs(nl) >= self.height / 2: raise beam_exceptions.InvalidInput("Invalid Neutral line")
    #     self.calculated_beam = False
    #
    #     self.__nl = nl

    @property
    def inertia_moment(self):
        return self.__I

    @inertia_moment.setter
    def inertia_moment(self, I):
        if not I > 0:
            raise beam_exceptions.InvalidInput("inertia_moement should be greater than zero")
        self.calculated_beam = False

        self.__I = I

    @property
    def supports(self):
        return self.__supports

    @supports.setter
    def supports(self, support_list=[]):

        if not support_list:
            self.__supports = []

            return

        if not min(support_list) >= 0:
            raise beam_exceptions.OutOfBounds("Support must be greater than zero")
        if not max(support_list) <= self.length:
            raise beam_exceptions.OutOfBounds(
                "Support must be lower than beam length")

        if (self.boundary[0] is simply_support and 0 in support_list):
            raise beam_exceptions.SuperImposedSupports
        if self.boundary[1] is simply_support and self.length in support_list:
            raise beam_exceptions.SuperImposedSupports
        if (self.boundary[0] is fixed_support and 0 in support_list):
            raise beam_exceptions.SuperImposedSupports
        if (self.boundary[1] is fixed_support and self.length in support_list):
            raise beam_exceptions.SuperImposedSupports

        self.__supports = list(set(support_list))

    @property
    def hinges(self):
        return self.__hinges

    @hinges.setter
    def hinges(self, hinge_list=[]):

        if not hinge_list:
            self.__hinges = []

            return

        if not min(hinge_list) >= 0: raise beam_exceptions.OutOfBounds("Hinge must be greater than zero")
        if not max(hinge_list) <= self.length: raise beam_exceptions.OutOfBounds("Hinge must be lower than beam length")

        if (self.boundary[0] is simply_support and 0 in hinge_list):  raise beam_exceptions.SuperImposedSupports
        if (self.boundary[
                1] is simply_support and self.length in hinge_list):  raise beam_exceptions.SuperImposedSupports
        if (self.boundary[0] is fixed_support and 0 in hinge_list):  raise beam_exceptions.SuperImposedSupports
        if (self.boundary[
                1] is fixed_support and self.length in hinge_list):  raise beam_exceptions.SuperImposedSupports

        self.__hinges = list(set(hinge_list))
        pass

    def setBoundary(self, left_support_type: str, right_support_type: str) -> None:
        """
        Set left and right boundary to Beam. Input: free, simply, fixed

        :param left_support_type: string
        :param right_support_type: string
        :return: none
        """

        support_list = self.supports

        if not isinstance(left_support_type, SupportObject): raise beam_exceptions.InvalidInput("Invalid left support")
        if not isinstance(right_support_type, SupportObject): raise beam_exceptions.InvalidInput(
            "Invalid right support")

        #
        # if (self.boundary[0] is simply_support and 0 in support_list):  raise beam_exceptions.SuperImposedSupports
        # if (self.boundary[1] is simply_support and self.beam_length in support_list):  raise beam_exceptions.SuperImposedSupports
        # if (self.boundary[0] is fixed_support and 0 in support_list):  raise beam_exceptions.SuperImposedSupports
        # if (self.boundary[1] is fixed_support and self.beam_length in support_list):  raise beam_exceptions.SuperImposedSupports
        #


        if (self.boundary[0] is simply_support and 0 in support_list):  support_list.remove(0)
        if (self.boundary[
                1] is simply_support and self.length in support_list):  support_list.remove(0)
        if (self.boundary[0] is fixed_support and 0 in support_list):  support_list.remove(0)
        if (self.boundary[
                1] is fixed_support and self.length in support_list):  support_list.remove(0)

        self.supports = support_list
        self.boundary = [left_support_type, right_support_type]

    def applyMoment(self, magnitude, distance):
        """

        :param magnitude:
        :param distance:
        :return:
        """
        if not distance >= 0: raise beam_exceptions.OutOfBounds("Load out of boundaries")
        if not distance <= self.length: raise beam_exceptions.OutOfBounds("Load out of boundaries")

        self.loads.append(["moment", magnitude, distance])

    def applyPointLoad(self, magnitude, distance):
        if not distance >= 0: raise beam_exceptions.OutOfBounds("Load out of boundaries")
        if not distance <= self.length: raise beam_exceptions.OutOfBounds("Load out of boundaries")

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
        if not distance_2 > distance_1: raise beam_exceptions.InvalidInput(
            "End load position must be > than star load position")
        if not distance_2 <= self.length: raise beam_exceptions.OutOfBounds("Load out of boundaries")
        if not magnitude_1 * magnitude_2 >= 0: raise beam_exceptions.InvalidInput("Both magnitudes must have same sign")
        if not abs(magnitude_1) + abs(magnitude_2) > 0: raise beam_exceptions.InvalidInput(
            "At least one magnitude must be greater than zero")

        self.loads.append(["dist_load", magnitude_1, distance_1, magnitude_2, distance_2])

    def resetLoads(self):
        self.loads = []

    def __addBracket(self, magnitude, distance, exponent):
        assert type(exponent) is int, "Exponent should be an integer"

        is_contour = False

        self.calculated_beam = False

        if distance == self.length or (distance == 0 and exponent < 0):
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

        len_supports = len(self.supports)
        len_hinges = len(self.hinges)
        reaction_array = sp.symbols("R1:%d" % (len_supports + 1))  # TODO: expand this
        eitheta_array = sp.symbols("EITHETA1:%d" % (len_hinges + 1))  # TODO: expand this

        for index in range(len_supports):
            self.__addPointLoad(reaction_array[index], self.supports[index])

        for index in range(len_hinges):
            self.__addHingeLoad(eitheta_array[index], self.hinges[index])

    def __addMoment(self, magnitude, distance):
        n = -2
        self.__addBracket(magnitude, distance, n)

    def __addPointLoad(self, magnitude, distance):
        n = -1
        self.__addBracket(magnitude, distance, n)

    def __addHingeLoad(self, magnitude, distance):
        n = -3
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

            if distance_2 < self.length:
                self.__addBracket(-w, distance_2, n)

            return

            # self.load_brackets.append(MacaulayBracket(magnitude, distance, -1))

        if abs(magnitude_2) > abs(magnitude_1):
            n = 1
            w = (magnitude_2 - magnitude_1) / (distance_2 - distance_1)
            self.__addBracket(w, distance_1, n)
            # self.load_brackets.append(MacaulayBracket(magnitude, distance, -1))

            if distance_2 < self.length:
                self.__addBracket(-w, distance_2, n)
                self.__addBracket(-(magnitude_2 - magnitude_1), distance_2, 0)

            if magnitude_1 != 0:
                self.__addBracket(magnitude_1, distance_1, 0)

                if distance_2 < self.length:
                    self.__addBracket(-magnitude_1, distance_2, 0)

            return

        else:
            n = 1
            w = (magnitude_1 - magnitude_2) / (distance_2 - distance_1)

            self.__addBracket((magnitude_1 - magnitude_2), distance_1, 0)
            self.__addBracket(-w, distance_1, n)

            if distance_2 < self.length:
                self.__addBracket(w, distance_2, n)
                # self.__addBracket(-(magnitude_2 - magnitude_1), distance_2, 0)

            if magnitude_2 != 0:
                self.__addBracket(magnitude_2, distance_1, 0)

                if distance_2 < self.length:
                    self.__addBracket(-magnitude_2, distance_2, 0)

            return

    @staticmethod
    def __evalBrackets(bracket_list, position, sym=False):
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

    def __findSections(self):
        """
        Find where the discontinuities are

        :return: set of discontinuities
        """

        section_pos = [0]
        for load in self.load_brackets:
            section_pos.append(load.pos)

        try:
            section_pos.remove(self.length)
        except ValueError:
            pass

        return sorted(set(section_pos))

    def __determineSectionsEquations(self):
        """

        Post-processing Method

        :return:
        """
        assert self.calculated_beam

        sections = self.__findSections()

        self.V_equations = []
        self.M_equations = []
        self.theta_equations = []
        self.disp_equations = []

        equations = (self.V_equations, self.M_equations, self.theta_equations, self.disp_equations)
        brackets = (self.V_brackets, self.M_brackets, self.theta_brackets, self.disp_brackets)

        for equation_list, bracket_list in zip(equations, brackets):
            for section in sections:
                equation_list.append(sp.expand(self.__evalBrackets(bracket_list, section, sym=True)))

    def __calculateValues(self):

        self.__beam_span = np.linspace(0, self.length, 500)

        self.__V_values = np.array([])
        self.__M_values = np.array([])
        self.__theta_values = np.array([])
        self.__disp_values = np.array([])

        for pos in self.__beam_span:
            self.__V_values = np.append(self.__V_values, np.float(self.__evalBrackets(self.V_brackets, pos)))
            self.__M_values = np.append(self.__M_values, np.float(self.__evalBrackets(self.M_brackets, pos)))
            self.__theta_values = np.append(self.__theta_values,
                                            np.float(self.__evalBrackets(self.theta_brackets, pos) / (
                                                self.young_modulus * self.inertia_moment)))
            self.__disp_values = np.append(self.__disp_values, np.float(self.__evalBrackets(self.disp_brackets, pos) / (
                self.young_modulus * self.inertia_moment)))

        self.__max_values['shear'] = max(self.__V_values, key=abs)
        self.__max_values['moment'] = max(self.__M_values, key=abs)
        self.__max_values['theta'] = max(self.__theta_values, key=abs)
        self.__max_values['displacement'] = max(self.__disp_values, key=abs)

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
                    momment_boundary[0] += load.magnitude

                elif load.pos == self.length:
                    momment_boundary[1] += load.magnitude

            if load.exp == -1:  # Moment loads
                if load.pos == 0:
                    conload_boundary[0] += load.magnitude

                elif load.pos == self.length:
                    conload_boundary[1] += load.magnitude

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
            self.V_boundary.append([self.length, -conload_boundary[1]])
            self.M_boundary.append([self.length, -momment_boundary[1]])

        elif boundary[1] is simply_support:
            self.disp_boundary.append([self.length, 0])
            self.M_boundary.append([self.length, -momment_boundary[1]])

        elif boundary[1] is fixed_support:
            self.disp_boundary.append([self.length, 0])
            self.theta_boundary.append([self.length, 0])

        ## Restrictions:

        for index in range(len(self.supports)):
            self.disp_boundary.append([self.supports[index], 0])

        for index in range(len(self.hinges)):
            self.M_boundary.append([self.hinges[index], 0])

    def diagramEquations(self):

        sections = self.__findSections()
        equations_string = ""

        for index in range(len(sections)):

            if index == len(sections) - 1:
                equations_string += ("%.2f < x < %.2f\n\n" % (sections[index], self.length))
            else:
                equations_string += ("%.2f < x < %.2f\n\n" % (sections[index], sections[index + 1]))


            V = self.V_equations[index].evalf(n= 3)
            M = self.M_equations[index].evalf(n= 3)
            theta = self.theta_equations[index].evalf(n= 3)
            v = self.disp_equations[index].evalf(n= 3)


            equations_string += ("V = %s \nM = %s\nEI*theta = %s\nEI*v = %s\n\n\n" % (V, M, theta, v))

        equations_string = equations_string.replace("**", "^")
        return equations_string



    def solve(self):

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
        variables = set()

        boundaries_tuple = (self.V_boundary, self.M_boundary, self.theta_boundary, self.disp_boundary)
        brackets_tuple = (self.V_brackets, self.M_brackets, self.theta_brackets, self.disp_brackets)

        for boundary_list, bracket_list in zip(boundaries_tuple, brackets_tuple):
            for boundary in boundary_list:
                equation = self.__evalBrackets(bracket_list, boundary[0]) - boundary[1]
                variables.update(equation.atoms(sp.Symbol), variables)

                equation_set.append(equation)

        if len(equation_set) != len(variables):
            raise beam_exceptions.ImpossibleToCalculate("Not enough supports")

        solutions = sp.solve(equation_set)
        for brackets in brackets_tuple:
            for bracket in brackets:
                try:
                    bracket.magnitude = bracket.magnitude.subs(solutions)
                except AttributeError:
                    pass

        self.__calculateValues()

        self.calculated_beam = True

        self.calculateStresses()

        self.__determineSectionsEquations()

    def evalPoint(self, plot, point):

        if plot == "shear":
            return self.__evalBrackets(self.V_brackets, point)
        elif plot == "moment":
            return self.__evalBrackets(self.M_brackets, point)
        elif plot == "theta":
            return self.__evalBrackets(self.theta_brackets, point) / (self.young_modulus * self.inertia_moment)
        elif plot == "displacement":
            return self.__evalBrackets(self.disp_brackets, point) / (self.young_modulus * self.inertia_moment)

    def evalMax(self, plot):
        return self.__max_values[plot]

    def calculateStresses(self):
        h_vector = np.linspace(-self.height / 2, self.height / 2, 200)
        M_value = self.__M_values

        MM, hh = np.meshgrid(M_value, h_vector)

        self.bending_stress = - MM * (hh) / (self.inertia_moment)

        V_value = self.__V_values

        VV, hh = np.meshgrid(V_value, h_vector)

        self.shear_stress = - VV * self.base / 2.0 * ((self.height ** 2) / 4 - hh ** 2) / (
            self.inertia_moment * self.base)

    def plotBendingStress(self, fig=None, ax=None):
        h_vector = np.linspace(-self.height / 2, self.height / 2, 200)

        if not self.calculated_beam: raise beam_exceptions.BeamNotCalculated(
            "Beam has not been calculated or has been modified")

        if not ax:
            figure_beam, ax_beam = plt.subplots()
        else:
            # plt.subplots_adjust(top=.98, bottom=.04, right=.95, left=.13, hspace=0.12)
            plt.figure(fig.number)
            ax_beam = ax
            figure_beam = fig

        n_levels = np.linspace(np.amin(self.bending_stress), np.amax(self.bending_stress), 100)

        im = ax_beam.contourf(self.__beam_span, h_vector, self.bending_stress, levels=n_levels)

        proxy = [plt.Rectangle((0, 0), 1, 1, fc=im.collections[-10].get_facecolor()[0]),
                 plt.Rectangle((0, 0), 1, 1, fc=im.collections[10].get_facecolor()[0])]

        ax_beam.legend(proxy, ["Maximum: %f" % np.amax(self.bending_stress),
                               "Minimum: %f" % np.amin(self.bending_stress)])

        # ax_beam.axis("equal")
        # ax_beam.autoscale(enable=False, axis='y', tight=False)


        if __name__ == "__main__":
            cb = figure_beam.colorbar(im, orientation="horizontal")

            ax_beam.set_ylabel("Beam height (m)")
            ax_beam.set_xlabel("Beam length (m)")
            ax_beam.set_title("Bending Stress")

            plt.show()

        return None

    def plotShearStress(self, fig=None, ax=None):
        h_vector = np.linspace(-self.height / 2, self.height / 2, 200)

        if not self.calculated_beam:
            raise beam_exceptions.BeamNotCalculated("Beam has not been calculated or has been modified")

        if not ax:
            figure_beam, ax_beam = plt.subplots()
        else:
            # plt.subplots_adjust(top=.98, bottom=.04, right=.95, left=.13, hspace=0.12)
            plt.figure(fig.number)
            ax_beam = ax
            figure_beam = fig

        n_levels = np.linspace(np.amin(self.shear_stress), np.amax(self.shear_stress), 100)

        im = ax_beam.contourf(self.__beam_span, h_vector, self.shear_stress, levels=n_levels)

        proxy = [plt.Rectangle((0, 0), 1, 1, fc=im.collections[-10].get_facecolor()[0]),
                 plt.Rectangle((0, 0), 1, 1, fc=im.collections[10].get_facecolor()[0])]

        ax_beam.legend(proxy, ["Maximum: %f" % np.amax(self.shear_stress),
                               "Minimum: %f" % np.amin(self.shear_stress)])

        # ax_beam.axis("equal")
        # ax_beam.autoscale(enable=True, axis='x', tight=True)


        if __name__ == "__main__":
            cb = figure_beam.colorbar(im, orientation="horizontal")

            ax_beam.set_ylabel("Beam height (m)")
            ax_beam.set_xlabel("Beam length (m)")
            ax_beam.set_title("Shear Stress")

            plt.show()

        return None

    def plotIsoChromatic(self, fig=None, ax=None):
        h_vector = np.linspace(-self.height / 2, self.height / 2, 200)

        radius = (((self.bending_stress / 2) ** 2) + self.shear_stress ** 2) ** (1 / 2)

        if not ax:
            figure_beam, ax_beam = plt.subplots()
        else:
            # plt.subplots_adjust(top=.98, bottom=.04, right=.95, left=.13, hspace=0.12)
            plt.figure(fig.number)
            ax_beam = ax
            figure_beam = fig

        n_levels = np.linspace(np.amin(radius), np.amax(radius), 100)

        im = ax_beam.contourf(self.__beam_span, h_vector, radius, levels=n_levels)

        proxy = [plt.Rectangle((0, 0), 1, 1, fc=im.collections[-10].get_facecolor()[0]),
                 plt.Rectangle((0, 0), 1, 1, fc=im.collections[10].get_facecolor()[0])]

        ax_beam.legend(proxy, ["Maximum: %f" % np.amax(radius),
                               "Minimum: %f" % np.amin(radius)])
        #
        # ax_beam.axis("equal")
        # ax_beam.autoscale(enable=True, axis='x', tight=True)


        if __name__ == "__main__":
            cb = figure_beam.colorbar(im, orientation="horizontal")

            ax_beam.set_ylabel("Beam height (m)")
            ax_beam.set_xlabel("Beam length (m)")
            ax_beam.set_title("Max Shear Stress")

            plt.show()

        return None

    def plotDiagrams(self, fig=None, ax=None):
        """
        Post-processing Method
        Evaluate the values of V, M, theta and v for the beam and plot.

        :return:
        """
        if not self.calculated_beam: raise beam_exceptions.BeamNotCalculated(
            "Beam has not been calculated or has been modified")

        if not ax:
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)
        else:
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

        if __name__ == "__main__":
            plt.show()

        return fig, (ax1, ax2, ax3, ax4)


if __name__ == "__main__":

    a = 3
    b = 1
    L = a + b
    I = 1234
    E = 200e9
    P = -10

    beam = Beam(E, L, I=I)
    beam.setBoundary(free_support, free_support)
    beam.supports = [0, 4]
    beam.applyPointLoad(P, a)
    beam.solve()

    beam.solve()
    print(beam.diagramEquations())
    # beam.plotBendingStress()
    # # beam.plotShearStress()
    # # beam.plotIsoChromatic()
    #
    # beam.plotDiagrams()
