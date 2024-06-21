from .assets.validate import is_not_valid
from . import MAIL, Message

def send_mail(mail_data: dict) -> tuple:
    """
    params: dict -> keys{ subject: string, recipients: arry, body: string}
    return: tuple (status: bool, message: string)
    summery: get json data from client and send to specific peoples
    """
    # get json mail data 
    if is_not_valid(mail_data):
        return ( False, "Check your input!" )
    # initialize message object for sending main
    try:
        message = Message(
        subject=mail_data["subject"],
            sender="rockyrityguard@gmail.com",
            recipients=mail_data["recipients"],
            body=mail_data["body"]
        )
        MAIL.send(message=message)
        return ( True, "Mail Sent" )
    except Exception as err:
        return ( False, "Something wrong while mail sending" )
        