# Stage 1: Build the application
FROM openjdk:21-jdk-slim AS build

WORKDIR /app

COPY gradlew .
COPY gradle gradle
COPY build.gradle .
COPY settings.gradle .
COPY src src

# Build the project with Gradle without tests
RUN chmod +x gradlew
RUN ./gradlew build -x test --no-daemon

# Remove the extra *-plain.jar file
RUN rm -f /build/libs/*-plain.jar

RUN ls -R
# Stage 2: Run the application
FROM openjdk:21-jdk-slim

WORKDIR /app

COPY --from=build app/build/libs/*.jar app.jar

EXPOSE 8080
CMD ["java", "-jar", "app.jar"]

