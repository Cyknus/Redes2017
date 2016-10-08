
# Format responses
def build_response(func):
    def format_response(*args):
        status, string_message = func(*args)
        return {"status": status, "message": string_message}
    return format_response
# Format querys
def decode_message(func):
    def format_message(self, message, **kwargs):
        # message_split = split_message_header(message)
        # kwgargs[NAME_CONTACT] =  message_split[MESSAGE_USERNAME]
        # kwargs[IP_CONTACT] = message_split[MESSAGE_IP]
        # kwargs[PORT_CONTACT] = message_split[MESSAGE_PORT]
        # kwargs[MSG_CONTACT] = message_split[MESSAGE_TEXT]
        return func(self, 1, 2, 3, 4)
    return format_message

def parse_params(func):
    def lel(self, a=None):
        a = a if a else 100
        return func(self, a, 2)
    return lel

@decode_message
@build_response
def send_message_wrapper(self, username, contact_ip, contact_port, message):
    print(username)
    print(contact_ip)
    print(contact_port)
    print(message)
    return 2, "OK"


class Test(object):
    """docstring for Test"""
    @parse_params
    def __init__(self, arg1, arg2):
        super(Test, self).__init__()
        print(arg1)
        print(arg2)
