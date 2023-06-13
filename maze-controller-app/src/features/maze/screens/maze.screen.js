import React, { useRef, useState, useEffect, useContext } from "react";
import {
  PanResponder,
  View,
  StyleSheet,
  Dimensions,
  Image,
} from "react-native";
import Svg, { Polyline, Defs, ClipPath, Rect } from "react-native-svg";
import styled from "styled-components";
import { SafeArea } from "../../../components/utility/safe-area.component";
import { UDPContext } from "../../../services/udp-controls/udp-controls.context";

const MazeContainer = styled(SafeArea)`
  justify-content: center;
  align-items: center;
  flex: 1;
`;

const MazeImage = styled.Image`
  height: 100%;
  width: 100%;
`;

const DrawingContainer = styled.View`
  justify-content: center;
  align-items: center;
  flex: 1;
`;

const GesturePath = ({
  path,
  color,
  containerWidth,
  containerHeight,
  mazeImage,
}) => {
  const { width, height } = Dimensions.get("window");

  const points = path.map((p) => `${p.x},${p.y}`).join(" ");
  return (
    <Svg>
      <Defs>
        <ClipPath id="imageClip">
          <Rect x="0" y="0" width={containerWidth} height={containerHeight} />
        </ClipPath>
      </Defs>
      <Image source={{ uri: mazeImage }} alt="WebSocket Image" />
      <Polyline points={points} fill="none" stroke={color} strokeWidth="3" />
    </Svg>
  );
};

const GestureRecorder = ({ onPathChanged }) => {
  const pathRef = useRef([]);

  const panResponder = useRef(
    PanResponder.create({
      onMoveShouldSetPanResponder: () => true,
      onPanResponderGrant: () => {
        pathRef.current = [];
      },
      onPanResponderMove: (event) => {
        pathRef.current.push({
          x: event.nativeEvent.locationX,
          y: event.nativeEvent.locationY,
        });
        // Uncomment the next line to draw the path as the user is performing the touch. (A new array must be created so setState recognises the change and re-renders the App)
        onPathChanged([...pathRef.current]);
      },
      onPanResponderRelease: () => {
        onPathChanged([...pathRef.current]);
      },
    })
  ).current;

  return <View style={StyleSheet.absoluteFill} {...panResponder.panHandlers} />;
};

export const MazeScreen = () => {
  const [path, setPath] = useState([]);
  const [containerWidth, setContainerWidth] = useState(0);
  const [containerHeight, setContainerHeight] = useState(0);
  const { mazeImage } = useContext(UDPContext);

  const handleLayout = () => {
    const { width, height } = Dimensions.get("window");
    setContainerWidth(width);
    setContainerHeight(height);
  };

  return (
    <MazeContainer>
      <MazeImage
        source={{
          uri: mazeImage,
        }}
        resizeMode="contain"
      />
    </MazeContainer>

    // <DrawingContainer>
    //   <MazeContainer onLayout={handleLayout}>
    //     <GesturePath
    //       path={path}
    //       color="green"
    //       containerWidth={containerWidth}
    //       containerHeight={containerHeight}
    //       mazeImage={mazeImage}
    //     />
    //     <GestureRecorder onPathChanged={setPath} />
    //   </MazeContainer>
    // </DrawingContainer>
  );
};
