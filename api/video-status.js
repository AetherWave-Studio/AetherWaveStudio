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

    // The mp4/record-info endpoint structure is different from music generation
    // It returns: { code: 0, msg: "", data: { taskId: "" } }
    // When video is ready, it might return additional fields in data

    if (statusData.code === 0) {
      // Check if we have video data in the response
      if (statusData.data?.videoUrl || statusData.data?.url || statusData.data?.mp4Url) {
        // Video is ready
        const videoUrl = statusData.data.videoUrl || statusData.data.url || statusData.data.mp4Url;
        const coverUrl = statusData.data.coverUrl || statusData.data.imageUrl;

        return res.status(200).json({
          status: 'complete',
          videoUrl: videoUrl,
          coverUrl: coverUrl,
          taskId: taskId
        });
      }

      // If we only have taskId, video is still processing
      return res.status(200).json({
        status: 'processing',
        message: 'Video is still being generated',
        taskId: taskId,
        debug: statusData
      });
    }

    // Check for errors
    if (statusData.code !== 0 && statusData.msg) {
      return res.status(500).json({
        status: 'failed',
        error: 'Video generation failed',
        details: statusData.msg
      });
    }

    // Unknown response
    return res.status(200).json({
      status: 'unknown',
      message: 'Unable to determine video status',
      taskId: taskId,
      debug: statusData
    });

  } catch (error) {
    console.error('Video Status Check Error:', error);
    return res.status(500).json({
      error: 'Failed to check video status',
      details: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
}
