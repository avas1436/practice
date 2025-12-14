from typing import ClassVar
import string
import secrets
from pydantic import BaseModel, Field, field_validator

# مدل پایه که منطق تولید و اعتبارسنجی را نگه می‌دارد
class PasswordGeneratorBase(BaseModel):
    # فیلد سطح کلاس برای مجموعه کاراکترهای مجاز؛ ClassVar به Pydantic می‌گوید این فیلد متعلق به کلاس است
    letters: ClassVar[str] = Field(default=..., description="Allowed characters for this generator")
    # حداقل طول قابل تنظیم برای نمونه‌ها
    min_length: int = Field(default=1, description="Minimum allowed password length")
    # حداکثر طول قابل تنظیم برای نمونه‌ها
    max_length: int = Field(default=1024, description="Maximum allowed password length")

    # اعتبارسنجی جدید Pydantic v2: field_validator برای فیلدهای min_length و max_length
    @field_validator("min_length", "max_length", mode="after")
    @classmethod
    def ensure_positive(cls, v: int) -> int:
        # اگر مقدار عدد صحیح نباشد یا منفی باشد خطا می‌دهیم
        if not isinstance(v, int) or v < 0:
            raise ValueError("length bounds must be non-negative integers")
        return v

    # متد تولید رمز؛ از secrets.choice برای امنیت بیشتر استفاده می‌شود
    def generate_password(self, length: int = 8) -> str:
        # بررسی محدوده طول
        if length < self.min_length or length > self.max_length:
            raise ValueError(f"length must be between {self.min_length} and {self.max_length}")
        # تولید رمز با انتخاب امن هر کاراکتر از letters و اتصال آن‌ها
        return "".join(secrets.choice(self.letters) for _ in range(length))

# زیرکلاس برای ارقام
class NumericPasswordGenerator(PasswordGeneratorBase):
    letters: ClassVar[str] = string.digits

# زیرکلاس برای حروف
class LetterPasswordGenerator(PasswordGeneratorBase):
    letters: ClassVar[str] = string.ascii_letters

# زیرکلاس ترکیبی از حروف و ارقام
class MixedPasswordGenerator(PasswordGeneratorBase):
    letters: ClassVar[str] = string.ascii_letters + string.digits


if __name__ == "__main__":
    num_gen = NumericPasswordGenerator()
    print("numeric:", num_gen.generate_password(length=6))

    let_gen = LetterPasswordGenerator(min_length=3, max_length=20)
    print("letters:", let_gen.generate_password(length=10))

    mix_gen = MixedPasswordGenerator()
    print("mixed:", mix_gen.generate_password(length=12))
