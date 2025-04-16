def hex_to_bin(hex_str):
    """Convert a hexadecimal string to binary string"""
    return ''.join(bin(int(c, 16))[2:].zfill(4) for c in hex_str)

def bin_to_hex(bin_str):
    """Convert a binary string to hexadecimal string"""
    return ''.join(hex(int(bin_str[i:i+4], 2))[2:] for i in range(0, len(bin_str), 4))

def text_to_binary(text):
    """Convert text to binary"""
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def permute(k, arr, n):
    """Permute the given input k according to the array arr"""
    permutation = ""
    for i in range(0, n):
        permutation += k[arr[i] - 1]
    return permutation

def shift_left(k, shifts):
    """Circular left shift the string by the specified number of shifts"""
    return k[shifts:] + k[:shifts]

def xor(a, b):
    """XOR two strings of binary"""
    result = ""
    for i in range(len(a)):
        result += '1' if a[i] != b[i] else '0'
    return result

# Initial Permutation Table
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]

# Expansion D-box Table
exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
         6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1]

# S-box Tables
s_box = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Straight Permutation Table
per = [16, 7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2, 8, 24, 14,
       32, 27, 3, 9,
       19, 13, 30, 6,
       22, 11, 4, 25]

# Final Permutation Table
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

# Parity bit drop table
keyp = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# Number of bits shifted per round
shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Key compression table
key_comp = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]

def encrypt(pt, key, show_details=True):
    # Convert the plain text to binary
    if all(c in '0123456789ABCDEF' for c in pt.upper()):
        pt = hex_to_bin(pt.upper())
    else:
        pt = text_to_binary(pt)
    
    # Pad to 64 bits if needed
    if len(pt) < 64:
        pt = pt.zfill(64)
    elif len(pt) > 64:
        pt = pt[:64]  # Truncate if longer than 64 bits
    
    if show_details:
        print(f"Plain Text (64 bits): {pt}")
        print(f"Plain Text (Hex): {bin_to_hex(pt)}")
    
    # Convert the key to binary
    if all(c in '0123456789ABCDEF' for c in key.upper()):
        key = hex_to_bin(key.upper())
    else:
        key = text_to_binary(key)
    
    # Pad key to 64 bits if needed
    if len(key) < 64:
        key = key.zfill(64)
    elif len(key) > 64:
        key = key[:64]  # Truncate if longer than 64 bits
    
    if show_details:
        print(f"Key (64 bits): {key}")
        print(f"Key (Hex): {bin_to_hex(key)}")
    
    # Initial Permutation
    pt = permute(pt, initial_perm, 64)
    if show_details:
        print("\nAfter Initial Permutation:", pt)
        print("After Initial Permutation (Hex):", bin_to_hex(pt))
    
    # Splitting
    left = pt[0:32]
    right = pt[32:64]
    if show_details:
        print(f"\nInitial Split - Left: {left}")
        print(f"Initial Split - Right: {right}")
    
    # Key generation
    # --parity bit drop table
    key = permute(key, keyp, 56)
    if show_details:
        print("\nAfter parity bit drop (56 bits):", key)
    
    # Splitting key
    left_key = key[0:28]
    right_key = key[28:56]
    
    rkb = []  # round keys binary
    rkh = []  # round keys in hexadecimal
    
    for i in range(16):
        # Shifting
        left_key = shift_left(left_key, shift_table[i])
        right_key = shift_left(right_key, shift_table[i])
        
        # Combining
        combined_key = left_key + right_key
        
        # Key Compression
        round_key = permute(combined_key, key_comp, 48)
        
        rkb.append(round_key)
        rkh.append(bin_to_hex(round_key))
        
        if show_details:
            print(f"\nRound {i+1} Key Generation:")
            print(f"Left Key after Shifting: {left_key}")
            print(f"Right Key after Shifting: {right_key}")
            print(f"Combined Key: {combined_key}")
            print(f"Round Key {i+1}: {round_key}")
            print(f"Round Key {i+1} (Hex): {rkh[i]}")
    
    if show_details:
        print("\nEncryption Process:")
    
    for i in range(16):
        if show_details:
            print(f"\n========== Round {i+1} ==========")
            print(f"Input Left: {left}")
            print(f"Input Right: {right}")
        
        # Expansion D-box
        right_expanded = permute(right, exp_d, 48)
        if show_details:
            print(f"Right Expanded (48 bits): {right_expanded}")
        
        # XOR RoundKey[i] and right_expanded
        xor_x = xor(right_expanded, rkb[i])
        if show_details:
            print(f"XOR with Round Key {i+1}: {xor_x}")
        
        # S-boxes
        sbox_str = ""
        for j in range(8):
            row = int(xor_x[j*6] + xor_x[j*6 + 5], 2)
            col = int(xor_x[j*6 + 1:j*6 + 5], 2)
            val = s_box[j][row][col]
            sbox_str += bin(val)[2:].zfill(4)
            
            if show_details:
                print(f"S-Box {j+1}: Input={xor_x[j*6:j*6+6]}, Row={row}, Col={col}, Value={val} => {bin(val)[2:].zfill(4)}")
        
        if show_details:
            print(f"S-Box Output (32 bits): {sbox_str}")
        
        # Straight D-box
        sbox_str = permute(sbox_str, per, 32)
        if show_details:
            print(f"After Straight Permutation: {sbox_str}")
        
        # XOR left and sbox_str
        result = xor(left, sbox_str)
        left = result
        if show_details:
            print(f"XOR Result (New Left): {result}")
        
        # Swapper
        if i != 15:
            left, right = right, left
            if show_details:
                print(f"After Swapping - Left: {left}")
                print(f"After Swapping - Right: {right}")
        else:
            if show_details:
                print(f"Final Left: {left}")
                print(f"Final Right: {right}")
    
    # Combine
    combine = left + right
    if show_details:
        print("\nCombined (Before Final Permutation):", combine)
    
    # Final permutation
    cipher_text = permute(combine, final_perm, 64)
    if show_details:
        print("Cipher Text (Binary):", cipher_text)
        print("Cipher Text (Hex):", bin_to_hex(cipher_text))
    
    return cipher_text, bin_to_hex(cipher_text)

def main():
    print("=== DES ENCRYPTION ALGORITHM ===\n")
    
    # Get plaintext from user
    plaintext = input("Enter plaintext (text or hex): ")
    
    # Get key from user
    key = input("Enter key (text or hex): ")
    
    # Encrypt with detailed output
    cipher_binary, cipher_hex = encrypt(plaintext, key)
    
    print("\n=== FINAL RESULT ===")
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Encrypted (Binary): {cipher_binary}")
    print(f"Encrypted (Hex): {cipher_hex}")

if __name__ == "__main__":
    main()