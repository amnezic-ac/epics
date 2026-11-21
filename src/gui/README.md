### Note for developers and maintainers

Here are some guidelines for maintainers of the gui part of the code:
- use ttk over tk as much as possible
- for makeXFrame functions:
    - return the created frame
    - the function should take in argument a dictionary that will hold a lambda function which can be called to get the property object directly