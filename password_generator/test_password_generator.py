

import secrets
import string


def generate_password(length, include_uppercase=True, include_lowercase=True,
                      include_numbers=True, include_special=True):
    """
    Generate a secure random password.
    
    Args:
        length (int): Desired password length
        include_uppercase (bool): Include uppercase letters
        include_lowercase (bool): Include lowercase letters
        include_numbers (bool): Include numbers
        include_special (bool): Include special characters
    
    Returns:
        str: Generated password
    """
    char_pool = ""
    
    if include_uppercase:
        char_pool += string.ascii_uppercase
    if include_lowercase:
        char_pool += string.ascii_lowercase
    if include_numbers:
        char_pool += string.digits
    if include_special:
        char_pool += string.punctuation
    
    if not char_pool:
        raise ValueError("At least one character type must be selected!")
    
    password = ''.join(secrets.choice(char_pool) for _ in range(length))
    return password


def calculate_strength(password):
    """Calculate password strength."""
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    score = 0
    if length >= 8: score += 1
    if length >= 12: score += 1
    if length >= 16: score += 1
    if has_upper: score += 1
    if has_lower: score += 1
    if has_digit: score += 1
    if has_special: score += 1
    
    if score <= 3:
        return "Weak"
    elif score <= 5:
        return "Moderate"
    else:
        return "Strong"


def main():
    """Run password generation tests."""
    print("=" * 70)
    print(" " * 20 + "PASSWORD GENERATOR - TEST DEMO")
    print("=" * 70)
    
    # Test Case 1: Strong Password (All options)
    print("\n📝 Test Case 1: Strong Password (16 chars, all options)")
    print("-" * 70)
    password1 = generate_password(16, True, True, True, True)
    print(f"Generated: {password1}")
    print(f"Strength:  {calculate_strength(password1)}")
    
    # Test Case 2: Numeric PIN
    print("\n📝 Test Case 2: Numeric PIN (6 chars, numbers only)")
    print("-" * 70)
    password2 = generate_password(6, False, False, True, False)
    print(f"Generated: {password2}")
    print(f"Strength:  {calculate_strength(password2)}")
    
    # Test Case 3: Alphanumeric (No special chars)
    print("\n📝 Test Case 3: Alphanumeric (12 chars, no special)")
    print("-" * 70)
    password3 = generate_password(12, True, True, True, False)
    print(f"Generated: {password3}")
    print(f"Strength:  {calculate_strength(password3)}")
    
    # Test Case 4: Maximum Security
    print("\n📝 Test Case 4: Maximum Security (32 chars, all options)")
    print("-" * 70)
    password4 = generate_password(32, True, True, True, True)
    print(f"Generated: {password4}")
    print(f"Strength:  {calculate_strength(password4)}")
    
    # Test Case 5: Letters Only
    print("\n📝 Test Case 5: Letters Only (10 chars)")
    print("-" * 70)
    password5 = generate_password(10, True, True, False, False)
    print(f"Generated: {password5}")
    print(f"Strength:  {calculate_strength(password5)}")
    
    # Generate multiple passwords to show randomness
    print("\n📝 Test Case 6: Multiple Passwords (same settings)")
    print("-" * 70)
    print("Generating 5 passwords with identical settings to demonstrate randomness:")
    for i in range(1, 6):
        pwd = generate_password(12, True, True, True, True)
        print(f"  {i}. {pwd}")
    
    print("\n" + "=" * 70)
    print("✅ All tests completed successfully!")
    print("=" * 70)
    
    # Statistics
    print("\n📊 Character Pool Information:")
    print("-" * 70)
    print(f"Uppercase letters: {len(string.ascii_uppercase)} chars ({string.ascii_uppercase})")
    print(f"Lowercase letters: {len(string.ascii_lowercase)} chars ({string.ascii_lowercase})")
    print(f"Numbers:           {len(string.digits)} chars ({string.digits})")
    print(f"Special chars:     {len(string.punctuation)} chars ({string.punctuation})")
    print(f"\nTotal (all types): {len(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation)} unique characters")
    
    print("\n💡 Security Note:")
    print("-" * 70)
    print("All passwords are generated using Python's 'secrets' module,")
    print("which provides cryptographically strong random generation.")
    print("This makes them suitable for security-sensitive applications.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
