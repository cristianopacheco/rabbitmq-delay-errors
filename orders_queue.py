import json

from rabbitmq import RabbitMQ


class OrdersQueue(RabbitMQ):
    def __init__(self, queue='orders'):
        self.msg = {}
        super(OrdersQueue, self).__init__(queue)

    def simulate_error_processing(self):
        # demo for post queue error
        if not self.msg.get('error'):
            self.msg['error'] = True
            self.msg['retry'] += 1
            self.post_msg_queue_error_delay(self.msg, 10000) # 10 sec for qa, default 10 minutes
            print(" [x] Schedule job at queue error delay 10s")
        elif self.msg.get('retry') >= 5:
            # imp`lement: save on database
            # send alert of error???
            print(' [x] Finish: Maximum attempts reached')
        else:
            self.msg['retry'] += 1
            self.post_msg_queue_error_delay(self.msg, time_delay=60000) # 1m for qa, default 30 minutes
            print(" [x] Schedule job at queue error delay 1m")


    def callback(self, ch, method, properties, body):
        #load message as object
        self.msg = json.loads(body)
        print(" [*] Initializing job processing...")
        print(" [x] Received job: %r" % body)

        #
        # ... implement block code here
        # check on database status of job in begining end ending before run and save #fix duplicate, re-run only when msg.get('force') is true
        #

        #simulate error delay
        if self.msg.get('job_id') >= 7000000:
            error = self.simulate_error_processing()

        # release job from queue
        ch.basic_ack(delivery_tag = method.delivery_tag)
        print(" [x] Done")

