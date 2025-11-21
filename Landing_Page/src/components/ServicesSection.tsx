import { ArrowRight, Shield, TrendingUp, Calculator, Briefcase, Users, Globe, Lightbulb, Target } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

const ServicesSection = () => {
  const services = [
    {
      icon: Shield,
      title: "Assurance",
      description: "Building trust and confidence in the capital markets through independent audit and assurance services.",
      color: "text-ey-yellow",
      bgColor: "bg-ey-yellow/10"
    },
    {
      icon: TrendingUp,
      title: "Consulting",
      description: "Helping organizations transform and innovate through technology, data analytics, and strategic advisory.",
      color: "text-ey-yellow",
      bgColor: "bg-ey-yellow/10"
    },
    {
      icon: Calculator,
      title: "Tax",
      description: "Comprehensive tax services to help you manage risk, comply with regulations, and improve efficiency.",
      color: "text-ey-yellow",
      bgColor: "bg-ey-yellow/10"
    },
    {
      icon: Briefcase,
      title: "Strategy and Transactions",
      description: "Supporting you through complex transactions and strategic decisions to unlock value and drive growth.",
      color: "text-ey-yellow",
      bgColor: "bg-ey-yellow/10"
    }
  ];

  const insights = [
    {
      icon: Users,
      title: "Future of Work",
      description: "How organizations can build resilient, adaptable workforces for the post-pandemic world.",
    },
    {
      icon: Globe,
      title: "ESG Excellence", 
      description: "Environmental, social and governance strategies that create sustainable value.",
    },
    {
      icon: Lightbulb,
      title: "Innovation Lab",
      description: "Cutting-edge technology solutions and digital transformation insights.",
    },
    {
      icon: Target,
      title: "CEO Outlook",
      description: "Strategic perspectives from global business leaders on growth and transformation.",
    }
  ];

  return (
    <section className="py-20 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Services */}
        <div className="text-center mb-16">
          <h2 className="heading-lg text-foreground mb-4">Our Services</h2>
          <p className="body-lg text-muted-foreground max-w-3xl mx-auto">
            We provide exceptional professional services across four key areas, helping organizations 
            navigate complexity and build confidence in their future.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-20">
          {services.map((service, index) => (
            <Card key={service.title} className="group hover:shadow-lg transition-all duration-300 border-border hover:border-ey-yellow/30">
              <CardContent className="p-8 text-center space-y-4">
                <div className={`w-16 h-16 ${service.bgColor} rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform duration-300`}>
                  <service.icon className={`w-8 h-8 ${service.color}`} />
                </div>
                <h3 className="heading-md text-foreground">{service.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{service.description}</p>
                <Button variant="ghost" className="text-ey-yellow hover:text-ey-yellow-dark group mt-4">
                  Learn more
                  <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Insights Section */}
        <div className="bg-primary rounded-2xl p-12">
          <div className="text-center mb-12">
            <h2 className="heading-lg text-primary-foreground mb-4">Latest Insights</h2>
            <p className="body-lg text-muted-foreground max-w-3xl mx-auto">
              Stay ahead with our thought leadership, research, and perspectives on the issues 
              that matter most to your business.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {insights.map((insight) => (
              <div key={insight.title} className="group cursor-pointer">
                <div className="space-y-4">
                  <div className="w-12 h-12 bg-ey-yellow/20 rounded-lg flex items-center justify-center group-hover:bg-ey-yellow/30 transition-colors duration-300">
                    <insight.icon className="w-6 h-6 text-ey-yellow" />
                  </div>
                  <h3 className="text-xl font-semibold text-primary-foreground group-hover:text-ey-yellow transition-colors duration-300">
                    {insight.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">{insight.description}</p>
                  <div className="flex items-center text-ey-yellow group-hover:translate-x-2 transition-transform duration-300">
                    <span className="text-sm font-medium">Read more</span>
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default ServicesSection;