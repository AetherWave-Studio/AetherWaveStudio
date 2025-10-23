import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Sparkles, Zap, Crown, Check } from "lucide-react";
import { useLocation } from "wouter";
import type { CreditBundle } from "@shared/schema";
import { apiRequest } from "@/lib/queryClient";

interface CreditBundlesModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function CreditBundlesModal({ open, onOpenChange }: CreditBundlesModalProps) {
  const [, setLocation] = useLocation();
  const [bundles, setBundles] = useState<CreditBundle[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (open) {
      apiRequest("GET", "/api/credit-bundles")
        .then((data: any) => {
          setBundles(data.bundles || []);
          setIsLoading(false);
        })
        .catch(() => {
          setIsLoading(false);
        });
    }
  }, [open]);

  const handleBundleSelect = (bundleId: string) => {
    setLocation(`/checkout?bundle=${bundleId}`);
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto" data-testid="dialog-credit-bundles">
        <DialogHeader>
          <DialogTitle className="text-2xl flex items-center gap-2">
            <Zap className="w-6 h-6 text-primary" />
            Purchase Credits
          </DialogTitle>
          <DialogDescription>
            Get more credits to continue creating. Buy credits once or subscribe for unlimited access.
          </DialogDescription>
        </DialogHeader>

        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full" />
          </div>
        ) : (
          <div className="space-y-6">
            {/* Credit Bundles */}
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-primary" />
                One-Time Credit Bundles
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {bundles.map((bundle) => {
                  const totalCredits = bundle.credits + (bundle.bonus || 0);
                  const pricePerCredit = (bundle.priceUSD / totalCredits).toFixed(3);
                  
                  return (
                    <Card 
                      key={bundle.id} 
                      className={`hover-elevate relative ${bundle.popular ? 'border-primary border-2' : ''}`}
                      data-testid={`card-bundle-${bundle.id}`}
                    >
                      {bundle.popular && (
                        <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground text-xs font-bold px-3 py-1 rounded-full">
                          POPULAR
                        </div>
                      )}
                      <CardContent className="p-6 space-y-4">
                        <div className="space-y-2">
                          <h4 className="font-bold text-xl">{bundle.name}</h4>
                          <div className="flex items-baseline gap-1">
                            <span className="text-3xl font-bold">${bundle.priceUSD}</span>
                          </div>
                          <p className="text-sm text-muted-foreground">
                            ${pricePerCredit} per credit
                          </p>
                        </div>

                        <div className="space-y-2">
                          <div className="flex items-center gap-2 text-sm">
                            <Check className="w-4 h-4 text-primary" />
                            <span>{bundle.credits} credits</span>
                          </div>
                          {bundle.bonus && (
                            <div className="flex items-center gap-2 text-sm text-primary font-medium">
                              <Sparkles className="w-4 h-4" />
                              <span>+ {bundle.bonus} bonus credits</span>
                            </div>
                          )}
                          <div className="flex items-center gap-2 text-sm font-semibold">
                            <Crown className="w-4 h-4 text-primary" />
                            <span>{totalCredits} total credits</span>
                          </div>
                        </div>

                        <Button 
                          className="w-full" 
                          onClick={() => handleBundleSelect(bundle.id)}
                          variant={bundle.popular ? "default" : "outline"}
                          data-testid={`button-select-${bundle.id}`}
                        >
                          Purchase Now
                        </Button>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </div>

            {/* Subscription Options */}
            <div className="border-t pt-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Crown className="w-5 h-5 text-primary" />
                Or Subscribe for Unlimited
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="hover-elevate">
                  <CardContent className="p-6 space-y-4">
                    <div>
                      <h4 className="font-bold text-lg">Studio</h4>
                      <p className="text-2xl font-bold mt-2">$20<span className="text-sm text-muted-foreground">/mo</span></p>
                    </div>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        Unlimited music generation
                      </li>
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        All music models (V5)
                      </li>
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        WAV conversion
                      </li>
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        Commercial license
                      </li>
                    </ul>
                    <Button className="w-full" variant="outline" disabled>
                      Coming Soon
                    </Button>
                  </CardContent>
                </Card>

                <Card className="hover-elevate border-primary border-2">
                  <CardContent className="p-6 space-y-4">
                    <div>
                      <div className="bg-primary text-primary-foreground text-xs font-bold px-2 py-1 rounded-md inline-block mb-2">
                        BEST VALUE
                      </div>
                      <h4 className="font-bold text-lg">Creator</h4>
                      <p className="text-2xl font-bold mt-2">$35<span className="text-sm text-muted-foreground">/mo</span></p>
                    </div>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        Everything in Studio
                      </li>
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        100 media credits/month
                      </li>
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        Video & image generation
                      </li>
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        Priority support
                      </li>
                    </ul>
                    <Button className="w-full" disabled>
                      Coming Soon
                    </Button>
                  </CardContent>
                </Card>

                <Card className="hover-elevate">
                  <CardContent className="p-6 space-y-4">
                    <div>
                      <h4 className="font-bold text-lg">All Access</h4>
                      <p className="text-2xl font-bold mt-2">$50<span className="text-sm text-muted-foreground">/mo</span></p>
                    </div>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        Everything in Creator
                      </li>
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        Unlimited everything
                      </li>
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        4K video generation
                      </li>
                      <li className="flex items-center gap-2">
                        <Check className="w-4 h-4 text-primary" />
                        API access
                      </li>
                    </ul>
                    <Button className="w-full" variant="outline" disabled>
                      Coming Soon
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
