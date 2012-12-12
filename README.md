# etf  
etf is module for supporting encoding/decoding of the [Erlang External Term Format](http://erlang.org/doc/apps/erts/erl_ext_dist.html) in Python.

## About  
Even though there are already other libraries which support this functionality. See:
[erlport](https://github.com/hdima/erlport) and [python-erlastic](https://github.com/samuel/python-erlastic).
I am reimplementing in order to learn the intimate details of the spec and eventually plan on making it a streaming codec via coroutines.