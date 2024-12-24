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

What is message type??
- There are 71k messages with null text, 91k with non null text
- Lets get counts of each associated_message_type
    - 0 is the most common with 151k, Maybe this is just default text message
    - 2: 71
    - 3: 310


# Get count of messages per handle starting Jan 1 2024
SELECT handle_id, handle.id as handle_id, COUNT(message.ROWID) as message_count
FROM message
JOIN handle ON message.handle_id = handle.ROWID
WHERE message.date > 725760000000000000
GROUP BY handle.id ORDER BY "message_count" desc LIMIT 100

fuck seeds: chat303857515224571892