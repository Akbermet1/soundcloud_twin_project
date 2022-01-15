from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from .utils import generate_activation_code


class UserManager(BaseUserManager):
    def _create(self, email, username, age, password, avatar, background_image, **extra_fields):
        if not email:
            raise ValueError('Please, enter your email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, age=age, password=password, avatar=avatar, background_image=background_image, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, age, password, avatar, background_image, **extra_fields):
        user = self._create(email, username, age, password, avatar, background_image,**extra_fields)
        user.is_active = True
        user.is_staff = True
        user.save()
        return user

    def create_user(self, email, username, age, password, avatar=None, background_image=None, **extra_fields):
        return self._create(email, username, age, password, avatar, background_image, **extra_fields)



class User(AbstractBaseUser):
    email = models.EmailField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    age = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    activation_code = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='users_avatars', blank=True, null=True)
    background_image = models.ImageField(upload_to='background_images', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'age']
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def assign_activation_code(self):
        code = generate_activation_code()
        if User.objects.filter(activation_code=code).exists():
            self.assign_activation_code()
        self.activation_code = code
        self.save()

    def send_activation_email(self, action):
        from django.core.mail import send_mail
        # action can be account activation a passwordr restoration
        if action.lower() == 'register':
            subject = 'Account activation'
            ''' CHECk ThIS ACTIVATION URL'''
            message = f'Follow this link to finalize your registration:\nhttp://localhost:8000/account/activate/{self.activation_code}/'
        else:
            subject = 'Password change'
            # this is not the final version of the message
            # message = f'This is your confirmation code: {self.activation_code}'

        send_mail(
            subject,
            message,
            'shop_staff@gmail.com',
            [self.email]
        )

