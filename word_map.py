from db import MessagesDB
from datetime import datetime, timedelta
from collections import defaultdict
from collections import Counter
from constants import AP_SQUAD_ID



def count_words_in_ap_squad_messages():
    """
    Count the number of times each word was sent in the AP squad chat for the past year.
    Returns:
        Dictionary with words as keys and their counts as values
    """
    
    with MessagesDB() as db:
        chat_messages = db.get_chat_messages(chat_identifier=AP_SQUAD_ID)
        
        word_count = defaultdict(int)
        
        for message in chat_messages:
            if message["text"] is not None:
                words = message["text"].split()
                for word in words:
                    word_count[word.lower()] += 1
        
    return word_count

def main():
    word_counts = count_words_in_ap_squad_messages()
    
    counter = Counter(word_counts)
    
    for word, count in counter.most_common(50):
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
