import React, { useState, useEffect, useLayoutEffect, useContext } from "react";
import { View, Text } from "react-native";
import styled from "styled-components/native";
import { UDPContext } from "../../services/udp-controls/udp-controls.context";

const ConnectionIndicatorContainer = styled.View`
  border-radius: 5px;
  background-color: ${({ isConnected }) => (isConnected ? "green" : "red")};
  justify-content: center;
  align-items: center;
`;

const IndicatorText = styled.Text`
  color: white;
  font-weight: bold;
`;

export const ConnectionIndicator = ({ isConnected }) => {
  return (
    <ConnectionIndicatorContainer isConnected={isConnected}>
      <IndicatorText>
        {isConnected ? "Connected" : "Not Connected"}
      </IndicatorText>
    </ConnectionIndicatorContainer>
  );
};
