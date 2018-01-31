from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

from django.utils.text import slugify
from django.db.models.signals import pre_save

from django.utils import timezone
# Create your models here.

# def upload_location(instance, filename):
#     return "%s/%s" %(instance.id, filename)

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish_date__lte=timezone.now())
        #calling super(PostManager, self) from all function, is the same as calling Post.objects.all()

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, help_text="This field will be automatically generated according to the Title")
    image = models.ImageField(upload_to="Notices",
                            default="Notices/default_notice.png", blank=True,
                            width_field="width_field",
                            height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)   #every time it's saved in the DB, updated will change
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) #when post was first added initially, like created
    draft = models.BooleanField(default=False)
    publish_date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now().today)

    objects = PostManager() # objects is the manager that we use like Post.objects.all(), could be named anything else

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})
        # return "/posts/%s/" %(self.id)
    class Meta:
        ordering = ["-timestamp", "-updated"]

 # to check for one or more same titles then create new slug base on id

def create_slug(instance, newSlug=None):
    slug = slugify(instance.title)
    if newSlug is not None:
        slug = newSlug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        newSlug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, newSlug=newSlug)
    return slug

def pre_save_postmodel_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_postmodel_reciever, sender=Post)
