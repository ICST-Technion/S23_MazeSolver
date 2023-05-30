import React, { useContext, useState } from "react";
import styled from "styled-components/native";
import {
  TouchableOpacity,
  Keyboard,
  TouchableWithoutFeedback,
} from "react-native";
import { List, Avatar } from "react-native-paper";

import { Text } from "../../components/typography/text.component";
import { SafeArea } from "../../components/utility/safe-area.component";
import { Spacer } from "../../components/spacer/spacer.component";
import { ConnectionIndicator } from "../../components/network/connection-indicator.component";
import { ActivityIndicator, Colors } from "react-native-paper";
import Toast from "react-native-root-toast";

import { Button, TextInput } from "react-native-paper";
import { UDPContext } from "../../services/udp-controls/udp-controls.context";
import { checkConnection } from "../../services/udp-controls/udp-controls.service";

export const AccountBackground = styled.View`
  flex: 1;
  align-items: center;
  justify-content: center;
`;

export const AccountCover = styled.View`
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.3);
`;

export const AccountContainer = styled.View`
  background-color: rgba(255, 255, 255, 0.7);
  padding: ${(props) => props.theme.space[4]};
  margin-top: ${(props) => props.theme.space[2]};
`;

export const NetworkSetButton = styled(Button)`
  padding: ${(props) => props.theme.space[2]};
`;

export const NetworkInput = styled(TextInput)`
  width: 300px;
`;

export const Title = styled(Text)`
  font-size: 30px;
`;

export const ErrorContainer = styled.View`
  max-width: 300px;
  align-items: center;
  align-self: center;
  margin-top: ${(props) => props.theme.space[2]};
  margin-bottom: ${(props) => props.theme.space[2]};
`;

export const AnimationWrapper = styled.View`
  width: 100%;
  height: 40%;
  position: absolute;
  top: 30px;
  padding: ${(props) => props.theme.space[2]};
`;

export const SettingsScreen = ({ navigation }) => {
  const handleScreenPress = () => {
    Keyboard.dismiss();
  };

  const {
    setServerIp,
    setServerPort,
    serverIp,
    serverPort,
    isConnected,
    attemptConnection,
  } = useContext(UDPContext);
  const [port, setPort] = useState(serverPort);
  const [ip, setIp] = useState(serverIp);
  return (
    <TouchableWithoutFeedback onPress={handleScreenPress}>
      <AccountBackground>
        <AccountCover />
        <Title>Network Settings</Title>
        <AccountContainer>
          <NetworkInput
            label="Server IP"
            value={ip}
            autoCapitalize="none"
            onChangeText={(u) => setIp(u)}
          />
          <Spacer size="large">
            <NetworkInput
              label="Port"
              value={port}
              autoCapitalize="none"
              onChangeText={(p) => setPort(p)}
            />
          </Spacer>

          <Spacer size="large">
            <NetworkSetButton
              icon="wifi"
              mode="contained"
              onPress={() => {
                setServerIp(ip);
                setServerPort(port);
                Keyboard.dismiss();
                attemptConnection();
              }}
            >
              Set and Check
            </NetworkSetButton>
          </Spacer>
          <Spacer>
            <ConnectionIndicator isConnected={isConnected} />
          </Spacer>
        </AccountContainer>
      </AccountBackground>
    </TouchableWithoutFeedback>
  );
};
