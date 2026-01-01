from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
#from django.utils.text import slugify

AUTH_USER_MODEL = 'post.User'

class Post(models.Model):
    def file_size(value): # add this to some file where you can import it from
        limit = 10 * 1024 * 1024
        if value.size > limit:
            raise ValidationError('File too large. Size should not exceed 10 MiB.')
        
    user = models.ForeignKey('auth.User', verbose_name="OP", related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=200,verbose_name="Title ")
    desc = RichTextField(verbose_name="")
    date = models.DateTimeField(verbose_name="Date/Time ", auto_now_add=True)

    image = models.ImageField(upload_to='images_uploaded', null=True, blank=True, validators=[file_size,FileExtensionValidator(allowed_extensions=['png','jpg','jpeg','webp'])])
    video = models.FileField(upload_to='videos_uploaded',null=True, blank=True, validators=[file_size,FileExtensionValidator(allowed_extensions=['mov','avi','mp4','webm','mkv'])])


    user_html = models.FileField(upload_to='html_uploaded',null=True, blank=True, validators=[file_size,FileExtensionValidator(allowed_extensions=['html'])])
    user_css = models.FileField(upload_to='css_uploaded',null=True, blank=True, validators=[file_size,FileExtensionValidator(allowed_extensions=['css'])])
    user_js =  models.FileField(upload_to='js_uploaded',null=True, blank=True, validators=[file_size,FileExtensionValidator(allowed_extensions=['js'])])

    site_preview = models.ImageField(upload_to='images_uploaded', null=True, blank=True, validators=[file_size,FileExtensionValidator(allowed_extensions=['png','jpg','jpeg','webp'])])

    upvotes = models.PositiveIntegerField(default=0)
    post_views = models.PositiveIntegerField(default=0)

    reports = models.PositiveBigIntegerField(default=0)

    staff_modified = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)

    def get_update_url(self):
        return reverse('post:update', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)

    def get_create_url(self):
        return reverse('post:create')
        #return "/user/{}".format(self.id)

    def get_delete_url(self):
        return reverse('post:delete', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)

    def get_report_url(self):
        return reverse('post:report', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)

    def get_delete_post_adminpanel_url(self):
        return reverse('admin_panel:delete_post_adminpanel', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)

    def get_delete_url_home(self):
        return reverse('home:delete_home', kwargs={'id': self.id})       # worst naming i have ever seen ... FIX IT
        #return "/user/{}".format(self.id)

    #def set_user_perms_staff_adminpanel(self):
    #    print("working2")
    #    return reverse('post:change_user_staff_perms', kwargs={'id': self.id})
    #    #return "/user/{}".format(self.id)

    #def set_user_perms_superusr_adminpanel(self):
    #    return reverse('post:change_user_superusr_perms', kwargs={'id': self.id})
    #    #return "/user/{}".format(self.id)
    
    #def get_unique_slug(self):
    #    slug = slugify(self.title.replace('ı', 'i'))
    #    unique_slug = slug
    #    counter = 1
    #    while Post.objects.filter(slug=unique_slug).exists():
    #        unique_slug = '{}-{}'.format(slug, counter)
    #        counter += 1
    #    return unique_slug

    #def save(self, *args, **kwargs):
    #    return super(Post, self).save(*args, **kwargs)
    #    self.slug = self.get_unique_slug()

    class Meta:
        ordering = ["-date","id"]

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='images_uploaded',
        validators=[Post.file_size, FileExtensionValidator(allowed_extensions=['png','jpg','jpeg','webp'])]
    )

class UserUpvote(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="upvotes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="user_upvotes")

    class Meta:
        unique_together = ("user","post")

class UserReport(models.Model): # there is probably a way better way of doing these
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="reports")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="user_reports")

    class Meta:
        unique_together = ("user","post")

class Comment(models.Model):
    post = models.ForeignKey('post.Post', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User' ,null=True,blank=True,verbose_name="OP", on_delete=models.SET_NULL)
    name = models.CharField(max_length=200,verbose_name="Name ")
    content = RichTextField(verbose_name="")
    created_date = models.DateTimeField(verbose_name="Created Date ", auto_now_add=True)
    
