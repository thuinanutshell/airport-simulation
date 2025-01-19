**Model Setup**

M/D/1: markov chain, deterministic, c=1.

- The events are independent - Events here mean the arrival of the traveler
- Service rate is fixed (not following a distribution): 30 seconds per traveler
- Each queue corresponds to only one server.

**Pseudocode**

1. The queue is empty (length = 0)
2. The time starts at 0
3. Waiting time is initiated as 0
4. Final time is 1440 seconds (24th hour of the day)
5. Sample from the exponential distribution to get the time gap between 0 and the arrival of the first traveler: t0
   a. Add the traveler (event) to the queue
   b. Departure time is equal to the time the traveler arrives (t0) + 30 seconds (service rate): d0
   c. Update queue length: length += 1
6. Continue to sample from the expon. dist. to get the time gap between traveler 1 and traveler 2: t1 = t0 + time gap
   a. Add the customer to the queue
   b. If the first traveler is still being served, the second traveler has to wait until the first traveler departs
   c. If t1 > d0, remove the traveler from the queue (the logic basically means if the arrival time of the second traveler is greater than the departure time of the first traveler, that means the previous traveler has already done screening and departed)
   d. If t1 < d0, add the second traveler to the queue (the same applies here -> if the departure time of the first traveler is greater than the second traveler, this means the second traveler has to wait until the previous traveler is done screening).
   e. Update queue length: length += 1
7. Keep track of the waiting time for each customer by subtracting the departure time of the previous customer by the time they are actually screened: w0 = 0 (because they do have to wait), w1 = d0 - t1
8. Compute the actual departure time by adding the arrival time + waiting time + service time
9. Continue until the time reaches 1440th second (the end of the day)
10. Return the queue length at the end of the day
