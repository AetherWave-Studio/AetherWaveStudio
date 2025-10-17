import json

# Read tools data
with open('tools_for_insertion.json', 'r') as f:
    tools = json.load(f)

# Skip the first 5 tools (already inserted)
remaining_tools = tools[5:]
print(f"Creating SQL for {len(remaining_tools)} remaining tools")

# Create smaller batches of 20 tools each for easier execution
batch_size = 20
total_batches = (len(remaining_tools) + batch_size - 1) // batch_size

for batch_num in range(total_batches):
    start_idx = batch_num * batch_size
    end_idx = min(start_idx + batch_size, len(remaining_tools))
    batch_tools = remaining_tools[start_idx:end_idx]
    
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
        
        # Create a single line for this tool
        sql_line = f"('{name}', '{description}', '{link}', '{category}', {logo_url}, {screenshot_url}, {featured}, {popularity_score}, {source})"
        sql_values.append(sql_line)
    
    # Create the complete SQL statement
    batch_sql = "INSERT INTO tools (name, description, link, category, logo_url, screenshot_url, featured, popularity_score, source) VALUES\n" + ",\n".join(sql_values) + ";"
    
    with open(f'tools_small_batch_{batch_num + 1:03d}.sql', 'w') as f:
        f.write(batch_sql)
    
    print(f"Created small batch {batch_num + 1:03d}/{total_batches} with {len(batch_tools)} tools")

print(f"All {total_batches} small SQL batch files created")
