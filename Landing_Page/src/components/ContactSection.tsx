import { useState } from 'react';
import { ArrowRight, Mail, Phone, MapPin, Clock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent } from '@/components/ui/card';

const ContactSection = () => {
  // State for the form fields
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    company: '',
    message: ''
  });

  // Data for the interactive contact cards (unchanged)
  const contactInfo = [
    {
      icon: Mail,
      title: "Email us",
      content: "contact@ey.com",
      description: "Get in touch with our team",
      href: "mailto:contact@ey.com"
    },
    {
      icon: Phone,
      title: "Call us",
      content: "+91 (555) 123-4567",
      description: "Speak with an advisor",
      href: "tel:+15551234567"
    },
    {
      icon: MapPin,
      title: "Visit us",
      content: "Global Headquarters",
      description: "London, New York, Singapore",
      href: `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent('London, New York, Singapore')}`
    },
    {
      icon: Clock,
      title: "Business hours",
      content: "24/7 Global Support",
      description: "We're here when you need us",
      href: "#"
    }
  ];

  // Handler to update form state on input change (unchanged)
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  // This function now saves data to localStorage and triggers a download.
  const handleSubmit = (e) => {
    e.preventDefault();

    // 1. Get existing submissions from the browser's local storage.
    // If none exist, start with an empty array.
    const existingSubmissions = JSON.parse(localStorage.getItem('contactSubmissions')) || [];

    // 2. Add the new form data to the array.
    const updatedSubmissions = [...existingSubmissions, formData];

    // 3. Save the updated array back to local storage for the next submission.
    localStorage.setItem('contactSubmissions', JSON.stringify(updatedSubmissions));

    // 4. Create a JSON file in memory to be downloaded.
    const jsonString = JSON.stringify(updatedSubmissions, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });

    // 5. Create a temporary link to trigger the download.
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'contact-submissions.json'; // The name of the downloaded file
    document.body.appendChild(link);
    link.click(); // Click the link to start the download
    document.body.removeChild(link); // Clean up by removing the link
    URL.revokeObjectURL(link.href); // Free up browser memory

    // 6. Give the user feedback and reset the form.
    alert('Submission saved! Check your downloads for the "contact-submissions.json" file.');
    setFormData({
      firstName: '',
      lastName: '',
      email: '',
      company: '',
      message: ''
    });
  };
//End of the Send Message action button 

  return (
    // The JSX for the component's appearance is completely unchanged
    <section className="py-20 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
          {/* Contact Form */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h2 className="heading-lg text-foreground">Let's start a conversation</h2>
              <p className="body-lg text-muted-foreground">
                Ready to transform your business? Our experts are here to help you 
                navigate complexity and unlock new opportunities.
              </p>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input 
                  placeholder="First name"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleInputChange}
                  className="border-border focus:border-ey-yellow focus:ring-ey-yellow/20"
                />
                <Input 
                  placeholder="Last name"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleInputChange}
                  className="border-border focus:border-ey-yellow focus:ring-ey-yellow/20"
                />
              </div>
              
              <Input 
                type="email" 
                placeholder="Email address"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="border-border focus:border-ey-yellow focus:ring-ey-yellow/20"
              />
              
              <Input 
                placeholder="Company"
                name="company"
                value={formData.company}
                onChange={handleInputChange}
                className="border-border focus:border-ey-yellow focus:ring-ey-yellow/20"
              />
              
              <Textarea 
                placeholder="Tell us about your challenge or opportunity"
                name="message"
                value={formData.message}
                onChange={handleInputChange}
                rows={5}
                className="border-border focus:border-ey-yellow focus:ring-ey-yellow/20 resize-none"
              />
              
              <Button 
                type="submit" 
                size="lg" 
                className="w-full bg-ey-yellow hover:bg-ey-yellow-dark text-primary font-semibold group"
              >
                Send message
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Button>
            </form>
            
            <div className="text-sm text-muted-foreground">
              By submitting this form, you acknowledge that EY may contact you about 
              its services and that this communication is subject to EY's privacy policy.
            </div>
          </div>
          
          {/* Contact Information */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h3 className="heading-md text-foreground">Get in touch</h3>
              <p className="text-muted-foreground">
                Choose the best way to reach us. Our global team is ready to support 
                your business needs around the clock.
              </p>
            </div>
            
            <div className="grid grid-cols-1 gap-6">
              {contactInfo.map((item) => (
                <a 
                  key={item.title} 
                  href={item.href} 
                  target="_blank"
                  rel="noopener noreferrer"
                  className="focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ey-yellow rounded-lg"
                >
                  <Card className="group h-full hover:shadow-lg transition-all duration-300 border-border hover:border-ey-yellow/30 cursor-pointer">
                    <CardContent className="p-6">
                      <div className="flex items-start space-x-4">
                        <div className="w-12 h-12 bg-ey-yellow/10 rounded-lg flex items-center justify-center group-hover:bg-ey-yellow/20 transition-colors duration-300">
                          <item.icon className="w-6 h-6 text-ey-yellow" />
                        </div>
                        <div className="space-y-1">
                          <h4 className="font-semibold text-foreground">{item.title}</h4>
                          <p className="font-medium text-ey-yellow">{item.content}</p>
                          <p className="text-sm text-muted-foreground">{item.description}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                  
                </a>
              ))}
            </div>
            
            <Card className="bg-primary border-ey-yellow/20">
              <CardContent className="p-8 text-center space-y-4">
                <h4 className="text-xl font-semibold text-primary-foreground">
                  Need immediate assistance?
                </h4>
                <p className="text-muted-foreground">
                  Our crisis management team is available 24/7 to help with 
                  urgent business matters.
                </p>
                <Button 
                  variant="outline" 
                  className="border-ey-yellow text-ey-yellow hover:bg-ey-yellow hover:text-primary"
                >
                  Emergency contact
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;