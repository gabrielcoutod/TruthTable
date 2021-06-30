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
![Example](https://github.com/gabrielcoutod/TruthTable/blob/master/example.png)
