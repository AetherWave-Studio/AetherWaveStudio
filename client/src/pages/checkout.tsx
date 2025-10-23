import { useStripe, Elements, PaymentElement, useElements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';
import { useEffect, useState } from 'react';
import { apiRequest, queryClient } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Check, Sparkles } from "lucide-react";
import { useLocation } from "wouter";
import type { CreditBundle } from "@shared/schema";

if (!import.meta.env.VITE_STRIPE_PUBLIC_KEY) {
  throw new Error('Missing required Stripe key: VITE_STRIPE_PUBLIC_KEY');
}
const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY);

const CheckoutForm = ({ bundle, onSuccess }: { bundle: CreditBundle; onSuccess: () => void }) => {
  const stripe = useStripe();
  const elements = useElements();
  const { toast } = useToast();
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setIsProcessing(true);

    try {
      const { error, paymentIntent } = await stripe.confirmPayment({
        elements,
        redirect: 'if_required',
        confirmParams: {
          return_url: window.location.origin,
        },
      });

      if (error) {
        toast({
          title: "Payment Failed",
          description: error.message,
          variant: "destructive",
        });
        setIsProcessing(false);
      } else if (paymentIntent && paymentIntent.status === 'succeeded') {
        // Manually confirm the payment to add credits
        try {
          await apiRequest("POST", "/api/confirm-payment", { 
            paymentIntentId: paymentIntent.id 
          });
          
          // Invalidate credits cache to refresh balance
          queryClient.invalidateQueries({ queryKey: ['/api/user/credits'] });
          
          toast({
            title: "Purchase Successful!",
            description: `${bundle.credits + (bundle.bonus || 0)} credits added to your account!`,
          });
          
          onSuccess();
        } catch (confirmError: any) {
          toast({
            title: "Payment Succeeded, Credits Pending",
            description: "Your payment was successful. Credits will be added shortly.",
          });
          onSuccess();
        }
      }
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.message || "An unexpected error occurred",
        variant: "destructive",
      });
      setIsProcessing(false);
    }
  };

  const totalCredits = bundle.credits + (bundle.bonus || 0);

  return (
    <form onSubmit={handleSubmit} className="space-y-6" data-testid="form-checkout">
      <div className="rounded-lg border bg-card p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-lg">{bundle.name}</h3>
            <p className="text-sm text-muted-foreground">
              {bundle.credits} credits
              {bundle.bonus && <span className="text-primary"> + {bundle.bonus} bonus</span>}
            </p>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold">${bundle.priceUSD}</p>
            <p className="text-sm text-muted-foreground">{totalCredits} total credits</p>
          </div>
        </div>
        
        {bundle.bonus && (
          <div className="flex items-center gap-2 text-sm text-primary">
            <Sparkles className="w-4 h-4" />
            <span className="font-medium">{bundle.bonus} bonus credits included!</span>
          </div>
        )}
      </div>

      <PaymentElement />
      
      <Button 
        type="submit" 
        disabled={!stripe || isProcessing} 
        className="w-full"
        size="lg"
        data-testid="button-complete-purchase"
      >
        {isProcessing ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Processing Payment...
          </>
        ) : (
          <>
            <Check className="mr-2 h-4 w-4" />
            Complete Purchase - ${bundle.priceUSD}
          </>
        )}
      </Button>
    </form>
  );
};

export default function Checkout() {
  const [, setLocation] = useLocation();
  const [clientSecret, setClientSecret] = useState("");
  const [bundle, setBundle] = useState<CreditBundle | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Get bundleId from URL query params
    const params = new URLSearchParams(window.location.search);
    const bundleId = params.get('bundle');

    if (!bundleId) {
      setError('No bundle selected');
      setIsLoading(false);
      return;
    }

    // Create PaymentIntent
    apiRequest("POST", "/api/create-payment-intent", { bundleId })
      .then((data: any) => {
        setClientSecret(data.clientSecret);
        setBundle(data.bundle);
        setIsLoading(false);
      })
      .catch((err) => {
        setError(err.message || 'Failed to initialize checkout');
        setIsLoading(false);
      });
  }, []);

  const handleSuccess = () => {
    setTimeout(() => {
      setLocation('/');
    }, 2000);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="flex flex-col items-center justify-center p-12">
            <Loader2 className="h-8 w-8 animate-spin text-primary mb-4" />
            <p className="text-muted-foreground">Initializing checkout...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error || !clientSecret || !bundle) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Checkout Error</CardTitle>
            <CardDescription>{error || 'Failed to initialize checkout'}</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => setLocation('/')} className="w-full" data-testid="button-back-home">
              Back to Home
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-background">
      <Card className="w-full max-w-lg">
        <CardHeader>
          <CardTitle>Purchase Credits</CardTitle>
          <CardDescription>
            Secure payment powered by Stripe
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Elements stripe={stripePromise} options={{ clientSecret }}>
            <CheckoutForm bundle={bundle} onSuccess={handleSuccess} />
          </Elements>
        </CardContent>
      </Card>
    </div>
  );
}
