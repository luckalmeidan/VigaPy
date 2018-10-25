from sympy import pretty_print as pp, latex
from sympy.abc import a, b, n

expr = (a*b)**n
pp(expr) # default
pp(expr, use_unicode=True)
print(latex(expr))
print(expr.evalf(subs=dict(a=2,b=4,n=5)))