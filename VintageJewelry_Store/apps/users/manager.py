from django.contrib.auth.base_user import BaseUserManager


class ShopUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password,
                    is_superuser=False, is_admin=False, is_active=False,
                    **other_fields):
        if not email:
            raise ValueError("User must have a unique email")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            is_admin=is_admin,
            is_active=is_active,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password,
                        **other_fields):
        user = self.create_user(email, first_name, last_name, password,
                    is_superuser=True, is_admin=True, is_active=True,
                     **other_fields)
        return user

    def create_staff(self, email, first_name, last_name, password,
                    **other_fields):
        user = self.create_user(email, first_name, last_name, password,
                    is_superuser=False, is_admin=True, is_active=True,
                    **other_fields)
        return user
