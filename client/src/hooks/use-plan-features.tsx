import { useQuery } from "@tanstack/react-query";
import { 
  PLAN_FEATURES, 
  getAllowedOptions,
  type PlanType,
  type VideoResolution,
  type ImageEngine,
  type MusicModel
} from "@shared/schema";

interface User {
  planType: PlanType;
  credits: number;
}

export function usePlanFeatures() {
  const { data: user } = useQuery<User>({
    queryKey: ["/api/auth/user"],
  });

  const planType = (user?.planType || 'free') as PlanType;
  const features = PLAN_FEATURES[planType];

  return {
    planType,
    features,
    isPaid: planType !== 'free',
    
    // Helper functions to get allowed options
    getAllowedVideoResolutions: () => getAllowedOptions<VideoResolution>(planType, 'videoResolutions'),
    getAllowedImageEngines: () => getAllowedOptions<ImageEngine>(planType, 'imageEngines'),
    getAllowedMusicModels: () => getAllowedOptions<MusicModel>(planType, 'musicModels'),
    
    // Helper functions to check if specific option is allowed
    isVideoResolutionAllowed: (resolution: VideoResolution) => 
      features.allowedVideoResolutions.includes(resolution),
    isImageEngineAllowed: (engine: ImageEngine) => 
      features.allowedImageEngines.includes(engine),
    isMusicModelAllowed: (model: MusicModel) => 
      features.allowedMusicModels.includes(model),
      
    // Get required plan for restricted features
    getRequiredPlan: (feature: 'video' | 'image' | 'music' | 'commercial' | 'api') => {
      if (feature === 'api') return 'All Access';
      if (feature === 'commercial') return 'Studio';
      if (feature === 'video' || feature === 'image') return 'Creator';
      return 'Studio';
    },
  };
}
