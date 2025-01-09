FROM gradle:8.5.0-jdk17-jammy

COPY . /build/
RUN cd /build && gradle build

WORKDIR /build/
CMD ["java", "-jar", "/build/build/libs/webwebhookhook-0.0.1-SNAPSHOT.jar"]

