// Vercel Serverless Function - Music Video Generation API
// Uses KIE.AI SUNO API to generate music videos from audio

// Import node-fetch explicitly to use with proxy agent
import fetch from 'node-fetch';
import { HttpsProxyAgent } from 'https-proxy-agent';

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
    musicTaskId, // Required: taskId from music generation
    audioId // Individual track ID (for reference)
  } = req.body;

  if (!musicTaskId) {
    return res.status(400).json({
      error: 'Invalid request. musicTaskId is required for music video generation.'
    });
  }

  // Proxy setup - use your Webshare details here
  const proxyUrl = 'http://mfvrmgdc:3281gl8vgvlp@142.111.48.253:7030';
  const agent = new HttpsProxyAgent(proxyUrl);

  try {
    // KIE.AI mp4/generate expects:
    // - taskId: music generation taskId (identifies the original music task)
    // - audioId: individual track ID (which variation to visualize)
    // - callBackUrl, author, domainName: optional metadata
    const requestPayload = {
      taskId: musicTaskId,  // Music generation taskId
      audioId: audioId,      // Specific track ID to visualize
      callBackUrl: 'https://aetherwavestudio.com/api/video-callback',
      author: 'AetherWave Studio',
      domainName: 'aetherwavestudio.com'
    };

    console.log('Generating music video with SUNO API:', {
      musicTaskId,
      trackId: audioId,
      prompt,
      payload: requestPayload
    });

    // Use the mp4 generate endpoint for video generation
    const generateResponse = await fetch('https://api.kie.ai/api/v1/mp4/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${sunoApiKey}`
      },
      body: JSON.stringify(requestPayload),
      agent  // Route through proxy
    });

    if (!generateResponse.ok) {
      const errorText = await generateResponse.text();
      console.error('SUNO Video Generate Error (raw):', errorText);
      console.error('Response status:', generateResponse.status);
      console.error('Response headers:', Object.fromEntries(generateResponse.headers.entries()));

      let errorDetails;
      try {
        const errorJson = JSON.parse(errorText);
        errorDetails = errorJson.msg || errorJson.message || 'Unknown error';
      } catch (e) {
        errorDetails = errorText.substring(0, 200);
      }

      return res.status(generateResponse.status).json({
        error: 'Video generation request failed',
        details: errorDetails
      });
    }

    const responseText = await generateResponse.text();
    console.log('SUNO Video API Response (raw):', responseText);

    let generateData;
    try {
      generateData = JSON.parse(responseText);
    } catch (e) {
      console.error('Failed to parse response as JSON:', e.message);
      return res.status(500).json({
        error: 'Invalid API response',
        details: responseText.substring(0, 200)
      });
    }
    console.log('SUNO Video API Response:', JSON.stringify(generateData, null, 2));

    // Check if the API accepted the request
    if (generateData.code !== 200) {
      return res.status(500).json({
        error: 'Video generation request failed',
        details: generateData.msg || 'Unknown error'
      });
    }

    console.log('Video generation started for musicTaskId:', musicTaskId);

    // Return immediately - video generation is async
    // KIE.AI will call our webhook when complete
    // Client should poll the status endpoint to check progress
    return res.status(202).json({
      status: 'processing',
      message: 'Video generation started. This may take 10-15 minutes.',
      taskId: musicTaskId,
      audioId: audioId,
      prompt: prompt
    });

  } catch (error) {
    console.error('Video Generation Error:', error);
    return res.status(500).json({
      error: 'Failed to generate video',
      details: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
}
