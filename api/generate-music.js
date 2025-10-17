// Vercel Serverless Function - Music Generation API
// Uses KIE.AI SUNO API to generate music from text prompts

const { HttpsProxyAgent } = require('https-proxy-agent');

export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight OPTIONS request
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Get API key from environment variables
  const sunoApiKey = process.env.SUNO_API_KEY;

  if (!sunoApiKey) {
    return res.status(500).json({ error: 'SUNO API key not configured' });
  }

  // Validate request body
  const {
    prompt,
    title,
    style,
    model = 'V5',
    instrumental = false,
    customMode = false
  } = req.body;

  if (!prompt && (!customMode || !title || !style)) {
    return res.status(400).json({
      error: 'Invalid request. Simple mode requires prompt. Custom mode requires title and style.'
    });
  }

  // Rate limiting check
  if (prompt && prompt.length > 3000) {
    return res.status(400).json({ error: 'Prompt/Lyrics too long (max 3000 characters)' });
  }

  // Proxy setup - use your Webshare details here
  const proxyUrl = 'https://mfvrmgdc:3281gl8vgvlp@142.111.48.253:7030';  // From Webshare
  const agent = new HttpsProxyAgent(proxyUrl);

  try {
    let requestPayload = {
      model: model,
      instrumental: instrumental,
      customMode: customMode
    };

    if (customMode) {
      // Custom Mode: title, style, and optional lyrics/prompt
      requestPayload.title = title;
      requestPayload.style = style;
      if (prompt) {
        requestPayload.prompt = prompt; // Lyrics
      }
      console.log('Generating music with SUNO API (Custom Mode):', {
        title,
        style,
        hasLyrics: !!prompt,
        model,
        instrumental
      });
    } else {
      // Simple Mode: just prompt
      requestPayload.prompt = prompt;
      console.log('Generating music with SUNO API (Simple Mode):', {
        prompt,
        model,
        instrumental
      });
    }

    const generateResponse = await fetch('https://api.kie.ai/api/v1/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${sunoApiKey}`
      },
      body: JSON.stringify(requestPayload),
      agent  // Route through proxy
    });

    if (!generateResponse.ok) {
      const error = await generateResponse.json();
      console.error('SUNO Generate Error:', error);
      return res.status(generateResponse.status).json({
        error: 'Music generation request failed',
        details: error.msg || 'Unknown error'
      });
    }

    const generateData = await generateResponse.json();
    console.log('SUNO API Response:', JSON.stringify(generateData, null, 2));

    const taskId = generateData.data?.taskId;

    if (!taskId) {
      console.error('No taskId found. Full response:', generateData);
      return res.status(500).json({
        error: 'No taskId returned from SUNO API',
        details: 'Response: ' + JSON.stringify(generateData)
      });
    }

    console.log('Music generation started, taskId:', taskId);

    // Step 2: Poll for completion (with timeout)
    const maxAttempts = 30; // 30 attempts
    const pollInterval = 2000; // 2 seconds
    let attempts = 0;
    let musicData = null;

    while (attempts < maxAttempts) {
      await new Promise(resolve => setTimeout(resolve, pollInterval));
      attempts++;

      const statusResponse = await fetch(
        `https://api.kie.ai/api/v1/generate/record-info?taskId=${taskId}`,
        {
          headers: {
            'Authorization': `Bearer ${sunoApiKey}`
          },
          agent  // Route through proxy
        }
      );

      if (!statusResponse.ok) {
        console.error('Status check failed');
        continue;
      }

      const statusData = await statusResponse.json();
      console.log(`Attempt ${attempts}: Status =`, statusData.data?.status);

      // Check if generation is complete
      if (statusData.data?.status === 'complete') {
        musicData = statusData.data;
        break;
      }

      // Check for errors
      if (statusData.data?.status === 'error' || statusData.data?.status === 'failed') {
        return res.status(500).json({
          error: 'Music generation failed',
          details: statusData.data?.errorMessage || 'Generation failed'
        });
      }
    }

    // Check if we got the music data
    if (!musicData || !musicData.audioUrl) {
      return res.status(408).json({
        error: 'Music generation timeout',
        message: 'Generation is taking longer than expected. Please try again.',
        taskId: taskId
      });
    }

    // Return successful response
    return res.status(200).json({
      audioUrl: musicData.audioUrl,
      imageUrl: musicData.imageUrl,
      title: musicData.title || title || 'Generated Track',
      duration: musicData.duration,
      prompt: prompt,
      style: style,
      taskId: taskId
    });

  } catch (error) {
    console.error('Music Generation Error:', error);
    return res.status(500).json({
      error: 'Failed to generate music',
      details: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
}
