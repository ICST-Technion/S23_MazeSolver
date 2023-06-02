import React, { useContext, useEffect } from "react";
import { View, Image } from "react-native";
import Svg, { Path } from "react-native-svg";
import styled from "styled-components/native";
import { Button } from "react-native-paper";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Text } from "../../../components/typography/text.component";
import { SafeArea } from "../../../components/utility/safe-area.component";
import { Spacer } from "../../../components/spacer/spacer.component";
import {
  sendStart,
  sendStop,
  sendReset,
  sendTakePic,
} from "../../../services/udp-controls/udp-controls.service";
import { UDPContext } from "../../../services/udp-controls/udp-controls.context";

const LogoComponent = (props) => (
  <Image
    source={require("../../../../assets/iot-icon.png")}
    style={{ width: 400, height: 400 }}
  />
);

const ScreenContainer = styled.View`
  background-color: ${(props) => props.theme.colors.bg.primary};
  flex: 1;
`;

const LogoContainer = styled.View`
  background-color: ${(props) => props.theme.colors.bg.primary};
  padding: 100px;
  justify-content: center;
  align-items: center;

  flex: 1;
`;

const FunctionalContainer = styled.View`
  background-color: ${(props) => props.theme.colors.bg.primary};
  padding: 10px;
  align-items: center;

  flex: 1;
`;
const ButtonsContainer = styled.View`
  background-color: ${(props) => props.theme.colors.bg.primary};
  padding: 10px;

  flex: 1;
`;

export const MainMenu = ({ navigation }) => {
  const { socket, updateStatus } = useContext(UDPContext);
  useEffect(() => {
    if (socket !== null) {
      const interval = setInterval(() => {
        updateStatus();
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [socket]);
  return (
    <ScreenContainer>
      <SafeArea>
        <LogoContainer>
          <LogoComponent />
          <Spacer position="top" size={"large"}>
            <Text variant={"title"}>Car Controller</Text>
          </Spacer>
        </LogoContainer>
        <FunctionalContainer>
          <ButtonsContainer>
            <Spacer position={"bottom"} size={"large"}>
              <Button
                icon="play"
                mode="contained"
                color="black"
                onPress={() => {
                  sendStart(socket);
                }}
              >
                Start
              </Button>
            </Spacer>
            <Spacer position={"bottom"} size={"large"}>
              <Button
                icon="stop"
                mode="contained"
                color="black"
                onPress={() => {
                  sendStop(socket);
                }}
              >
                Stop
              </Button>
            </Spacer>
            <Spacer position={"bottom"} size={"large"}>
              <Button
                icon="replay"
                mode="contained"
                color="black"
                onPress={() => {
                  sendReset(socket);
                }}
              >
                Restart
              </Button>
            </Spacer>

            <Button
              icon="camera"
              mode="contained"
              color="black"
              onPress={() => {
                sendTakePic(socket);
              }}
            >
              Take Maze Image
            </Button>
          </ButtonsContainer>
        </FunctionalContainer>
      </SafeArea>
    </ScreenContainer>
  );
};
