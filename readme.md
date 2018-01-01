http-bench
==========

A series of http benchmarks against popular languages and frameworks.
  
hardware specs
--------------
* 2.7GHz dual-core Intel Core i5 processor
* 16GB RAM

benchmarks
----------
Last run 2017-12-31T20:05:10.291782
  
  name | version | lang | avg latency | requests/sec | transfer/sec
------: | ------: | ------: | ------: | ------: | ------:
go fasthttp | 1 | go | 489.59us | 52,151 | 7.26MB
go stdlib | 1.9.2 | go | 1.58ms | 35,263 | 3.80MB
iron | 0.5.0 | rust | 820.44us | 31,341 | 3.38MB
node cluster | 9.3.0 | js | 4.49ms | 19,455 | 2.89MB
node stdlib | 9.3.0 | js | 838.68us | 14,076 | 2.09MB
dart stdlib | 1.24.3 | dart | 1.35ms | 8,954 | 1.74MB
luvit | 2.6.0 | lua | 1.27ms | 8,062 | 1.06MB
express | 4.13.3 | js | 1.47ms | 7,561 | 1.51MB
tornado | 4.5.2 | python | 5.07ms | 1,972 | 398.81KB
