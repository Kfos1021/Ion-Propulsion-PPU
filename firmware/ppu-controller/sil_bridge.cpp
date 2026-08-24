/**
 * @file sil_bridge.cpp
 * @brief C++ TCP Socket Server for Software-in-the-Loop (SiL) Integration
 */

#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 8080

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};

    std::cout << "--- Starting C++ PPU SiL IPC Server ---" << std::endl;

    // Create Socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket creation failed");
        return -1;
    }

    // Attach socket to port 8080
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror("setsockopt failed");
        return -1;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        return -1;
    }

    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        return -1;
    }

    std::cout << "[SiL SERVER] Waiting for Python Thruster Simulator on port " << PORT << "..." << std::endl;

    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
        perror("Accept failed");
        return -1;
    }

    std::cout << "[SiL SERVER] Python Thruster Model Connected!" << std::endl;

    // Send initial control command
    std::string command = "STATE:THRUST,THROTTLE:1.0\n";
    send(new_socket, command.c_str(), command.length(), 0);
    std::cout << "[SiL SERVER] Sent Command: " << command;

    // Read response telemetry from Python
    read(new_socket, buffer, 1024);
    std::cout << "[SiL SERVER] Received Telemetry: " << buffer << std::endl;

    close(new_socket);
    close(server_fd);
    return 0;
}