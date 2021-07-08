# TruthTable
From a given string, creates a truth table

# Dependencies
To install dependencies: 
```
pip install -e .
```
# How to use
```
python3 truth_table.py <FORMULA>
```
ex:
```
python3 truth_table.py "(p->(q^~p))->((p->~q)^(p->q))"
```
Will have the following output:
```
p      q      ((p -> (q ^ ~p)) -> ((p -> ~q) ^ (p -> q)))
-----  -----  ---------------------------------------------
False  False  True
False  True   True
True   False  True
True   True   True
```
