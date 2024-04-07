from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile



User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='ntnulogo3.jpg')    
    location = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        # Open the uploaded image using PIL
        img = Image.open(self.profileimg)
        
        img = img.convert('RGB')

        # Calculate the new dimensions for cropping
        width, height = img.size
        if width > height:
            new_width = height
            new_height = height
        else:
            new_width = width
            new_height = width

        # Crop the image to the new dimensions
        left = (width - new_width) // 2
        top = (height - new_height) // 2
        right = left + new_width
        bottom = top + new_height
        img = img.crop((left, top, right, bottom))

        # Resize the image to a maximum size if desired
        max_size = (800, 800)  # Set your desired maximum size here
        img.thumbnail(max_size, Image.LANCZOS)

        # Save the modified image back to the original field
        output_io = BytesIO()
        img.save(output_io, format='JPEG')

        # Set the modified image data to the profileimg field
        self.profileimg = InMemoryUploadedFile(
            output_io,
            None,
            f'{self.profileimg.name.split(".")[0]}.jpg',
            'image/jpeg',
            output_io.tell,
            None
        )

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        # Open the uploaded image using PIL
        img = Image.open(self.image)
        
        img = img.convert('RGB')

        # Calculate the new dimensions for cropping
        width, height = img.size
        if width > height:
            new_width = height
            new_height = height
        else:
            new_width = width
            new_height = width

        # Crop the image to the new dimensions
        left = (width - new_width) // 2
        top = (height - new_height) // 2
        right = left + new_width
        bottom = top + new_height
        img = img.crop((left, top, right, bottom))

        # Resize the image to a maximum size if desired
        max_size = (800, 800)  # Set your desired maximum size here
        img.thumbnail(max_size, Image.LANCZOS)

        # Save the modified image back to the original field
        output_io = BytesIO()
        img.save(output_io, format='JPEG')

        # Set the modified image data to the image field
        self.image = InMemoryUploadedFile(
            output_io,
            None,
            f'{self.image.name.split(".")[0]}.jpg',
            'image/jpeg',
            output_io.tell,
            None
        )

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user + " | " + self.caption


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username + " | " + self.post_id 


class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    
    def __str__(self):
        return  self.follower + " -> " +self.user
    