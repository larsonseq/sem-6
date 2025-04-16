def diffie_hellman(p, g, secret):
    """
    Perform Diffie-Hellman key exchange with the given prime `p`, base `g`, and secret.
    Returns the public value (g^secret % p).
    """
    return pow(g, secret, p)

def compute_shared_secret(public_value, secret, p):
    """
    Compute the shared secret using the received public value, secret, and prime `p`.
    """
    return pow(public_value, secret, p)

# Step 1: Get inputs from the user
p = int(input("Enter a prime number (p): "))
g = int(input("Enter a base (g): "))

# Step 2: Each party selects a secret
alice_secret = int(input("Enter Alice's secret key: "))
bob_secret = int(input("Enter Bob's secret key: "))

# Step 3: Calculate public values for Alice and Bob
alice_public = diffie_hellman(p, g, alice_secret)
bob_public = diffie_hellman(p, g, bob_secret)
 
# Step 5: Both parties compute the shared secret
alice_shared_secret = compute_shared_secret(bob_public, alice_secret, p)
bob_shared_secret = compute_shared_secret(alice_public, bob_secret, p)
 
print(f"\nAlice's public value: {alice_public}")
print(f"Bob's public value: {bob_public}")
print(f"Alice's shared secret: {alice_shared_secret}")
print(f"Bob's shared secret: {bob_shared_secret}")
 
if alice_shared_secret == bob_shared_secret:
    print("The shared secret is successfully established.")
else:
    print("The shared secret key does not match")