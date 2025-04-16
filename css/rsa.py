from math import gcd

# Function to check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

# Function to compute modular inverse
def mod_inverse(e, phi):
    for d in range(2, phi):
        if (d * e) % phi == 1:
            return d
    return None

# Get two prime numbers from the user
while True:
    P = int(input("Enter first prime number (P): "))
    if is_prime(P):
        break
    print("P is not a prime number. Please enter a valid prime.")

while True:
    Q = int(input("Enter second prime number (Q): "))
    if is_prime(Q):
        break
    print("Q is not a prime number. Please enter a valid prime.")

# Step 1: Compute N
N = P * Q
print(f"\nN = P × Q = {P} × {Q} = {N}")

# Step 2: Compute Euler's Totient Function (Φ(n))
phi_n = (P - 1) * (Q - 1)
print(f"Φ(n) = (P - 1) × (Q - 1) = ({P} - 1) × ({Q} - 1) = {phi_n}")

# Step 3: Choose public key E
for E in range(2, phi_n):
    if gcd(E, phi_n) == 1:
        break
print(f"\nPublic key exponent (E) chosen such that gcd(E, Φ(n)) = 1:")
print(f"E = {E}")

# Step 4: Compute private key D
D = mod_inverse(E, phi_n)
print(f"\nPrivate key (D) is calculated as modular inverse of E mod Φ(n):")
print(f"(D × E) mod Φ(n) = 1")
print(f"({D} × {E}) mod {phi_n} = 1")

# Display public and private keys
print("\nPublic Key: (E, N) = ({}, {})".format(E, N))
print("Private Key: (D, N) = ({}, {})".format(D, N))

# Encryption function
def encrypt(pt, E, N):
    return pow(pt, E, N)  # CT = PT^E mod N

# Decryption function
def decrypt(ct, D, N):
    return pow(ct, D, N)  # PT = CT^D mod N

# Step 5: User enters a message
message = int(input("\nEnter a number to encrypt (Plain Text PT): "))
print(f"\nEncrypting using: CT = PT^E mod N")
ciphertext = encrypt(message, E, N)
print(f"Cipher Text (CT) = {message}^{E} mod {N} = {ciphertext}")

# Step 6: Decrypt the message
print(f"\nDecrypting using: PT = CT^D mod N")
decrypted_message = decrypt(ciphertext, D, N)
print(f"Decrypted Plain Text (PT) = {ciphertext}^{D} mod {N} = {decrypted_message}")
