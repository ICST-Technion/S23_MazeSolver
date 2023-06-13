import React, { useState, createContext, useEffect, useRef } from "react";
import { connectToWebSocket, requestStatus } from "./udp-controls.service";

export const UDPContext = createContext();
export const UDPContextProvider = ({ children }) => {
  const [serverIp, setServerIp] = useState("192.168.5.1");
  const [serverPort, setServerPort] = useState("7000");
  const [socket, setSocket] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [status, setStatus] = useState({
    connection: false,
    path_found: false,
    running: false,
    calculating_path: false,
  });
  const [mazeImage, setMazeImage] = useState(null);
  const [keyToText, setKeyToText] = useState({
    connection: "Network Connection",
    path_found: "Found Path",
    running: "Solver Running",
    calculating_path: "Calculating Path",
  });
  useEffect(() => {
    attemptConnection();
  }, [serverIp, serverPort]);

  const updateStatus = () => {
    if (socket === null) {
      setStatusValues({
        connection: false,
        path_found: false,
        running: false,
        calculating_path: false,
      });
    } else if (socket.readyState === WebSocket.CLOSED) {
      setStatusValues({
        connection: false,
        path_found: false,
        running: false,
        calculating_path: false,
      });
    } else {
      requestStatus(socket);
    }
  };

  const setStatusValues = (updated_status) => {
    let temp_status = { ...status };
    for (const key in updated_status) {
      temp_status[key] = updated_status[key];
    }
    setStatus(temp_status);
  };

  const attemptConnection = () => {
    connectToWebSocket(serverIp, serverPort, setStatusValues, setMazeImage)
      .then((res) => {
        setSocket(res);
        setIsConnected(true);
      })
      .catch((err) => {
        console.log(err);
        setIsConnected(false);
        if (socket) {
          socket.close();
        }
        setSocket(null);
      });
  };
  return (
    <UDPContext.Provider
      value={{
        serverIp,
        serverPort,
        setServerPort,
        setServerIp,
        attemptConnection,
        setSocket,
        setStatusValues,
        keyToText: keyToText,
        status,
        socket,
        updateStatus,
        isConnected,
        mazeImage,
      }}
    >
      {children}
    </UDPContext.Provider>
  );
};
