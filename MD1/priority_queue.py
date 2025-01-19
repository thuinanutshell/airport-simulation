import heapq
import scipy.stats as sts

class Event:
    def __init__(self, timestamp, function, *args, **kwargs):
        self.timestamp = timestamp
        self.function = function
        self.args = args
        self.kwargs = kwargs
    
    def __lt__(self, other):
        return self.timestamp < other.timestamp
    
    def run(self, schedule):
        self.function(schedule, *self.args, **self.kwargs)

class Schedule:
    def __init__(self, ):
        self.now = 0
        self.priority_queue = []
    
    def add_event_at(self, timestamp, function, *args, **kwargs):
        heapq.heappush(self.priority_queue, Event(timestamp, function, *args, **kwargs))
    
    def add_event_after(self, interval, function, *args, **kwargs):
        self.add_event_at(self.now + interval, function, *args, **kwargs)
    
    def next_event_time(self):
        return self.priority_queue[0].timestamp
    
    def run_next_event(self):
        event = heapq.heappop(self.priority_queue)
        self.now = event.timestamp
        event.run(self)
    
    def __repr__(self):
        return (
            f'Schedule() at time {self.now} ' +
            f'with {len(self.priority_queue)} events in the queue')
    
    def print_events(self):
        print(repr(self))
        for event in sorted(self.priority_queue):
            print(f'   {event.timestamp}: {event.function.__name__}')
        

class Queue:
    def __init__(self, service_rate):
        # Deterministic service time for an M/D/1 queue
        self.service_time = 1/service_rate
        self.people_in_queue = 0
        self.people_being_served = 0

    def add_person(self, schedule):
        # Add a person to the queue
        self.people_in_queue += 1
        if self.people_being_served < 1:
            # This person can be served immediately
            schedule.add_event_after(0, self.start_serving_person)
            
    def start_serving_person(self, schedule):
        # Move a person from the queue to a server
        self.people_in_queue -= 1
        self.people_being_served += 1
        # Schedule when the server will be done with the person
        schedule.add_event_after(
            self.service_time,
            self.finish_serving_person)
            
    def finish_serving_person(self, schedule):
        # Remove the person from the server
        self.people_being_served -= 1
        if self.people_in_queue > 0:
            # There are more people in the queue so serve the next person
            schedule.add_event_after(0, self.start_serving_person)
    
    
class Airport:
    def __init__(self, arrival_rate, service_rate):
        self.queue = Queue(service_rate)
        self.arrival_distribution = sts.expon(scale = 1/arrival_rate)

    def add_person(self, schedule):
        # Add a person to a queue when they arrive at the airport
        self.queue.add_person(schedule)
        # Schedule when to add another person
        schedule.add_event_after(
            self.arrival_distribution.rvs(),
            self.add_person)

    def run(self, schedule):
        # Schedule when the first person arrives
        schedule.add_event_after(
            self.arrival_distribution.rvs(),
            self.add_person)
    
def run_simulation(arrival_rate, service_rate, run_until):
    '''
    your docstring
    '''
    schedule = Schedule()
    airport = Airport(arrival_rate, service_rate)
    airport.run(schedule)
    while schedule.next_event_time() < run_until:
        schedule.run_next_event()
    return airport