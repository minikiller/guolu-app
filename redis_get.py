import redis
import time
"""try to test redis sub/pub
"""
conn=None


def sub_msg(link=None):
    if link is None:
        link=[]
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    global conn
    conn=link
    with r:
        # r.set('foo', 'bar')
        p = r.pubsub(ignore_subscribe_messages=True)
        with p:
            p.subscribe('sunlf')
            while True:
                getmsg = p.get_message()
                if getmsg:
                    print(getmsg['data'])
                    print("current conn id is {}".format(id(link)))
                    link.sendall(getmsg['data'])
                if link._closed:
                    break
                time.sleep(0.001)
def change_conn(link):
    global conn
    conn=link