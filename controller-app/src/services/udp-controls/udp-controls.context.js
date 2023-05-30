import React, { useState, createContext, useEffect, useContext } from "react";
import { connectToWebSocket } from "./udp-controls.service";

export const UDPContext = createContext();
export const UDPContextProvider = ({ children }) => {
  const [serverIp, setServerIp] = useState("192.168.5.1");
  const [serverPort, setServerPort] = useState(8080);
  const [socket, setSocket] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    attemptConnection();
  }, [serverIp, serverPort]);

  const attemptConnection = () => {
    connectToWebSocket(serverIp, serverPort)
      .then((res) => {
        setSocket(res);
        setIsConnected(true);
      })
      .catch((err) => {
        setIsConnected(false);
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
        socket,
        isConnected,
      }}
    >
      {children}
    </UDPContext.Provider>
  );
};
