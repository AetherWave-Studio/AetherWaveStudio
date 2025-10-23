import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { setupAuth, isAuthenticated } from "./replitAuth";
import { z } from "zod";
import multer from "multer";
import { db } from "./db";
import { uploadedAudio } from "@shared/schema";
import { eq } from "drizzle-orm";

export async function registerRoutes(app: Express): Promise<Server> {
  // Setup Replit Auth
  await setupAuth(app);

  // Auth user route
  app.get('/api/auth/user', isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const user = await storage.getUser(userId);
      res.json(user);
    } catch (error) {
      console.error("Error fetching user:", error);
      res.status(500).json({ message: "Failed to fetch user" });
    }
  });

  // Music generation route with vocal gender support (KIE.ai API)
  app.post("/api/generate-music", async (req, res) => {
    try {
      const { 
        prompt, 
        model = 'V4_5', 
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
          details: 'Please add SUNO_API_KEY to your Replit Secrets'
        });
      }

      // Build KIE.ai API request
      const sunoPayload: any = {
        prompt: prompt,
        model: model,
        instrumental: instrumental,
        customMode: customMode
      };

      // Add vocal gender only in custom mode (per KIE.ai API spec)
      if (customMode) {
        sunoPayload.vocalGender = vocalGender;
      }

      if (customMode && title) {
        sunoPayload.title = title;
      }
      
      if (customMode && style) {
        sunoPayload.style = style;
      }

      console.log('Sending to KIE.ai:', JSON.stringify(sunoPayload, null, 2));

      // Call KIE.ai SUNO API
      const sunoResponse = await fetch('https://api.kie.ai/api/v1/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sunoApiKey}`
        },
        body: JSON.stringify(sunoPayload)
      });

      if (!sunoResponse.ok) {
        const errorData = await sunoResponse.json().catch(() => ({}));
        console.error('KIE.ai API error:', errorData);
        return res.status(sunoResponse.status).json({
          error: 'SUNO API error',
          details: errorData.msg || errorData.message || sunoResponse.statusText
        });
      }

      const sunoData = await sunoResponse.json();
      console.log('KIE.ai response:', JSON.stringify(sunoData, null, 2));
      
      // KIE.ai returns { code: 200, msg: "success", data: { taskId: "xxx" } }
      if (sunoData.code === 200) {
        // Return task ID - frontend will need to poll for results
        res.json({
          taskId: sunoData.data.taskId,
          status: 'processing',
          message: 'Music generation started. Check status with task ID.'
        });
      } else {
        res.status(500).json({
          error: 'Generation failed',
          details: sunoData.msg || 'Unknown error'
        });
      }

    } catch (error: any) {
      console.error('Music generation error:', error);
      res.status(500).json({ 
        error: 'Failed to generate music',
        details: error.message 
      });
    }
  });

  // Upload & Cover Audio route (KIE.ai API)
  app.post("/api/upload-cover-music", async (req, res) => {
    try {
      const { 
        uploadUrl,
        prompt, 
        model = 'V4_5', 
        instrumental = false, 
        vocalGender = 'm',
        customMode = false,
        title,
        style,
        styleWeight,
        weirdnessConstraint,
        audioWeight,
        negativeTags
      } = req.body;

      console.log('Upload-cover request:', { uploadUrl, prompt, model, instrumental, vocalGender, customMode });

      const sunoApiKey = process.env.SUNO_API_KEY;
      if (!sunoApiKey) {
        return res.status(500).json({ 
          error: 'SUNO API key not configured',
          details: 'Please add SUNO_API_KEY to your Replit Secrets'
        });
      }

      if (!uploadUrl) {
        return res.status(400).json({
          error: 'Upload URL required',
          details: 'Please provide an audio URL to cover'
        });
      }

      // Build KIE.ai upload-cover API request
      const coverPayload: any = {
        uploadUrl: uploadUrl,
        prompt: prompt,
        model: model,
        instrumental: instrumental,
        customMode: customMode,
        callBackUrl: '' // Optional - we're polling instead
      };

      // Add vocal gender only in custom mode (per KIE.ai API spec)
      if (customMode) {
        coverPayload.vocalGender = vocalGender;
      }

      if (customMode && title) {
        coverPayload.title = title;
      }
      
      if (customMode && style) {
        coverPayload.style = style;
      }

      // Add optional advanced parameters
      if (styleWeight !== undefined) {
        coverPayload.styleWeight = styleWeight;
      }
      if (weirdnessConstraint !== undefined) {
        coverPayload.weirdnessConstraint = weirdnessConstraint;
      }
      if (audioWeight !== undefined) {
        coverPayload.audioWeight = audioWeight;
      }
      if (negativeTags) {
        coverPayload.negativeTags = negativeTags;
      }

      console.log('Sending to KIE.ai upload-cover:', JSON.stringify(coverPayload, null, 2));

      // Call KIE.ai upload-cover SUNO API
      const sunoResponse = await fetch('https://api.kie.ai/api/v1/generate/upload-cover', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sunoApiKey}`
        },
        body: JSON.stringify(coverPayload)
      });

      if (!sunoResponse.ok) {
        const errorData = await sunoResponse.json().catch(() => ({}));
        console.error('KIE.ai upload-cover API error:', errorData);
        return res.status(sunoResponse.status).json({
          error: 'SUNO upload-cover API error',
          details: errorData.msg || errorData.message || sunoResponse.statusText
        });
      }

      const sunoData = await sunoResponse.json();
      console.log('KIE.ai upload-cover response:', JSON.stringify(sunoData, null, 2));
      
      // KIE.ai returns { code: 200, msg: "success", data: { taskId: "xxx" } }
      if (sunoData.code === 200) {
        res.json({
          taskId: sunoData.data.taskId,
          status: 'processing',
          message: 'Audio cover generation started. Check status with task ID.'
        });
      } else {
        res.status(500).json({
          error: 'Upload-cover generation failed',
          details: sunoData.msg || 'Unknown error'
        });
      }

    } catch (error: any) {
      console.error('Upload-cover error:', error);
      res.status(500).json({ 
        error: 'Failed to cover audio',
        details: error.message 
      });
    }
  });

  // Get music generation status (for KIE.ai polling)
  app.get("/api/music-status/:taskId", async (req, res) => {
    try {
      const { taskId } = req.params;
      const sunoApiKey = process.env.SUNO_API_KEY;

      if (!sunoApiKey) {
        return res.status(500).json({ error: 'API key not configured' });
      }

      const response = await fetch(`https://api.kie.ai/api/v1/get?ids=${taskId}`, {
        headers: {
          'Authorization': `Bearer ${sunoApiKey}`
        }
      });

      const data = await response.json();
      
      // Format response for frontend
      if (data.code === 200 && data.data && data.data.length > 0) {
        const tracks = data.data.map((track: any) => ({
          id: track.id,
          title: track.title,
          audioUrl: track.audio_url,
          streamAudioUrl: track.stream_audio_url,
          imageUrl: track.image_url,
          status: track.status
        }));

        res.json({
          status: data.data[0].status,
          tracks: tracks
        });
      } else {
        res.json({ status: 'pending', tracks: [] });
      }

    } catch (error: any) {
      console.error('Status check error:', error);
      res.status(500).json({ error: error.message });
    }
  });

  // User preferences route
  app.get("/api/user/preferences", isAuthenticated, async (req, res) => {
    try {
      const userId = (req as any).user?.claims?.sub;
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
  app.post("/api/user/preferences", isAuthenticated, async (req, res) => {
    try {
      const userId = (req as any).user?.claims?.sub;
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

  // Configure multer for audio file uploads (in-memory)
  const upload = multer({
    storage: multer.memoryStorage(),
    limits: {
      fileSize: 10 * 1024 * 1024, // 10MB max
    },
    fileFilter: (req, file, cb) => {
      const allowedMimeTypes = ['audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/m4a', 'audio/ogg', 'audio/flac', 'audio/x-m4a'];
      if (allowedMimeTypes.includes(file.mimetype) || file.originalname.match(/\.(mp3|wav|m4a|ogg|flac)$/i)) {
        cb(null, true);
      } else {
        cb(new Error('Invalid file type. Only audio files are allowed.'));
      }
    }
  });

  // Upload audio file endpoint
  app.post("/api/upload-audio", upload.single('audio'), async (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({
          error: 'No file uploaded',
          details: 'Please select an audio file to upload'
        });
      }

      const userId = (req as any).user?.claims?.sub || null;

      // Convert buffer to base64
      const base64Audio = req.file.buffer.toString('base64');

      // Store in database
      const [newAudio] = await db.insert(uploadedAudio).values({
        fileName: req.file.originalname,
        mimeType: req.file.mimetype,
        fileSize: req.file.size.toString(),
        audioData: base64Audio,
        userId: userId,
      }).returning();

      // Return public URL for accessing the audio
      const publicUrl = `${req.protocol}://${req.get('host')}/api/audio/${newAudio.id}`;

      res.json({
        success: true,
        url: publicUrl,
        id: newAudio.id,
        fileName: newAudio.fileName,
        fileSize: newAudio.fileSize
      });

    } catch (error: any) {
      console.error('Audio upload error:', error);
      res.status(500).json({
        error: 'Failed to upload audio',
        details: error.message
      });
    }
  });

  // Serve audio file by ID
  app.get("/api/audio/:id", async (req, res) => {
    try {
      const { id } = req.params;

      const [audio] = await db.select().from(uploadedAudio).where(eq(uploadedAudio.id, id));

      if (!audio) {
        return res.status(404).json({
          error: 'Audio file not found'
        });
      }

      // Convert base64 back to buffer
      const audioBuffer = Buffer.from(audio.audioData, 'base64');

      // Set appropriate headers
      res.set({
        'Content-Type': audio.mimeType,
        'Content-Length': audioBuffer.length,
        'Content-Disposition': `inline; filename="${audio.fileName}"`,
        'Cache-Control': 'public, max-age=31536000', // Cache for 1 year
      });

      res.send(audioBuffer);

    } catch (error: any) {
      console.error('Audio serve error:', error);
      res.status(500).json({
        error: 'Failed to serve audio',
        details: error.message
      });
    }
  });

  const httpServer = createServer(app);

  return httpServer;
}
