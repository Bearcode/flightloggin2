from django.contrib.sitemaps import Sitemap
from models import Plane

class TailnumberSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        p = Plane.objects\
                    .values_list('tailnumber', flat=True)\
                    .order_by()\
                    .distinct()
        
        p = [x.upper() for x in p]
        
        return p
    
    def location(self, item):
        item = item.replace(' ','')
        from django.core.urlresolvers import reverse
        try:
            return reverse("profile-tailnumber", kwargs={"pk": item})
        except:
            return ""
        

class TypeSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        p = Plane.objects\
                    .values_list('type', flat=True)\
                    .order_by()\
                    .distinct()
        
        p = [x.upper() for x in p]
        
        return p
    
    def location(self, item):
        item = item.replace(' ','')
        from django.core.urlresolvers import reverse
        try:
            return reverse("profile-type", kwargs={"pk": item})
        except:
            return ""
