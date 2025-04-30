package com.lecturium.lecturiumservices.config;

import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Base64;

@Component
public class JwtConfig {
    private static String aesKeyBase64;

    @Value("${app.jwtKey.name}")
    public void setAesKeyBase64(String key) {
        JwtConfig.aesKeyBase64 = key;
    }

    public static SecretKey getSingInKey() {
        byte[] keyBytes = Base64.getDecoder().decode(aesKeyBase64);
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
