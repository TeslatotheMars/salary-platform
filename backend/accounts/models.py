from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Person(models.Model):
    user_id = models.BigAutoField(primary_key=True)  # global incremental ID
    email = models.EmailField(null=True, blank=True)  # optional for imported persons
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Person({self.user_id})"

class AccountManager(BaseUserManager):
    def create_user(self, email: str, password: str | None = None, role: str = "USER"):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)

        with transaction.atomic():
            person = Person.objects.create(email=email)
            account = self.model(user_id=person, email=email, role=role, is_active=True)
            account.set_password(password)
            account.save(using=self._db)
        return account

    def create_superuser(self, email: str, password: str):
        user = self.create_user(email=email, password=password, role="ADMIN")
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    # user_id is also FK to Person; primary key via OneToOneField
    user_id = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True, related_name="account")
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=16, default="USER")  # USER|ADMIN

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # needed for Django admin
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def uid(self) -> int:
        return int(self.user_id_id)  # Person.user_id
