from db import MessagesDB


def main():
    with MessagesDB() as db:
        # Verify tables exist
        schema_check = db.execute_query(
            """
            SELECT name FROM sqlite_master 
            WHERE type='table'
        """
        )

        if schema_check:
            print("Available tables:", schema_check)

            # Query messages
            results = db.execute_query(
                """
                SELECT text, date 
                FROM message 
                WHERE text IS NOT NULL 
                LIMIT 5
            """
            )

            if results:
                for row in results:
                    print(row)
            else:
                print("No messages found")


if __name__ == "__main__":
    main()
