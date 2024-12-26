from helpers.db import MessagesDB
from datetime import datetime
import sqlite3


def escape_sql_identifier(identifier):
    """Safely escape SQL identifiers"""
    return f'"{identifier}"'


def dump_schema_to_md():
    try:
        with MessagesDB() as db:
            # Get all tables
            tables = db.execute_query(
                """
                SELECT name 
                FROM sqlite_master 
                WHERE type='table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name;
            """
            )

            if not tables:
                print("No tables found")
                return

            output = []
            output.append("# Messages Database Schema")
            output.append(
                f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

            for (table_name,) in tables:
                safe_table = escape_sql_identifier(table_name)
                output.append(f"## Table: {table_name}\n")

                # Table info
                table_info = db.execute_query(f"PRAGMA table_info({safe_table})")
                if table_info:
                    output.append("### Columns\n")
                    output.append("| Column | Type | NotNull | DefaultValue | PK |")
                    output.append("|--------|------|----------|--------------|-----|")
                    for col in table_info:
                        cid, name, type_, notnull, dflt_value, pk = col
                        default_val = dflt_value if dflt_value is not None else ""
                        output.append(
                            f"| {name} | {type_} | {bool(notnull)} | {default_val} | {bool(pk)} |"
                        )
                    output.append("")

                # Foreign keys
                foreign_keys = db.execute_query(
                    f"PRAGMA foreign_key_list({safe_table})"
                )
                if foreign_keys:
                    output.append("### Foreign Keys\n")
                    output.append("| Column | References | On Delete | On Update |")
                    output.append("|--------|------------|-----------|-----------|")
                    for fk in foreign_keys:
                        _, _, ref_table, from_, to, on_update, on_delete, _ = fk
                        output.append(
                            f"| {from_} | {ref_table}({to}) | {on_delete} | {on_update} |"
                        )
                    output.append("")

                # Indexes
                indexes = db.execute_query(
                    f"""
                    SELECT name, sql 
                    FROM sqlite_master 
                    WHERE type='index' 
                    AND tbl_name={safe_table}
                    AND sql IS NOT NULL
                """
                )
                if indexes:
                    output.append("### Indexes\n")
                    output.append("```sql")
                    for idx_name, idx_sql in indexes:
                        if idx_sql:
                            output.append(f"{idx_sql};")
                    output.append("```\n")

            # Write to file with error handling
            try:
                with open("schema.md", "w") as f:
                    f.write("\n".join(output))
                print("Schema has been written to schema.md")
            except IOError as e:
                print(f"Error writing schema file: {e}")

    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    dump_schema_to_md()
