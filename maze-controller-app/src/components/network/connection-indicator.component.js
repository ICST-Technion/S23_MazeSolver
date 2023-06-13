import React, { useState, useEffect, useLayoutEffect, useContext } from "react";
import { View } from "react-native";
import { Text } from "../typography/text.component";
import styled from "styled-components/native";
import { UDPContext } from "../../services/udp-controls/udp-controls.context";
import { Spacer } from "../spacer/spacer.component";

const ConnectionIndicatorContainer = styled.View`
  border-radius: 5px;
  padding: 5px;
  flex-direction: row;
  justify-content: space-between;
`;

const Indicator = styled.View`
  width: 20px;
  height: 20px;
  border-radius: 10px;
  border-width: 1px;
  border-color: #ccc;
  background: ${({ isOn }) => (isOn ? "#00FF00" : "#CCCCCC")};
`;

export const StatusIndicator = ({ isOn, label }) => {
  return (
    <ConnectionIndicatorContainer isOn={isOn}>
      <Text variant={"title"}>{label}</Text>
      <Indicator isOn={isOn} />
    </ConnectionIndicatorContainer>
  );
};
