import  redis 
import  time
"""监听redis的guolu主题，发送修改参数的变量名称和数值给socket连接
"""


def sub_msg(conn=None):
    """监听guolu topic，当接受到数据的时候，发送数据给socket连接
    
    Keyword Arguments:
        conn {[socket]} -- [socket 客户端连接] (default: {None})
    """
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
                
    