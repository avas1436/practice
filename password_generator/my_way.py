import secrets
import string
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class PasswordGenerator(BaseModel):
    pas_type: Optional[Literal["digit", "letter", "mixed", "mix with symbols"]] = Field(
        default="mixed", description="you can choose three ways to generate password"
    )

    @field_validator("pas_type", mode="before")
    def normalize_pas_type(cls, v):
        if isinstance(v, str):
            return v.lower().strip()
        return v

    length: int = Field(default=10, description="determine the length of password")

    @property
    def password(self):
        if self.pas_type == "digit":
            characters = string.digits
        elif self.pas_type == "letter":
            characters = string.ascii_letters
        elif self.pas_type == "mixed":
            characters = string.ascii_letters + string.digits
        elif self.pas_type == "mix with symbols":
            characters = string.punctuation + string.ascii_letters + string.digits
        return "".join(secrets.choice(characters) for _ in range(self.length))


t = PasswordGenerator(pas_type="mix with symbols")
print(t.password)
