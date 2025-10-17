import json

# Read tools data and skip the first 5 (already inserted)
with open('tools_for_insertion.json', 'r') as f:
    all_tools = json.load(f)

remaining_tools = all_tools[5:]
print(f"Preparing {len(remaining_tools)} tools for bulk insertion")

# Save the remaining tools data for the edge function
with open('remaining_tools_for_bulk_insert.json', 'w') as f:
    json.dump(remaining_tools, f, indent=2)

print(f"Saved {len(remaining_tools)} tools to remaining_tools_for_bulk_insert.json")

# Also save just a small sample for initial testing
sample_tools = remaining_tools[:10]
with open('sample_tools_for_testing.json', 'w') as f:
    json.dump(sample_tools, f, indent=2)

print(f"Also saved {len(sample_tools)} sample tools for testing")
