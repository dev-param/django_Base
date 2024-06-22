from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _





class userManagers(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, mobile_number, mobile_country_code, pin,  password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not mobile_number:
            raise ValueError(_("The mobile number must be set"))
        # email = self.normalize_email(email)
        user = self.model(
            mobile_number=mobile_number,
            mobile_country_code=mobile_country_code,
            pin=pin,
            **extra_fields
            )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile_number,   pin, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        print(mobile_number)
        print(pin)
        print(password)
        mobile_country_code = '+91'
        # pin = '0000'
        extra_fields.setdefault("_staff", {"status": True})
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("_active", {"status": True})

        # if extra_fields.get("_staff").get is not True:
        #     raise ValueError(_("Superuser must have _staff=True."))
        # if extra_fields.get("_superuser") is not True:
        #     raise ValueError(_("Superuser must have _superuser=True."))
        return self.create_user(mobile_number, mobile_country_code, pin, password, **extra_fields)
    
  