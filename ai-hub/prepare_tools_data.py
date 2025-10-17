import json

# Read tools data and prepare for batch insertion
with open('tools_for_insertion.json', 'r') as f:
    tools = json.load(f)

print(f"Processing {len(tools)} tools...")

# Process tools in batches of 100 for manageable SQL statements
batch_size = 100
total_batches = (len(tools) + batch_size - 1) // batch_size

for batch_num in range(total_batches):
    start_idx = batch_num * batch_size
    end_idx = min(start_idx + batch_size, len(tools))
    batch_tools = tools[start_idx:end_idx]
    
    sql_values = []
    for tool in batch_tools:
        # Escape single quotes and handle None values
        name = tool['name'].replace("'", "''") if tool['name'] else ''
        description = tool['description'].replace("'", "''") if tool['description'] else ''
        link = tool['link'].replace("'", "''") if tool['link'] else ''
        category = tool['category'].replace("'", "''") if tool['category'] else ''
        
        if tool.get('logo_url'):
            logo_url = "'" + tool['logo_url'].replace("'", "''") + "'"
        else:
            logo_url = 'NULL'
            
        if tool.get('screenshot_url'):
            screenshot_url = "'" + tool['screenshot_url'].replace("'", "''") + "'"
        else:
            screenshot_url = 'NULL'
            
        featured = 'true' if tool.get('featured', False) else 'false'
        popularity_score = tool.get('popularity_score', 0.0)
        
        if tool.get('source'):
            source = "'" + tool['source'].replace("'", "''") + "'"
        else:
            source = 'NULL'
        
        sql_values.append(f"('{name}', '{description}', '{link}', '{category}', {logo_url}, {screenshot_url}, {featured}, {popularity_score}, {source})")
    
    batch_sql = f"""
INSERT INTO tools (name, description, link, category, logo_url, screenshot_url, featured, popularity_score, source) VALUES
{', '.join(sql_values)};
"""
    
    with open(f'insert_tools_batch_{batch_num + 1}.sql', 'w') as f:
        f.write(batch_sql)
    
    print(f"Created batch {batch_num + 1}/{total_batches} with {len(batch_tools)} tools")

print(f"All {total_batches} SQL batch files created")
