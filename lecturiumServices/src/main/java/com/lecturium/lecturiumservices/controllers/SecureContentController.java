package com.lecturium.lecturiumservices.controllers;

import com.lecturium.lecturiumservices.services.EncryptionService;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StreamUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.InputStream;
import java.nio.file.Path;
import java.nio.file.Paths;


@RestController
@RequestMapping("/api/v1/secure-content")
public class SecureContentController {

    // Example: Define path where original files are stored
    private final Path fileStorageLocation = Paths.get("./uploads").toAbsolutePath().normalize();
    private final EncryptionService encryptionService;

    public SecureContentController(EncryptionService encryptionService) {
        this.encryptionService = encryptionService;
    }

    @GetMapping("/{filename:.+}")
    public ResponseEntity<?> getEncryptedFile(@PathVariable String filename) {
        try {
            //Construct the path to the original file
            Path filePath = this.fileStorageLocation.resolve(filename).normalize();
            System.out.println(filePath);
            //Basic security check - prevent path traversal
            if (!filePath.startsWith(this.fileStorageLocation)) {
                return ResponseEntity.status(HttpStatus.FORBIDDEN).body("Access denied.");
            }

            Resource resource = new UrlResource(filePath.toUri());

            if (!resource.exists() || !resource.isReadable()) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("File not found or not readable.");
            }

            //Read the original file content
            byte[] fileContent;
            try (InputStream inputStream = resource.getInputStream()) {
                fileContent = StreamUtils.copyToByteArray(inputStream);
            }

            //Encrypt the file content
            byte[] encryptedData = encryptionService.encrypt(fileContent);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_OCTET_STREAM); // Indicate binary data
            headers.setContentLength(encryptedData.length);

            return new ResponseEntity<>(encryptedData, headers, HttpStatus.OK);


            /* // Option 2: Send Base64 encoded string (simpler for some JS handling)
             String encryptedBase64Data = encryptionService.encryptAndBase64Encode(fileContent);

             HttpHeaders headers = new HttpHeaders();
             headers.setContentType(MediaType.TEXT_PLAIN); // It's text now
             headers.setContentLength(encryptedBase64Data.length());

             return new ResponseEntity<>(encryptedBase64Data, headers, HttpStatus.OK);
            */


        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error encrypting file.");
        }
    }

    @GetMapping("/decrypt/{filename:.+}")
    public ResponseEntity<?> getDencryptedFile(@PathVariable String filename) {
        try {
            Path filePath = this.fileStorageLocation.resolve(filename).normalize();
            System.out.println(filePath);
            if (!filePath.startsWith(this.fileStorageLocation)) {
                return ResponseEntity.status(HttpStatus.FORBIDDEN).body("Access denied.");
            }

            Resource resource = new UrlResource(filePath.toUri());

            if (!resource.exists() || !resource.isReadable()) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("File not found or not readable.");
            }

            //read file
            byte[] fileContent;
            try (InputStream inputStream = resource.getInputStream()) {
                fileContent = StreamUtils.copyToByteArray(inputStream);
            }

            // decrypt file
            byte[] encryptedData = encryptionService.decrypt(fileContent);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_OCTET_STREAM); //Indicate binary data
            headers.setContentLength(encryptedData.length);

            return new ResponseEntity<>(encryptedData, headers, HttpStatus.OK);


        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error decrypting file.");
        }
    }
}