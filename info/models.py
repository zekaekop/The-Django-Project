from django.db import models
from django.urls import reverse

# Create your models here.

class ContactInfo(models.Model):
    user = models.ForeignKey('auth.User' ,null=True,blank=True,verbose_name="OP", on_delete=models.CASCADE)
    
    name = models.CharField(max_length=200,verbose_name="Name")
    surname = models.CharField(max_length=200,verbose_name="Surname")
    
    select_gender = (
        ('Other', 'Other'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    user_gender = models.CharField(max_length=8, choices=select_gender, default="other")

    adress = models.CharField(max_length=200,verbose_name="Adress")
    email = models.EmailField(verbose_name="Email")        
    
    def get_delete_contact_adminpanel_url(self):
        return reverse('admin_panel:delete_contact_adminpanel', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)

    def get_modify_contact_adminpanel_url(self):
        return reverse('admin_panel:modify_contact_adminpanel', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)