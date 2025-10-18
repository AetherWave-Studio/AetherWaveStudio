// Vercel Serverless Function - Check Video Generation Status
// Polls KIE.AI API to check if video generation is complete

import fetch from 'node-fetch';
import { HttpsProxyAgent } from 'https-proxy-agent';

export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight OPTIONS request
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only allow GET requests
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Get API key from environment variables
  const sunoApiKey = process.env.SUNO_API_KEY;

  if (!sunoApiKey) {
    return res.status(500).json({ error: 'SUNO API key not configured' });
  }

  // Get taskId from query parameters
  const { taskId } = req.query;

  if (!taskId) {
    return res.status(400).json({ error: 'taskId is required' });
  }

  // Proxy setup
  const proxyUrl = 'http://mfvrmgdc:3281gl8vgvlp@142.111.48.253:7030';
  const agent = new HttpsProxyAgent(proxyUrl);

  try {
    // Check video generation status
    const statusResponse = await fetch(
      `https://api.kie.ai/api/v1/mp4/record-info?taskId=${taskId}`,
      {
        headers: {
          'Authorization': `Bearer ${sunoApiKey}`
        },
        agent  // Route through proxy
      }
    );

    if (!statusResponse.ok) {
      return res.status(statusResponse.status).json({
        error: 'Failed to check video status',
        details: await statusResponse.text()
      });
    }

    const statusData = await statusResponse.json();
    console.log('Video status full response:', JSON.stringify(statusData, null, 2));

    const status = statusData.data?.status;
    const response = statusData.data?.response;

    console.log('Video status check:', { taskId, status, hasResponse: !!response });

    // Check if generation is complete
    if (status && status !== 'PENDING' && status !== 'PROCESSING') {
      if (status === 'SUCCESS' || status === 'COMPLETE' || response) {
        // Video is ready
        const videoUrl = response?.videoUrl || response?.url;
        const coverUrl = response?.coverUrl || response?.imageUrl;

        return res.status(200).json({
          status: 'complete',
          videoUrl: videoUrl,
          coverUrl: coverUrl,
          taskId: taskId
        });
      }
    }

    // Check for errors
    if (status === 'error' || status === 'failed') {
      return res.status(500).json({
        status: 'failed',
        error: 'Video generation failed',
        details: statusData.data?.errorMessage || 'Generation failed'
      });
    }

    // Still processing
    return res.status(200).json({
      status: 'processing',
      message: 'Video is still being generated',
      taskId: taskId
    });

  } catch (error) {
    console.error('Video Status Check Error:', error);
    return res.status(500).json({
      error: 'Failed to check video status',
      details: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
}
