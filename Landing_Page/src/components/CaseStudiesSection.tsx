import { ArrowRight, Star, Building2, Zap, Globe } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

const CaseStudiesSection = () => {
  const caseStudies = [
    {
      icon: Building2,
      title: "Global Financial Institution",
      challenge: "Digital transformation across 50+ markets",
      solution: "Implemented cloud-first strategy and AI-driven analytics",
      result: "40% reduction in operational costs, 60% faster processing",
      industry: "Financial Services",
      bgColor: "bg-gradient-to-br from-ey-yellow/10 to-ey-yellow/5"
    },
    {
      icon: Zap,
      title: "Technology Unicorn",
      challenge: "IPO readiness and compliance framework",
      solution: "Comprehensive audit and governance restructuring",
      result: "Successfully raised $2.1B in public markets",
      industry: "Technology",
      bgColor: "bg-gradient-to-br from-primary/10 to-primary/5"
    },
    {
      icon: Globe,
      title: "Energy Conglomerate",
      challenge: "ESG reporting and sustainability strategy",
      solution: "Integrated ESG framework with real-time monitoring",
      result: "Achieved carbon neutral status 2 years ahead of target",
      industry: "Energy & Resources",
      bgColor: "bg-gradient-to-br from-ey-yellow/10 to-ey-yellow/5"
    }
  ];

  return (
    <section className="py-20 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="heading-lg text-foreground mb-4">Success Stories</h2>
          <p className="body-lg text-muted-foreground max-w-3xl mx-auto">
            Discover how we've helped organizations across industries transform their 
            operations, manage risk, and unlock new opportunities for growth.
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          {caseStudies.map((study, index) => (
            <Card 
              key={study.title} 
              className={`group hover:shadow-xl transition-all duration-500 border-0 ${study.bgColor} hover:scale-105`}
            >
              <CardContent className="p-8 space-y-6">
                <div className="flex items-start justify-between">
                  <div className="w-12 h-12 bg-ey-yellow/20 rounded-lg flex items-center justify-center group-hover:bg-ey-yellow/30 transition-colors duration-300">
                    <study.icon className="w-6 h-6 text-ey-yellow" />
                  </div>
                  <span className="text-xs font-semibold text-ey-yellow bg-ey-yellow/10 px-3 py-1 rounded-full">
                    {study.industry}
                  </span>
                </div>
                
                <div className="space-y-4">
                  <h3 className="text-xl font-bold text-foreground group-hover:text-ey-yellow transition-colors duration-300">
                    {study.title}
                  </h3>
                  
                  <div className="space-y-3">
                    <div>
                      <h4 className="text-sm font-semibold text-foreground mb-1">Challenge</h4>
                      <p className="text-sm text-muted-foreground">{study.challenge}</p>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-semibold text-foreground mb-1">Solution</h4>
                      <p className="text-sm text-muted-foreground">{study.solution}</p>
                    </div>
                    
                    <div className="bg-ey-yellow/5 p-4 rounded-lg border-l-4 border-ey-yellow">
                      <h4 className="text-sm font-semibold text-ey-yellow mb-1">Result</h4>
                      <p className="text-sm font-medium text-foreground">{study.result}</p>
                    </div>
                  </div>
                </div>
                
                <Button variant="ghost" className="w-full text-ey-yellow hover:text-ey-yellow-dark group">
                  Read full case study
                  <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
        
        {/* Client testimonial */}
        <div className="bg-primary rounded-2xl p-12 text-center">
          
          <div className="max-w-4xl mx-auto">
            <div className="flex justify-center mb-6">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="w-6 h-6 text-ey-yellow fill-current" />
              ))}
            </div>
            <blockquote className="text-2xl font-medium text-primary-foreground mb-8 leading-relaxed">
              "EY's strategic guidance and innovative approach helped us navigate one of the most 
              complex transformations in our industry. Their team became true partners in our success."
            </blockquote>
            <div className="space-y-2">
              <div className="text-lg font-semibold text-ey-yellow">Sarah Chen</div>
              <div className="text-muted-foreground">Chief Executive Officer, TechGlobal Corp</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CaseStudiesSection;