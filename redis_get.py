import  redis 
import  time
"""redis to test sub/pub
"""


def sub_msg(conn=None):
    if conn is None:
        conn=[]
    redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
    with redis_conn:
        pub = redis_conn.pubsub(ignore_subscribe_messages=True)
        with pub:
            pub.subscribe('guolu')
            while True:
                msg = pub.get_message()
                if msg:
                    print("get subscribe from is, value is {}".format(msg['data']))
                    conn.sendall(msg['data'])
                if conn._closed:
                    break
                time.sleep(0.01)
                
    