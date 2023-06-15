import React, { useRef, useState, useEffect, useContext } from "react";
import Toast from "react-native-root-toast";
import {
  PanResponder,
  TouchableOpacity,
  View,
  StyleSheet,
  Dimensions,
  Image,
} from "react-native";
import styled from "styled-components";
import { SafeArea } from "../../../components/utility/safe-area.component";
import { UDPContext } from "../../../services/udp-controls/udp-controls.context";
import { TakePictureModal } from "../components/modal.component";
import { sendTakePic } from "../../../services/udp-controls/udp-controls.service";

const CircleWithInnerRing = () => {
  return (
    <Container>
      <Circle />
      <InnerRing />
    </Container>
  );
};

const Container = styled(View)`
  justify-content: center;
  align-items: center;
`;

const Circle = styled(View)`
  border-radius: 90px;
  width: 75px;
  height: 75px;
  background-color: black;
`;

const InnerRing = styled(View)`
  position: absolute;
  width: 60px;
  height: 60px;
  border-radius: 80px;
  border-width: 3px;
  border-color: white;
`;

const MazeContainer = styled(View)`
  justify-content: center;
  align-items: center;
  flex: 1;
`;

const ButtonContainer = styled(View)`
  padding: 5px;
  overflow: hidden;
  border-radius: 90px;
  flex: 0.25;
`;

const ScreenContainer = styled(SafeArea)`
  flex: 1;
`;

const MazeImage = styled.Image`
  height: 100%;
  width: 100%;
`;

export const MazeScreen = ({ children, ...props }) => {
  const [path, setPath] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [containerWidth, setContainerWidth] = useState(0);
  const [containerHeight, setContainerHeight] = useState(0);
  const { mazeImage, socket, status } = useContext(UDPContext);

  const handleLayout = () => {
    const { width, height } = Dimensions.get("window");
    setContainerWidth(width);
    setContainerHeight(height);
  };

  const onDecline = () => {
    setIsModalVisible(false);
  };

  const onAccept = () => {
    if (status["connection"]) {
      sendTakePic(socket);
    } else {
      Toast.show("Please connect first.", {
        duration: Toast.durations.SHORT,
        backgroundColor: "red", // Change the background color to red
        textColor: "white",
        animation: true,
        hideOnPress: true,
      });
    }
    setIsModalVisible(false);
  };

  return (
    <ScreenContainer>
      <MazeContainer>
        <MazeImage
          source={{
            uri: mazeImage,
          }}
          resizeMode="contain"
        />
      </MazeContainer>
      <TakePictureModal
        visible={isModalVisible}
        onRequestClose={() => onDecline()}
        onAccept={() => onAccept()}
      />
      <ButtonContainer>
        <TouchableOpacity
          onPress={() => {
            setIsModalVisible(!isModalVisible);
          }}
        >
          <CircleWithInnerRing />
        </TouchableOpacity>
      </ButtonContainer>
    </ScreenContainer>
  );
};
