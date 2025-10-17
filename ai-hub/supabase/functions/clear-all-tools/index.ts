Deno.serve(async (req) => {
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE, PATCH',
        'Access-Control-Max-Age': '86400',
        'Access-Control-Allow-Credentials': 'false'
    };

    if (req.method === 'OPTIONS') {
        return new Response(null, { status: 200, headers: corsHeaders });
    }

    try {
        const { confirm } = await req.json();

        if (confirm !== 'CLEAR_ALL_TOOLS') {
            throw new Error('Confirmation required to clear all tools');
        }

        console.log('Starting to clear all existing tools from database');

        // Get environment variables
        const serviceRoleKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');
        const supabaseUrl = Deno.env.get('SUPABASE_URL');

        if (!serviceRoleKey || !supabaseUrl) {
            throw new Error('Supabase configuration missing');
        }

        // First, get count of existing tools
        const countResponse = await fetch(`${supabaseUrl}/rest/v1/tools?select=count()`, {
            headers: {
                'Authorization': `Bearer ${serviceRoleKey}`,
                'apikey': serviceRoleKey,
                'Content-Type': 'application/json'
            }
        });

        let existingCount = 0;
        if (countResponse.ok) {
            const countData = await countResponse.json();
            existingCount = countData[0]?.count || 0;
        }

        console.log(`Found ${existingCount} existing tools to clear`);

        // Delete all tools (need WHERE clause)
        const deleteResponse = await fetch(`${supabaseUrl}/rest/v1/tools?id=gte.0`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${serviceRoleKey}`,
                'apikey': serviceRoleKey,
                'Content-Type': 'application/json'
            }
        });

        if (!deleteResponse.ok) {
            const errorText = await deleteResponse.text();
            console.error('Failed to clear tools:', errorText);
            throw new Error(`Failed to clear tools: ${errorText}`);
        }

        // Verify deletion
        const verifyResponse = await fetch(`${supabaseUrl}/rest/v1/tools?select=count()`, {
            headers: {
                'Authorization': `Bearer ${serviceRoleKey}`,
                'apikey': serviceRoleKey,
                'Content-Type': 'application/json'
            }
        });

        let remainingCount = 0;
        if (verifyResponse.ok) {
            const verifyData = await verifyResponse.json();
            remainingCount = verifyData[0]?.count || 0;
        }

        const result = {
            data: {
                message: 'All tools cleared successfully',
                existingCount: existingCount,
                remainingCount: remainingCount,
                cleared: existingCount - remainingCount,
                timestamp: new Date().toISOString()
            }
        };

        console.log('Tools clearing completed:', result.data);

        return new Response(JSON.stringify(result), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });

    } catch (error) {
        console.error('Clear tools error:', error);

        const errorResponse = {
            error: {
                code: 'CLEAR_TOOLS_FAILED',
                message: error.message,
                timestamp: new Date().toISOString()
            }
        };

        return new Response(JSON.stringify(errorResponse), {
            status: 500,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
    }
});