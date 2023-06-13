import React from "react";
import styled from "styled-components";
import { ActivityIndicator, Colors } from "react-native-paper";

const Loading = styled(ActivityIndicator)`
  margin-left: -25px;
`;
const LoadingContainer = styled.View`
  position: absolute;
  top: 50%;
  left: 50%;
`;

export const LoadingWheel = () => {
  return (
    <LoadingContainer>
      <Loading size={50} animating={true} color={Colors.blue300} />
    </LoadingContainer>
  );
};
