# Volatile Sets Dictionary
This project aims to extend python's native dictionary class, in order to add volatile sets.
Volatile sets are a combination of key and value that expires after a period of time. This time is decided by the user.
___
## Instalatiton
You can install it using pip with the following command.
```console
pip install volatile_dictionary
```
To install it by cloning its github repository, use the following commands. The "-e" flag install it in the path you clone it to, so, changes in the code will be instantly valid for the package users.
```console
git clone https://github.com/pedrogyrao/volatile_dictionary
cd volatile_dictionary
pip install -e .
```

___
## Using the VolatileDictionary Class
First import it in your project:
```python
from volatile_dictionary import VolatileDictionary
```
Then instantiate it:
```python
volatile_dict = VolatileDictionary()
```
___
VolatileDictionary works as a normal dictionary
```python
volatile_dict['key'] = 'value'
print(volatile_dict['key'])
```
saves internally the set "{'key', 'value'}" and outputs:
```python
value
```
This set added above is nonvolatile. To add a volatile the key must be a length 2 tuple and with the second element being the set's duration time in seconds.
```python
volatile_dict['volatile_key', 2] = 'volatile_value'
```
for the 2 seconds after the above line is ran,  this code
```python
print(volatile_dict['volatile_key'])
```
will output:
```python
volatile_value
```
after 2 seconds the set "{'volatile_key': 'volatile_value'}" will be deleted.
___
To manipulate this volatile sets three methods were created:

* is_set_volatile(key): returns "True" if the set is volatile and "False" if the set is nonvolatile.
* get_set_lifetime(key): returns the remaining lifetime of the specified key. If the key doesn't represent a volatile set, the method raises "NonvolatileTypeError".
* cancel_volatily(key): cancel the volatility of a volatile set. If the key doesn't represent a volatile set, the	method raises "NonvolatileTypeError".
___
In order to work with this differentiation between volatile and nonvolatile sets, the basic dict methods "keys", "values" and "items" were implemented too:

* volatile_keys and nonvolatile_keys;
* volatile_values and nonvolatile_values;
* volatile_items and nonvolatile_items.

