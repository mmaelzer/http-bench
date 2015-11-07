http-bench
==========

A series of http benchmarks against popular languages and frameworks. Come back soon for a more complete project.  
  
hardware specs
--------------
* 2.7GHz dual-core Intel Core i5 processor
* 16GB RAM

benchmarks
----------
name | version | lang | avg latency | requests/sec | transfer/sec
------- | ------- | ------- | ------- | ------- | -------
go stdlib | 1.5 | go | 276.63us | 61530.5 | 6.63MB
node cluster | 4.2.1 | js | 702.15us | 28121.71 | 4.18MB
node stdlib | 4.2.1 | js | 553.71us | 18502.01 | 2.75MB
dart stdlib | 1.12.2 | dart | 726.57us | 17846.62 | 3.47MB
luvit | 2.6.0 | lua | 1.04ms | 9995.26 | 1.32MB
tornado | 4.3 | python | 4.62ms | 2191.54 | 438.74KB
