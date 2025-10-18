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
    duration = '10',
    aspectRatio = '16:9',
    audioId // Optional: existing audio ID from music generation
  } = req.body;

  if (!prompt) {
    return res.status(400).json({
      error: 'Invalid request. Prompt is required.'
    });
  }

  // Proxy setup - use your Webshare details here
  const proxyUrl = 'http://mfvrmgdc:3281gl8vgvlp@142.111.48.253:7030';
  const agent = new HttpsProxyAgent(proxyUrl);

  try {
    const requestPayload = {
      prompt: prompt,
      callBackUrl: 'https://aetherwavestudio.com/api/video-callback'
    };

    // If audioId is provided, use it (for generating video from existing audio)
    if (audioId) {
      requestPayload.audioId = audioId;
    }

    console.log('Generating music video with SUNO API:', {
      prompt,
      duration,
      aspectRatio,
      hasAudioId: !!audioId
    });

    // Use the same generate endpoint as music, with video-specific parameters
    const generateResponse = await fetch('https://api.kie.ai/api/v1/generate/video', {
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

    const taskId = generateData.data?.taskId;

    if (!taskId) {
      console.error('No taskId found. Full response:', generateData);
      return res.status(500).json({
        error: 'No taskId returned from SUNO API',
        details: 'Response: ' + JSON.stringify(generateData)
      });
    }

    console.log('Video generation started, taskId:', taskId);

    // Step 2: Poll for completion (with timeout)
    const maxAttempts = 60; // 60 attempts (videos take longer)
    const pollInterval = 3000; // 3 seconds
    let attempts = 0;
    let videoData = null;

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
      const status = statusData.data?.status;
      const response = statusData.data?.response;

      console.log(`Attempt ${attempts}: Status = ${status}, has response = ${!!response}`);

      // Check if generation is complete
      // Wait for status to be SUCCESS/COMPLETE and response to be populated
      if (status && status !== 'PENDING' && status !== 'PROCESSING') {
        if (status === 'SUCCESS' || status === 'COMPLETE' || response) {
          videoData = statusData.data;
          console.log('Video generation complete! Data:', JSON.stringify(videoData, null, 2));
          break;
        }
      }

      // Check for errors
      if (statusData.data?.status === 'error' || statusData.data?.status === 'failed') {
        return res.status(500).json({
          error: 'Video generation failed',
          details: statusData.data?.errorMessage || 'Generation failed'
        });
      }
    }

    // Check if we got the video data
    if (!videoData || !videoData.response) {
      return res.status(408).json({
        error: 'Video generation timeout',
        message: 'Generation is taking longer than expected. Please try again.',
        taskId: taskId
      });
    }

    // Extract video URL from response
    const videoUrl = videoData.response.videoUrl || videoData.response.url;
    const coverUrl = videoData.response.coverUrl || videoData.response.imageUrl;

    // Return successful response
    return res.status(200).json({
      videoUrl: videoUrl,
      coverUrl: coverUrl,
      taskId: taskId,
      prompt: prompt,
      duration: duration,
      aspectRatio: aspectRatio
    });

  } catch (error) {
    console.error('Video Generation Error:', error);
    return res.status(500).json({
      error: 'Failed to generate video',
      details: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
}
