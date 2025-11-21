import { ArrowUp, Linkedin, Twitter, Facebook, Youtube } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Footer = () => {
  const footerSections = [
    {
      title: "Services",
      links: ["Assurance", "Consulting", "Tax", "Strategy and Transactions", "Managed Services"]
    },
    {
      title: "Industries", 
      links: ["Financial Services", "Technology", "Energy & Resources", "Healthcare", "Consumer Products"]
    },
    {
      title: "Insights",
      links: ["CEO Outlook", "Future of Work", "ESG", "Digital Transformation", "Megatrends"]
    },
    {
      title: "About EY",
      links: ["Our purpose", "Leadership", "Careers", "Sustainability", "Investor relations"]
    }
  ];

  const socialLinks = [
    { icon: Linkedin, href: "https://www.linkedin.com/company/ernstandyoung/", label: "LinkedIn" },
    { icon: Twitter, href: "https://x.com/EY_India?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor", label: "Twitter" },
    { icon: Facebook, href: "https://www.facebook.com/EY/", label: "Facebook" },
    { icon: Youtube, href: "https://www.youtube.com/ernstandyoungglobal", label: "YouTube" }
  ];

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="bg-primary text-primary-foreground">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Main Footer Content */}
        <div className="py-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          {/* Brand Section */}
          <div className="lg:col-span-1 space-y-6">
            <div>
              <div className="text-3xl font-bold text-ey-yellow mb-2">EY</div>
              <p className="text-sm text-muted-foreground">Building a better working world</p>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              EY exists to build a better working world — helping create long-term value for 
              clients, people and society and build trust in the capital markets.
            </p>
            <div className="flex space-x-4">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  className="w-10 h-10 bg-ey-yellow/10 hover:bg-ey-yellow hover:text-primary rounded-full flex items-center justify-center transition-all duration-300 group"
                  aria-label={social.label}
                >
                  <social.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Footer Links */}
          {footerSections.map((section) => (
            <div key={section.title} className="space-y-4">
              <h4 className="font-semibold text-ey-yellow">{section.title}</h4>
              <ul className="space-y-3">
                {section.links.map((link) => (
                  <li key={link}>
                    <a 
                      href="#" 
                      className="text-sm text-muted-foreground hover:text-ey-yellow transition-colors duration-200"
                    >
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Newsletter Section */}
        <div className="border-t border-ey-yellow/20 py-12">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-primary-foreground">
                Stay informed with EY insights
              </h3>
              <p className="text-muted-foreground">
                Get the latest thought leadership, research, and perspectives delivered to your inbox.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-4 py-3 bg-background text-foreground rounded-lg border border-border focus:border-ey-yellow focus:outline-none focus:ring-2 focus:ring-ey-yellow/20 transition-colors"
              />
              <Button className="bg-ey-yellow hover:bg-ey-yellow-dark text-primary font-semibold">
                Subscribe
              </Button>
            </div>
          </div>
        </div>

        {/* Bottom Footer */}
        <div className="border-t border-ey-yellow/20 py-8 flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div className="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-6 text-sm text-muted-foreground">
            <span>© 2024 Ernst & Young Global Limited. All rights reserved.</span>
            <div className="flex space-x-4">
              <a href="#" className="hover:text-ey-yellow transition-colors">Privacy</a>
              <a href="#" className="hover:text-ey-yellow transition-colors">Terms</a>
              <a href="#" className="hover:text-ey-yellow transition-colors">Cookies</a>
            </div>
          </div>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={scrollToTop}
            className="text-ey-yellow hover:text-ey-yellow-dark hover:bg-ey-yellow/10 group"
          >
            Back to top
            <ArrowUp className="ml-2 h-4 w-4 group-hover:-translate-y-1 transition-transform" />
          </Button>
        </div>
      </div>
    </footer>
  );
};

export default Footer;