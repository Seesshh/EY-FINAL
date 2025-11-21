import { useState } from 'react';
import { Menu, X, ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Navigation = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navItems = [
    { 
      name: 'Services', 
      hasDropdown: true,
      items: ['Assurance', 'Consulting', 'Tax', 'Strategy and Transactions']
    },
    { 
      name: 'Industries', 
      hasDropdown: true,
      items: ['Financial Services', 'Technology', 'Energy', 'Healthcare']
    },
    { name: 'Insights', hasDropdown: false },
    { name: 'Careers', hasDropdown: false },
    { name: 'About EY', hasDropdown: false },
  ];

  return (
    <nav className="fixed top-0 w-full z-50 bg-primary/95 backdrop-blur-sm border-b border-ey-yellow/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="text-2xl font-bold">
              <span className="text-ey-yellow">EY</span>
              <span className="text-primary-foreground ml-2 text-sm">Building a better working world</span>
            </div>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <div key={item.name} className="relative group">
                <button className="flex items-center space-x-1 text-primary-foreground hover:text-ey-yellow transition-colors duration-200">
                  <span>{item.name}</span>
                  {item.hasDropdown && <ChevronDown size={16} />}
                </button>
                
                {item.hasDropdown && (
                  <div className="absolute top-full left-0 mt-2 w-64 bg-primary border border-ey-yellow/20 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300">
                    <div className="py-2">
                      {item.items?.map((subItem) => (
                        <a
                          key={subItem}
                          href="#"
                          className="block px-4 py-2 text-primary-foreground hover:bg-ey-yellow/10 hover:text-ey-yellow transition-colors duration-200"
                        >
                          {subItem}
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
            
            <Button variant="outline" className="border-ey-yellow text-ey-yellow hover:bg-ey-yellow hover:text-primary">
              Contact us
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-primary-foreground hover:text-ey-yellow transition-colors"
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-ey-yellow/20">
            <div className="py-4 space-y-4">
              {navItems.map((item) => (
                <div key={item.name}>
                  <button className="block w-full text-left text-primary-foreground hover:text-ey-yellow transition-colors py-2">
                    {item.name}
                  </button>
                  {item.hasDropdown && (
                    <div className="ml-4 mt-2 space-y-2">
                      {item.items?.map((subItem) => (
                        <a
                          key={subItem}
                          href="#"
                          className="block text-sm text-muted-foreground hover:text-ey-yellow transition-colors py-1"
                        >
                          {subItem}
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              ))}
              <Button variant="outline" className="w-full border-ey-yellow text-ey-yellow hover:bg-ey-yellow hover:text-primary mt-4">
                Contact us
              </Button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;