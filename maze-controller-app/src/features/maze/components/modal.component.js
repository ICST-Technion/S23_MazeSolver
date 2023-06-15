import React from "react";
import { Modal, View, Text, TouchableOpacity } from "react-native";
import styled from "styled-components/native";

export const TakePictureModal = ({ visible, onRequestClose, onAccept }) => {
  return (
    <Modal
      visible={visible}
      onRequestClose={onRequestClose}
      transparent
      animationType="fade"
    >
      <ModalContainer>
        <ModalContent>
          <ModalText>{"Do you want to take a new maze picture?"}</ModalText>
          <ButtonContainer>
            <AcceptButton onPress={onAccept}>
              <ButtonText>Accept</ButtonText>
            </AcceptButton>
            <CancelButton onPress={onRequestClose}>
              <ButtonText>Cancel</ButtonText>
            </CancelButton>
          </ButtonContainer>
        </ModalContent>
      </ModalContainer>
    </Modal>
  );
};

const ModalContainer = styled(View)`
  flex: 1;
  background-color: rgba(0, 0, 0, 0.5);
  justify-content: center;
  align-items: center;
`;

const ModalContent = styled(View)`
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  align-items: center;
`;

const ModalText = styled(Text)`
  font-size: 18px;
  margin-bottom: 20px;
  text-align: center;
`;

const ButtonContainer = styled(View)`
  flex-direction: row;
  justify-content: center;
`;

const Button = styled(TouchableOpacity)`
  padding-vertical: 10px;
  padding-horizontal: 20px;
  border-radius: 8px;
  margin-horizontal: 10px;
`;

const AcceptButton = styled(Button)`
  background-color: #2196f3;
`;

const CancelButton = styled(Button)`
  background-color: #e91e63;
`;

const ButtonText = styled(Text)`
  color: white;
  font-size: 16px;
  font-weight: bold;
`;
