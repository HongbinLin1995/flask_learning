from flask import Flask, request
import redis
from rq import Queue
import time

app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)

def background_task(n):
    
    delay = 2
    print('Task is running')
    print('Simulating {delay} second dealy')

    time.sleep(delay)
    print(len(n))
    print('Task complete')
    
    return len(n)

@app.route('/task')
@app.route('/task1')
def add_task():
    
    if request.args.get("n"):
        job = q.enqueue(background_task,request.args.get('n'))
        q_len = len(q)
        
        return f"Task {job.id} added to queue at {job.enqueued_at}. {q_len} tasks in the queue"
    
    return "No value for n :("


if __name__ == '__main__':
    app.run(debug=True)