package com.lecturium.lecturiumservices.services;

import com.lecturium.lecturiumservices.config.EncryptionConfig;
import org.springframework.stereotype.Service;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.ByteBuffer;
import java.security.SecureRandom;

@Service
public class EncryptionService {

    private static final String ALGORITHM = "AES/GCM/NoPadding";
    private static final int GCM_IV_LENGTH = 12; // 96 bits is standard for GCM IV/Nonce
    private static final int GCM_TAG_LENGTH = 128; // bits

    private static SecretKey secretKey = null;
    private static final SecureRandom secureRandom = new SecureRandom();

    public EncryptionService(EncryptionConfig encryptionConfig) {
        byte[] keyBytes = encryptionConfig.getAesKey();
        if (keyBytes.length != 32) { // Check for 256-bit key
            throw new IllegalArgumentException("Invalid AES key length. Requires 32 bytes (256 bits).");
        }
        secretKey = new SecretKeySpec(keyBytes, "AES");
    }



    public static byte[] encrypt(byte[] plainData) throws Exception {
        // 1. Generate a unique IV/Nonce for each encryption
        byte[] iv = new byte[GCM_IV_LENGTH];
        secureRandom.nextBytes(iv);

        // 2. Initialize Cipher
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        GCMParameterSpec gcmParameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, gcmParameterSpec);

        // 3. Encrypt data
        byte[] cipherText = cipher.doFinal(plainData);

        // 4. Prepend IV to ciphertext for decryption on the client
        // The client needs the IV (it's not secret) to decrypt correctly.
        ByteBuffer byteBuffer = ByteBuffer.allocate(iv.length + cipherText.length);
        byteBuffer.put(iv);
        byteBuffer.put(cipherText);
        return byteBuffer.array();
    }

    // Optional: Add a decrypt method for testing or other backend needs
    public static byte[] decrypt(byte[] encryptedDataWithIv) throws Exception {
        // 1. Extract IV and Ciphertext
        ByteBuffer byteBuffer = ByteBuffer.wrap(encryptedDataWithIv);
        byte[] iv = new byte[GCM_IV_LENGTH];
        byteBuffer.get(iv);
        byte[] cipherText = new byte[byteBuffer.remaining()];
        byteBuffer.get(cipherText);

        // 2. Initialize Cipher
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        GCMParameterSpec gcmParameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
        cipher.init(Cipher.DECRYPT_MODE, secretKey, gcmParameterSpec);

        // 3. Decrypt data
        return cipher.doFinal(cipherText);
    }


}