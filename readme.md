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
go stdlib | 1.5 | go | 563.08us | 61005.95 | 6.57MB
node stdlib | 4.2.1 | js | 735.02us | 13987.15 | 2.08MB
node cluster | 4.2.1 | js | 608.60us | 22926.30 | 3.41MB
luvit | 2.6.0 | lua | 1.09ms | 9654.11 | 1.27MB
tornado | 4.3 | python | 4.48ms | 2226.51 | 445.74KB
