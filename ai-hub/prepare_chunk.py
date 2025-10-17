import json

# Read the full remaining tools data
with open('remaining_tools_for_bulk_insert.json', 'r') as f:
    remaining_tools = json.load(f)

print(f"Loaded {len(remaining_tools)} tools for bulk insertion")

# Since the edge function processes in batches of 100, let's send a reasonable chunk
# Start with 200 tools to test payload limits
chunk_size = 200
tools_chunk = remaining_tools[:chunk_size]

with open('tools_chunk_for_insertion.json', 'w') as f:
    json.dump(tools_chunk, f, indent=2)

print(f"Prepared chunk of {len(tools_chunk)} tools for insertion")
print(f"First tool: {tools_chunk[0]['name']}")
print(f"Last tool: {tools_chunk[-1]['name']}")

# Also prepare the remaining tools for the next batch
remaining_after_chunk = remaining_tools[chunk_size:]
with open('remaining_after_chunk.json', 'w') as f:
    json.dump(remaining_after_chunk, f, indent=2)

print(f"Remaining tools after chunk: {len(remaining_after_chunk)}")
