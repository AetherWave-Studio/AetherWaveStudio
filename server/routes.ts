import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { z } from "zod";

export async function registerRoutes(app: Express): Promise<Server> {
  // Music generation route with vocal gender support
  app.post("/api/generate-music", async (req, res) => {
    try {
      const { 
        prompt, 
        model = 'V5', 
        instrumental = false, 
        vocalGender = 'm',
        customMode = false,
        title,
        style
      } = req.body;

      console.log('Music generation request:', { prompt, model, instrumental, vocalGender, customMode, title, style });

      const sunoApiKey = process.env.SUNO_API_KEY;
      if (!sunoApiKey) {
        return res.status(500).json({ 
          error: 'SUNO API key not configured',
          details: 'Please add SUNO_API_KEY to your secrets'
        });
      }

      // Build SUNO API request with vocal gender
      const sunoPayload: any = {
        model: model,
        instrumental: instrumental,
        gender: vocalGender
      };

      if (customMode) {
        sunoPayload.custom_mode = true;
        sunoPayload.title = title;
        sunoPayload.tags = style;
        sunoPayload.prompt = prompt;
      } else {
        sunoPayload.custom_mode = false;
        sunoPayload.prompt = prompt;
      }

      // Call SUNO API
      const sunoResponse = await fetch('https://studio-api.prod.suno.com/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sunoApiKey}`
        },
        body: JSON.stringify(sunoPayload)
      });

      if (!sunoResponse.ok) {
        const errorData = await sunoResponse.json().catch(() => ({}));
        return res.status(sunoResponse.status).json({
          error: 'SUNO API error',
          details: errorData.message || sunoResponse.statusText
        });
      }

      const sunoData = await sunoResponse.json();
      
      // Return formatted response
      res.json({
        taskId: sunoData.id || sunoData.task_id,
        tracks: sunoData.clips || sunoData.tracks || []
      });

    } catch (error: any) {
      console.error('Music generation error:', error);
      res.status(500).json({ 
        error: 'Failed to generate music',
        details: error.message 
      });
    }
  });

  // User preferences route
  app.get("/api/user/preferences", async (req, res) => {
    try {
      const userId = (req as any).user?.sub;
      if (!userId) {
        return res.status(401).json({ error: 'Not authenticated' });
      }

      const user = await storage.getUser(userId);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      res.json({ vocalGenderPreference: user.vocalGenderPreference });
    } catch (error: any) {
      res.status(500).json({ error: error.message });
    }
  });

  // Update user vocal preference
  app.post("/api/user/preferences", async (req, res) => {
    try {
      const userId = (req as any).user?.sub;
      if (!userId) {
        return res.status(401).json({ error: 'Not authenticated' });
      }

      const { vocalGenderPreference } = req.body;
      const user = await storage.updateUserVocalPreference(userId, vocalGenderPreference);
      
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      res.json({ success: true, vocalGenderPreference: user.vocalGenderPreference });
    } catch (error: any) {
      res.status(500).json({ error: error.message });
    }
  });

  const httpServer = createServer(app);

  return httpServer;
}
