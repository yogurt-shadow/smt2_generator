import sys
import json
import argparse
import os
import subprocess
import random

"""
Generate polynomial constraints with literals sharing the same maximum variables

e.g.
c1:  p1(x) \/ p2(x)
c2:  p3(x, y) \/ p4(x, y)
"""

var_name_dict = {}

def number2str(num):
    if num < 0:
        return '( - ' + str(-num) + ')'
    else:
        return str(num)

def power2str(var, power):
    "(* v1 v1 v1)"
    assert power >= 1
    if power == 1:
        return var_name_dict[var]
    else:
        res = '(*'
        for i in range(power):
            res += ' ' + var_name_dict[var]
        res += ')'
        return res

def generate_random_sum(num, sum):
    """
    Generate a vector with `num` elements whose sum is `sum`
    """
    points = []
    for i in range(num - 1):
        curr = random.randint(0, sum)
        points.append(curr)
    points.sort()
    points.append(sum)
    res = []
    for i in range(len(points)):
        if i == 0:
            res.append(points[i])
        else:
            res.append(points[i] - points[i - 1])
    return res

class monomial_generator:
    """
    (* 12 x1 x2 x3)
    """
    def __init__(self, coeff_lower, coeff_upper):
        self.coeff_lower = coeff_lower
        self.coeff_upper = coeff_upper

    def generate_monomial(self, degree, var_set):
        coeff = random.randint(self.coeff_lower, self.coeff_upper)
        res = '(* ' + number2str(coeff)
        degree_vec = generate_random_sum(len(var_set), degree)
        for i in range(len(var_set)):
            if degree_vec[i] == 0:
                continue
            res += ' ' + power2str(var_set[i], degree_vec[i])
        res += ')'
        return res


class polynomial_generator:
    """
    (+ m1 m2 coeff)
    """
    def __init__(self, coeff_lower, coeff_upper, monomial_lower, monomial_upper, mono_generator, degree_lower, degree_upper):
        self.coeff_lower = coeff_lower
        self.coeff_upper = coeff_upper
        self.monomial_lower = monomial_lower
        self.monomial_upper = monomial_upper
        self.mono_generator = mono_generator
        self.degree_lower = degree_lower
        self.degree_upper = degree_upper

    def generate_polynomial(self, var_set):
        degree = random.randint(self.degree_lower, self.degree_upper)
        coeff = random.randint(self.coeff_lower, self.coeff_upper)
        monomial_num = random.randint(self.monomial_lower, self.monomial_upper)
        res = '(+'
        assert monomial_num >= 1
        first_monomial = self.mono_generator.generate_monomial(degree, var_set)
        res += ' ' + first_monomial
        for i in range(1, monomial_num):
            curr_degree = random.randint(1, degree)
            res += ' ' + self.mono_generator.generate_monomial(curr_degree, var_set)
        res += ' ' + number2str(coeff) + ')'
        return res
       
class clause_generator:
    """
    (assert (or a1 a2 a3))
    """
    def __init__(self, literal_lower, literal_upper, poly_generator):
        self.literal_lower = literal_lower
        self.literal_upper = literal_upper
        self.poly_generator = poly_generator

    def generate_literal(self, var_set):
        res = '('
        choice = random.random()
        if choice < 0.45:
            res += '> '
        elif choice < 0.9:
            res += '< '
        else:
            res += '= '
        res += self.poly_generator.generate_polynomial(var_set)
        res += ' 0)'
        return res

    def generate_clause(self, var_set):
        literal_num = random.randint(self.literal_lower, self.literal_upper)
        res = '(assert (or'
        for i in range(literal_num):
            res += ' ' + self.generate_literal(var_set)
        res += '))'
        return res


class smt_generator:
    def __init__(self, cls_generator, clause_lower, clause_upper, var_lower, var_upper, clause_var_lower, clause_var_upper):
        self.cls_generator = cls_generator
        self.clause_lower = clause_lower
        self.clause_upper = clause_upper
        self.var_lower = var_lower
        self.var_upper = var_upper
        self.clause_var_lower = clause_var_lower
        self.clause_var_upper = clause_var_upper
        self.vars = []

    def generate_clauses(self):
        clause_num = random.randint(self.clause_lower, self.clause_upper)
        res = ''
        for i in range(clause_num):
            curr_var_num = random.randint(self.clause_var_lower, self.clause_var_upper)
            curr_var_set = random.sample(self.vars, curr_var_num)
            res += self.cls_generator.generate_clause(curr_var_set) + '\n'
        return res

    def generate_variables(self):
        res = ''
        for i in range(len(self.vars)):
            var_name = 'v' + str(i)
            var_name_dict[i] = var_name
            res += '(declare-const ' + var_name + ' Real)\n'
        return res

    def generate_smt2(self):
        self.vars = [i for i in range(random.randint(self.var_lower, self.var_upper))]
        var_name_dict.clear()
        res  = ''
        res += '(set-logic QF_NRA)\n\n'
        res += self.generate_variables() + '\n'
        res += self.generate_clauses() + '\n'
        res += "(check-sat)\n"
        res += "(exit)"
        return res

def load_config(config):
    mono_generator = monomial_generator(config['monomial']['coefficient_lower'], config['monomial']['coefficient_upper'])
    poly_generator = polynomial_generator(config['polynomial']['coefficient_lower'], config['polynomial']['coefficient_upper'], config['polynomial']['monomial_lower'], config['polynomial']['monomial_upper'], mono_generator, config['polynomial']['degree_lower'], config['polynomial']['degree_upper'])
    cls_generator = clause_generator(config['clause']['literal_lower'], config['clause']['literal_upper'], poly_generator)
    smt_gen = smt_generator(cls_generator, config['clause_lower'], config['clause_upper'], config['var_lower'], config['var_upper'], config['clause']['var_lower'], config['clause']['var_upper'])
    return smt_gen

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate polynomial constraints with literals sharing the same maximum variables')
    parser.add_argument('--config', type=str, default='config.json', help='path to the configuration file')
    parser.add_argument('--output', type=str, default='demo.smt2', help='path to the output file')
    args = parser.parse_args()
    # Load configuration
    with open(args.config) as f:
        config = json.load(f)
    # Generate SMT2
    smt_gen = load_config(config)
    smt2 = smt_gen.generate_smt2()
    # Write to file
    output = args.output
    if os.path.exists(output):
        os.remove(output)
    with open(output, 'w') as f:
        f.write(smt2)

