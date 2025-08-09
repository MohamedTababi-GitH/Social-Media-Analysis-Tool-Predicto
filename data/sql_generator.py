import json

input_file = 'sm_data.json'
output_sql = 'insert_data.sql'

with open(input_file, 'r', encoding='utf-8') as f, open(output_sql, 'w', encoding='utf-8') as out:
    
    out.write('-- SQL dump generated from sm_data.json\n\n')

    # transaction beging
    out.write('BEGIN;\n\n')

    for line_num, line in enumerate(f, start=1):
        data = json.loads(line)
        # convert dict back to JSON string and escape single quotes for SQL
        json_str = json.dumps(data).replace("'", "''")
        sql = f"INSERT INTO social_media_data (data) VALUES ('{json_str}'::jsonb);\n"
        out.write(sql)

        if line_num % 1000 == 0:
            out.write('\n')  

    # transaction end
    out.write('\nCOMMIT;\n')

print(f"SQL dump file '{output_sql}' created successfully")
