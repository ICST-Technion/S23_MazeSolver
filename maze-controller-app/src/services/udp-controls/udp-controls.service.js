import React, { useEffect } from "react";
import { View, Text } from "react-native";

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
export const sendTakePic = (socket) => {
  if (socket) {
    socket.send("pic");
  }
};

export const connectToWebSocket = async (ip, port, setStatus, setImage) => {
  return new Promise((resolve, reject) => {
    const serverAddress = `ws://${ip}:${port}`;
    const socket = new WebSocket(serverAddress);
    console.log(serverAddress);
    socket.onopen = () => {
      // Connection is successfully established
      resolve(socket);
    };

    socket.onerror = (error) => {
      // Connection error occurred
      reject(error);
    };
    socket.onmessage = (e) => {
      message = JSON.parse(e.data);
      if (message.type == "status") {
        setStatus(message.status);
      } else if (message.type == "maze") {
        setImage("data:image/jpeg;base64," + message.maze);
      }
    };
  });
};

export const requestStatus = (socket) => {
  if (socket) {
    socket.send("status");
  }
};
