# Script for Generating Polynomial Constraints (SMT QF_NRA)

## Run
```
python3 smt2_gen.py --config <config file> --output <output file>
```

`<config file>`: Configuration file in JSON format., default is `config.json`

`<output file>`: Output SMT-LIB 2.0 file, default is `output.smt2`


## Parameters

### Overall
| Parameter | Type | Description |
| :-:| :-: | :-: |
| `var_lower` | integer | Lower bound of the variable number |
| `var_upper` | integer | Upper bound of the variable number |
| `clause_lower` | integer | Lower bound of the number of clauses |
| `clause_upper` | integer | Upper bound of the number of clauses |

### Polynomial
| Parameter | Type | Description |
| :-:| :-: | :-: |
| `degree_lower`| integer | Lower bound of the degree of the polynomial |
| `degree_upper`| integer | Upper bound of the degree of the polynomial |
| `monomial_lower`| integer | Lower bound of the number of monomials in the polynomial |
| `monomial_upper`| integer | Upper bound of the number of monomials in the polynomial |
| `coefficient_lower`| integer | Lower bound of the value of the coefficients of the monomials |
| `coefficient_upper`| integer | Upper bound of the value of the coefficients of the monomials |

### Monomial
| Parameter | Type | Description |
| :-:| :-: | :-: |
| `coefficient_lower`| integer | Lower bound of the value of the coefficient of the monomial |
| `coefficient_upper`| integer | Upper bound of the value of the coefficient of the monomial |

### Clause
| Parameter | Type | Description |
| :-:| :-: | :-: |
| `var_lower`| integer | Lower bound of the number of variables in the clause |
| `var_upper`| integer | Upper bound of the number of variables in the clause |
| `literal_lower`| integer | Lower bound of the number of the literals in the clause |
| `literal_upper`| integer | Upper bound of the number of the literals in the clause |
