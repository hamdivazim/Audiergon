# Minimising Lambda Costs

This is a sort of linear programming problem, but it's in practice :)

## The problem

I was testing the performance of the Lambda function, and it was pretty slow with the initial 512 MB memory. With AWS Lambda, CPU performance is allocated proportionally to memory.
* This was the exact performance output I got with 512 MB memory:
```
Total Round Trip Time: 29.42 seconds
```
Yeah, pretty long.

## Optimising

Lambda is charged based on usage of Gigabyte-seconds. I.e., based on how long its executions are and how much memory is allocated. So with 512 MB, the function used 14.71 GBs. So... I tried 1024 MB!
```
Total Round Trip Time: 14.48 seconds
```
So we actually minimised our cost to 14.48 GBs. That's a pretty small improvement, but in return you wait twice as less to get a result!