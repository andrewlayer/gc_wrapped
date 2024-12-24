import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from db import MessagesDB, apple_time_to_datetime, datetime_to_apple_time
from collections import Counter

def db_text_coverage(start_date=None, end_date=None, periodicity='W'):
    """
    Returns dataframe of total messages and messages with non-null text per period (Week, month, year etc)
    
    'D': Daily
    'W': Weekly
    'M': Monthly
    'Q': Quarterly
    'Y': Yearly
    """

    with MessagesDB() as db:
        query = """
            SELECT
                message.date,
                message.text
            FROM message
        """
        conditions = []
        params = []

        if start_date:
            conditions.append("message.date >= ?")
            params.append(datetime_to_apple_time(start_date))
        if end_date:
            conditions.append("message.date <= ?")
            params.append(datetime_to_apple_time(end_date))

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        results = db.execute_query(query, params)
        dict_results = [{'date': row[0], 'has_text': bool(row[1])} for row in results]

        # Extract the period from each message's date based on the periodicity
        periods = [apple_time_to_datetime(msg['date']).strftime({
            'D': '%Y-%m-%d',
            'W': '%Y-%W',
            'M': '%Y-%m',
            'Q': '%Y-Q' + str((apple_time_to_datetime(msg['date']).month - 1) // 3 + 1),
            'Y': '%Y'
        }[periodicity]) for msg in dict_results]
        
        periods_with_non_null_txt = [apple_time_to_datetime(msg['date']).strftime({
            'D': '%Y-%m-%d',
            'W': '%Y-%W',
            'M': '%Y-%m',
            'Q': '%Y-Q' + str((apple_time_to_datetime(msg['date']).month - 1) // 3 + 1),
            'Y': '%Y'
        }[periodicity]) for msg in dict_results if msg['has_text']]

        # Count the number of messages per period
        all_msg_period_counts = Counter(periods)
        non_null_txt_period_counts = Counter(periods_with_non_null_txt)
        
        # Sort the periods
        sorted_periods = sorted(all_msg_period_counts.keys())
        total_counts = [all_msg_period_counts[period] for period in sorted_periods]
        non_null_counts = [non_null_txt_period_counts.get(period, 0) for period in sorted_periods]
        
        # Plot the results
        plt.figure(figsize=(10, 5))
        plt.bar(sorted_periods, total_counts, label='Total Messages')
        plt.bar(sorted_periods, non_null_counts, label='Messages with Non-null Text', alpha=0.7)
        plt.xlabel('Period')
        plt.ylabel('Number of Messages')
        plt.title(f'Number of Messages per {periodicity}')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

db_text_coverage(periodicity='M')