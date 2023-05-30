import React, { useEffect } from "react";
import { View, Text } from "react-native";

SERVER_ADDRESS = "ws://192.168.1.101:8080";

export const sendStart = (socket) => {
  if (socket) {
    socket.send("start");
  }
};

export const sendStop = (socket) => {
  if (socket) {
    socket.send("stop");
  }
};

export const sendReset = (socket) => {
  if (socket) {
    socket.send("reset");
  }
};

export const connectToWebSocket = async (ip, port) => {
  return new Promise((resolve, reject) => {
    const serverAddress = `ws://${ip}:${port}`;
    const socket = new WebSocket(serverAddress);

    socket.onopen = () => {
      // Connection is successfully established
      resolve(socket);
    };

    socket.onerror = (error) => {
      // Connection error occurred
      reject(error);
    };
  });
};
