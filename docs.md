# Tables

**chat**


**message**
Each row in the message table represents one sent message.
- `handle_id` is the id of the handle that sent the message
- `associated_message_type`??
    Values: 0, 2, 3, 1000, 2000-2005, 3000-3005. What does each one mean

**handle**
Each row in the handle table represents a unique account that you have sent/received messages with.
- There are separate handles for a number that you have both imessaged and sms messaged with.


Current:
- Research on what the message types are
- Splitting up message response by user.