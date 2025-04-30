package com.lecturium.lecturiumservices.services;

import com.lecturium.lecturiumservices.models.*;
import com.lecturium.lecturiumservices.repositories.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthenticationService {

    private final UserRepository repository;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;
    private final PasswordEncoder passwordEncoder;

    public AuthenticationResponse register(RegisterRequest registerRequest) {
        var user = User.builder()
                .firstName(registerRequest.getFirstname())
                .lastName(registerRequest.getLastname())
                .email(registerRequest.getEmail())
                .hashedPassword(passwordEncoder.encode(registerRequest.getHashedPassword()))
                .role(Role.USER)
                .build();
        repository.save(user);
        var JwtToken = jwtService.generateJwtToken(user);
        return AuthenticationResponse
                .builder()
                .token(JwtToken)
                .build();
    }

    public AuthenticationResponse authenticate(AuthenticationRequest request) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.getEmail(),
                        request.getHashedPassword()
                )
        );
        var user = repository.findByEmail(request.getEmail())
                .orElseThrow();

        var JwtToken = jwtService.generateJwtToken(user);
        return AuthenticationResponse
                .builder()
                .token(JwtToken)
                .build();
    }
}

