// Vercel Serverless Function - Check Seedance Video Generation Status
// Polls KIE.AI API to check if Seedance video generation is complete

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
  const seedanceApiKey = process.env.SEEDANCE1_API_KEY;

  if (!seedanceApiKey) {
    return res.status(500).json({ error: 'Seedance API key not configured' });
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
    // Check Seedance video generation status using jobs query endpoint
    // Use query parameter instead of path parameter
    const statusResponse = await fetch(
      `https://api.kie.ai/api/v1/jobs/query?taskId=${taskId}`,
      {
        headers: {
          'Authorization': `Bearer ${seedanceApiKey}`
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
    console.log('Seedance video status full response:', JSON.stringify(statusData, null, 2));

    // KIE.AI Seedance jobs endpoint returns:
    // { code: 200, msg: "success", data: { taskId: "...", status: "...", output: { ... } } }

    // Check for success
    if (statusData.code === 200) {
      const jobData = statusData.data;
      const jobStatus = jobData?.status;

      // Check job status
      if (jobStatus === 'completed' || jobStatus === 'succeeded' || jobStatus === 'success' || jobData?.state === 'success') {
        // Video is ready - parse the output/resultJson
        let videoUrl = null;
        let coverUrl = null;

        // Try output field first
        const output = jobData?.output;
        if (output?.video_url || output?.videoUrl || output?.url) {
          videoUrl = output.video_url || output.videoUrl || output.url;
          coverUrl = output?.cover_url || output?.coverUrl ||
                     output?.thumbnail_url || output?.thumbnailUrl;
        }
        // Try parsing resultJson field (Seedance format)
        else if (jobData?.resultJson) {
          try {
            const result = JSON.parse(jobData.resultJson);
            if (result.resultUrls && result.resultUrls.length > 0) {
              videoUrl = result.resultUrls[0];
            }
          } catch (e) {
            console.error('Failed to parse resultJson:', e);
          }
        }

        if (videoUrl) {
          return res.status(200).json({
            status: 'complete',
            videoUrl: videoUrl,
            coverUrl: coverUrl,
            taskId: taskId,
            duration: jobData?.duration,
            resolution: jobData?.resolution,
            model: jobData?.model,
            costTime: jobData?.costTime
          });
        }
      }

      // Check if job failed
      if (jobStatus === 'failed' || jobStatus === 'error') {
        return res.status(500).json({
          status: 'failed',
          error: 'Video generation failed',
          details: jobData?.error || jobData?.errorMessage || 'Unknown error',
          taskId: taskId
        });
      }

      // Job is still processing (pending, running, etc.)
      return res.status(200).json({
        status: 'processing',
        message: 'Video is still being generated with Seedance 1.0',
        taskId: taskId,
        jobStatus: jobStatus,
        progress: jobData?.progress
      });
    }

    // Check for API errors
    if (statusData.code !== 200) {
      return res.status(500).json({
        status: 'failed',
        error: 'Failed to check video status',
        details: statusData.msg || 'Unknown error',
        code: statusData.code
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
