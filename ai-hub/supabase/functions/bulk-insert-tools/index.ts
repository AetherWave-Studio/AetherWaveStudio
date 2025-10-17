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
        const { tools } = await req.json();

        if (!tools || !Array.isArray(tools)) {
            throw new Error('Tools array is required');
        }

        console.log(`Received ${tools.length} tools for bulk insertion`);

        // Get environment variables
        const serviceRoleKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');
        const supabaseUrl = Deno.env.get('SUPABASE_URL');

        if (!serviceRoleKey || !supabaseUrl) {
            throw new Error('Supabase configuration missing');
        }

        // Process tools in batches of 100 to avoid payload size limits
        const batchSize = 100;
        const totalBatches = Math.ceil(tools.length / batchSize);
        let totalInserted = 0;
        const insertResults = [];

        for (let batchIndex = 0; batchIndex < totalBatches; batchIndex++) {
            const startIndex = batchIndex * batchSize;
            const endIndex = Math.min(startIndex + batchSize, tools.length);
            const batchTools = tools.slice(startIndex, endIndex);

            console.log(`Processing batch ${batchIndex + 1}/${totalBatches} with ${batchTools.length} tools`);

            // Prepare tools data for insertion
            const toolsData = batchTools.map(tool => ({
                name: tool.name || '',
                description: tool.description || '',
                link: tool.link || '',
                category: tool.category || '',
                logo_url: tool.logo_url || null,
                screenshot_url: tool.screenshot_url || null,
                featured: tool.featured || false,
                popularity_score: tool.popularity_score || 0.0,
                source: tool.source || null
            }));

            // Insert batch into database
            const insertResponse = await fetch(`${supabaseUrl}/rest/v1/tools`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${serviceRoleKey}`,
                    'apikey': serviceRoleKey,
                    'Content-Type': 'application/json',
                    'Prefer': 'return=minimal'
                },
                body: JSON.stringify(toolsData)
            });

            if (!insertResponse.ok) {
                const errorText = await insertResponse.text();
                console.error(`Batch ${batchIndex + 1} insertion failed:`, errorText);
                throw new Error(`Batch ${batchIndex + 1} insertion failed: ${errorText}`);
            }

            totalInserted += batchTools.length;
            insertResults.push({
                batch: batchIndex + 1,
                inserted: batchTools.length,
                status: 'success'
            });

            console.log(`Batch ${batchIndex + 1} completed: ${batchTools.length} tools inserted`);
        }

        // Verify total count in database
        const countResponse = await fetch(`${supabaseUrl}/rest/v1/tools?select=count()`, {
            headers: {
                'Authorization': `Bearer ${serviceRoleKey}`,
                'apikey': serviceRoleKey,
                'Content-Type': 'application/json'
            }
        });

        let totalInDatabase = 0;
        if (countResponse.ok) {
            const countData = await countResponse.json();
            totalInDatabase = countData[0]?.count || 0;
        }

        const result = {
            data: {
                message: 'Bulk insertion completed successfully',
                totalProcessed: tools.length,
                totalInserted: totalInserted,
                totalInDatabase: totalInDatabase,
                batches: insertResults,
                batchSize: batchSize,
                totalBatches: totalBatches
            }
        };

        console.log('Bulk insertion completed:', result.data);

        return new Response(JSON.stringify(result), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });

    } catch (error) {
        console.error('Bulk insertion error:', error);

        const errorResponse = {
            error: {
                code: 'BULK_INSERT_FAILED',
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