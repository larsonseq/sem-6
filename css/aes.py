import numpy as np

# AES S-box
sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# Rcon for key expansion
rcon = [
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a
]

def sub_bytes(state):
    """Apply S-box substitution to each byte in the state matrix"""
    for i in range(4):
        for j in range(4):
            state[i][j] = sbox[state[i][j]]
    return state

def shift_rows(state):
    """Shift rows of the state matrix"""
    state[1] = state[1][1:] + state[1][:1]  # Shift row 1 by 1
    state[2] = state[2][2:] + state[2][:2]  # Shift row 2 by 2
    state[3] = state[3][3:] + state[3][:3]  # Shift row 3 by 3
    return state

def xtime(a):
    """Multiply by x in GF(2^8)"""
    if a & 0x80:
        return ((a << 1) ^ 0x1B) & 0xFF
    else:
        return (a << 1) & 0xFF

def mix_columns(state):
    """Mix columns of the state matrix"""
    new_state = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        new_state[0][i] = (xtime(state[0][i]) ^ xtime(state[1][i]) ^ state[1][i] ^
                          state[2][i] ^ state[3][i]) & 0xFF
        new_state[1][i] = (state[0][i] ^ xtime(state[1][i]) ^ xtime(state[2][i]) ^
                          state[2][i] ^ state[3][i]) & 0xFF
        new_state[2][i] = (state[0][i] ^ state[1][i] ^ xtime(state[2][i]) ^
                          xtime(state[3][i]) ^ state[3][i]) & 0xFF
        new_state[3][i] = (xtime(state[0][i]) ^ state[0][i] ^ state[1][i] ^
                          state[2][i] ^ xtime(state[3][i])) & 0xFF
    return new_state

def add_round_key(state, round_key):
    """Add round key to state"""
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]
    return state

def key_expansion(key):
    """Expand the 16-byte key into round keys"""
    # Initialize key_schedule with the original key
    key_schedule = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            key_schedule[j][i] = key[i*4 + j]
    
    # Expand key into round keys
    round_keys = [key_schedule]
    for round_num in range(1, 11):
        prev_key = round_keys[-1]
        new_key = [[0 for _ in range(4)] for _ in range(4)]
        
        # Calculate g(w[3])
        temp = [prev_key[0][3], prev_key[1][3], prev_key[2][3], prev_key[3][3]]
        # Rotate word
        temp = temp[1:] + temp[:1]
        # SubBytes
        temp = [sbox[b] for b in temp]
        # XOR with Rcon
        temp[0] ^= rcon[round_num]
        
        # Calculate w[4] = w[0] XOR g(w[3])
        for i in range(4):
            new_key[i][0] = prev_key[i][0] ^ temp[i]
        
        # Calculate w[5] = w[4] XOR w[1]
        for i in range(4):
            new_key[i][1] = new_key[i][0] ^ prev_key[i][1]
        
        # Calculate w[6] = w[5] XOR w[2]
        for i in range(4):
            new_key[i][2] = new_key[i][1] ^ prev_key[i][2]
        
        # Calculate w[7] = w[6] XOR w[3]
        for i in range(4):
            new_key[i][3] = new_key[i][2] ^ prev_key[i][3]
        
        round_keys.append(new_key)
    
    return round_keys

def aes_encrypt(plaintext, key):
    """Encrypt plaintext using AES-128"""
    # Convert plaintext and key to bytes if they are strings
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # Ensure plaintext and key are exactly 16 bytes
    if len(plaintext) != 16 or len(key) != 16:
        raise ValueError("Plaintext and key must be exactly 16 bytes")
    
    # Create state matrix (column-major order)
    state = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            state[j][i] = plaintext[i*4 + j]
    
    # Create key matrix
    key_bytes = [k for k in key]
    
    # Generate round keys
    round_keys = key_expansion(key_bytes)
    
    # Print initial state and key
    print("Initial state:")
    print_state(state)
    print("Initial key:")
    print_state(round_keys[0])
    
    # Round 0: Add round key
    print("\nRound 0 - Add Round Key:")
    state = add_round_key(state, round_keys[0])
    print_state(state)
    
    # Main rounds
    for round_num in range(1, 10):
        print(f"\nRound {round_num}:")
        print(f"Round {round_num} - SubBytes:")
        state = sub_bytes(state)
        print_state(state)
        
        print(f"Round {round_num} - ShiftRows:")
        state = shift_rows(state)
        print_state(state)
        
        print(f"Round {round_num} - MixColumns:")
        state = mix_columns(state)
        print_state(state)
        
        print(f"Round {round_num} - AddRoundKey:")
        state = add_round_key(state, round_keys[round_num])
        print_state(state)
    
    # Final round (no MixColumns)
    print("\nRound 10 (Final):")
    print("Round 10 - SubBytes:")
    state = sub_bytes(state)
    print_state(state)
    
    print("Round 10 - ShiftRows:")
    state = shift_rows(state)
    print_state(state)
    
    print("Round 10 - AddRoundKey:")
    state = add_round_key(state, round_keys[10])
    print_state(state)
    
    # Convert state back to bytes
    result = bytearray(16)
    for i in range(4):
        for j in range(4):
            result[i*4 + j] = state[j][i]
    
    return result

def print_state(state):
    """Print state matrix in a readable format"""
    for i in range(4):
        row = ""
        for j in range(4):
            row += f"{state[i][j]:02X} "
        print(row)

def print_round_keys(round_keys):
    """Print all round keys"""
    print("All Round Keys:")
    for i, key in enumerate(round_keys):
        flat_key = []
        for col in range(4):
            for row in range(4):
                flat_key.append(key[row][col])
        key_str = " ".join(f"{b:02X}" for b in flat_key)
        print(f"Round {i}: {key_str}")

# Example from the PDF
def main():
    key = "Thats my Kung Fu"
    plaintext = "Two One Nine Two"
    
    # Convert to bytes
    key_bytes = key.encode('utf-8')
    plaintext_bytes = plaintext.encode('utf-8')
    
    # Print inputs
    print("AES-128 Encryption Example")
    print("==========================")
    print(f"Key: {key}")
    print(f"Key (hex): {' '.join(f'{b:02X}' for b in key_bytes)}")
    print(f"Plaintext: {plaintext}")
    print(f"Plaintext (hex): {' '.join(f'{b:02X}' for b in plaintext_bytes)}")
    print()
    
    # Generate round keys
    round_keys = key_expansion(key_bytes)
    print_round_keys(round_keys)
    print()
    
    # Encrypt
    ciphertext = aes_encrypt(plaintext_bytes, key_bytes)
    
    # Print result
    print("\nEncryption Result:")
    print(f"Ciphertext (hex): {' '.join(f'{b:02X}' for b in ciphertext)}")

if __name__ == "__main__":
    main()