import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Scanner;

public class Main {

    // A3: Authenticate function (for SRES generation)
    public static byte[] authenticate(byte[] rand, byte[] ki) {
        try {
            byte[] input = new byte[rand.length + ki.length];
            System.arraycopy(rand, 0, input, 0, rand.length);
            System.arraycopy(ki, 0, input, rand.length, ki.length);

            MessageDigest md = MessageDigest.getInstance("SHA-1");
            byte[] hash = md.digest(input);

            byte[] sres = new byte[8]; // Take the first 8 bytes of the hash
            System.arraycopy(hash, 0, sres, 0, 8);
            return sres;
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-1 algorithm not available", e);
        }
    }

    // A8: Key Generation Algorithm (for Kc generation)
    public static byte[] generateKey(byte[] rand, byte[] ki) {
        try {
            byte[] input = new byte[rand.length + ki.length];
            System.arraycopy(rand, 0, input, 0, rand.length);
            System.arraycopy(ki, 0, input, rand.length, ki.length);

            MessageDigest md = MessageDigest.getInstance("SHA-1");
            byte[] hash = md.digest(input);

            byte[] kc = new byte[8]; // Key length is 8 bytes
            System.arraycopy(hash, 0, kc, 0, 8);
            return kc;
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-1 algorithm not available", e);
        }
    }

    // A5: Encryption Algorithm (XOR)
    public static byte[] encrypt(byte[] plaintext, byte[] key) {
        byte[] ciphertext = new byte[plaintext.length];
        for (int i = 0; i < plaintext.length; i++) {
            ciphertext[i] = (byte) (plaintext[i] ^ key[i % key.length]);
        }
        return ciphertext;
    }

    // A5: Decryption Algorithm (Same as encryption for XOR)
    public static byte[] decrypt(byte[] ciphertext, byte[] key) {
        return encrypt(ciphertext, key);
    }

    // Helper to Convert Bytes to Hex String
    public static String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Input RAND and Ki for A3 and A8
        System.out.println("Enter RAND (16 characters):");
        String randInput = scanner.nextLine();
        System.out.println("Enter Ki (16 characters):");
        String kiInput = scanner.nextLine();

        byte[] rand = randInput.getBytes();
        byte[] ki = kiInput.getBytes();

        // Generate SRES using A3
        byte[] sres = authenticate(rand, ki);
        System.out.println("Generated SRES: " + bytesToHex(sres));

        // Generate Key using A8
        byte[] kc = generateKey(rand, ki);
        System.out.println("Generated Key (Kc): " + bytesToHex(kc));

        // Input Plaintext for Encryption
        System.out.println("Enter plaintext message:");
        String plaintextInput = scanner.nextLine();
        byte[] plaintext = plaintextInput.getBytes();

        // Encrypt using A5
        byte[] ciphertext = encrypt(plaintext, kc);
        System.out.println("Encrypted Message: " + bytesToHex(ciphertext));

        // Decrypt for Verification
        byte[] decryptedText = decrypt(ciphertext, kc);
        System.out.println("Decrypted Message: " + new String(decryptedText));
    }
}
