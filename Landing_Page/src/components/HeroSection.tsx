import { ArrowRight, Play } from 'lucide-react';
import { Button } from '@/components/ui/button';
import heroImage from '@/assets/ey-hero-main.jpg';

const HeroSection = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-primary">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0">
        <img 
          src={heroImage} 
          alt="EY Professional Consulting" 
          className="w-full h-full object-cover opacity-30"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-primary via-primary/80 to-transparent"></div>
      </div>
      
      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center lg:text-left">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8 animate-fade-up">
            <div className="space-y-4">
              <h1 className="heading-xl text-primary-foreground">
                Building a better
                <span className="block gradient-text-yellow">
                  working world
                </span>
              </h1>
              <p className="body-lg text-muted-foreground max-w-2xl">
                We help you achieve your ambitions by making business work better. 
                From assurance to consulting, from tax to transactions — we deliver 
                exceptional service that builds trust and confidence in the capital markets.
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Button size="lg" className="bg-ey-yellow hover:bg-ey-yellow-dark text-primary font-semibold group">
                Explore our services
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button 
                variant="outline" 
                size="lg" 
                className="border-primary-foreground text-primary-foreground hover:bg-primary-foreground hover:text-primary group"
              >
                <Play className="mr-2 h-5 w-5" />
                Watch our story
              </Button>
            </div>
            
            <div className="grid grid-cols-3 gap-8 pt-8 border-t border-ey-yellow/20">
              <div className="text-center lg:text-left">
                <div className="text-2xl font-bold text-ey-yellow">700k+</div>
                <div className="text-sm text-muted-foreground">People worldwide</div>
              </div>
              <div className="text-center lg:text-left">
                <div className="text-2xl font-bold text-ey-yellow">150+</div>
                <div className="text-sm text-muted-foreground">Countries served</div>
              </div>
              <div className="text-center lg:text-left">
                <div className="text-2xl font-bold text-ey-yellow">#1</div>
                <div className="text-sm text-muted-foreground">Global consulting</div>
              </div>
            </div>
          </div>
          
          {/* Additional content or imagery space */}
          <div className="hidden lg:block"></div>
        </div>
      </div>
      
      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
        <div className="w-6 h-10 border-2 border-ey-yellow rounded-full flex justify-center">
          <div className="w-1 h-3 bg-ey-yellow rounded-full mt-2 animate-bounce"></div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;