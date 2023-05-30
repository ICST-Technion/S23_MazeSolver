import styled from "styled-components";

export const SectionSeperator = styled.View`
  border-bottom-color: lightgray;
  border-bottom-width: 1px;
  margin-left: 5%;
  margin-right: 5%;
`;

export const Section = styled.View`
  flex-direction: row;
  align-items: center;
  padding: ${(props) => props.theme.space[2]};
`;

export const SectionEnd = styled.View`
  flex: 1;
  flex-direction: row;
  justify-content: flex-end;
`;
