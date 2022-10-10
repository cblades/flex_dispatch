"""Demonstration of flex-dispatch's extension mechanism.

You can dynamically add functionality to dispatchers with their extend method.  
Each function passed to extend will be called before the original dispatcher function and the first non-None value
returned will be used as the dispatch value.
"""
from re import S
from flex_dispatch import dispatcher

from dataclasses import dataclass

# For the sake of this demo, lets assume EmailSender and EmailAddress are third-party classes.
# Note EmailSender's send method is a flex dispatcher that can handle a string or an EmailAddress object.
# It would be trivial to implement that functionality without using dispatcher, but using dispatcher makes it
# very easy for users to extend EmailSender's functionality
# 

@dataclass
class EmailAddress:
    address: str

class EmailSender:
    """Dummy class that sends email."""
    def _do_send(self, address: str):
        print(f'Sending email to {address}')
        return True  # our emails never fail to send

    @dispatcher
    def send(self, address) -> bool:  # type: ignore
        if isinstance(address, str):
            # returning an Inline means the contained callabale will be invoked
            # and since our dispatcher is a method, the first arg will be the self reference
            return dispatcher.Inline(lambda s, a: s._do_send(a))  # type: ignore
        elif isinstance(address, EmailAddress):
            return dispatcher.Inline(lambda s, a: s._do_send(a.address))  # type: ignore


# this works pretty well for us:
es = EmailSender()
es.send('foo@bar.com')
es.send(EmailAddress('bash@bar.com'))


# but we have our own EmailAddress class, and it would be great if we could make EmailSender just work for it:
@dataclass
class MyBetterEmailAddress:
    better_address: str

    def get_my_address(self):
        return self.better_address

def send_dispatch(self, address):  # the dispatcher is a method, so we still get send here!
    if isinstance(address, MyBetterEmailAddress):
        return MyBetterEmailAddress  # instead of using inline or static, we're using dispatch value.

EmailSender.send.extend(send_dispatch)

@EmailSender.send.map(MyBetterEmailAddress)
def send_better(self: EmailSender, address):  # remember, dispatch is a method, so we still get the self reference when we're extending the dispatch.
    self._do_send(address.get_my_address())


# now EmailSender works for our type, without having to modify or extnd EmailSender!
es.send(MyBetterEmailAddress(better_address='bang@bar.com'))
