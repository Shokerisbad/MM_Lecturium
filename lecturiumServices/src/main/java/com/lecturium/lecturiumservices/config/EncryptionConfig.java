package com.lecturium.lecturiumservices.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class EncryptionConfig {

    @Value("${app.encryptionKey.name}")
    private String aesKeyBase64;

    public byte[] getAesKey() {
        return java.util.Base64.getDecoder().decode(aesKeyBase64);
    }
}