import React, { useContext } from "react";
import {
  createStackNavigator,
  TransitionPresets,
} from "@react-navigation/stack";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { Ionicons } from "@expo/vector-icons";
import { Colors, Avatar } from "react-native-paper";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import styled from "styled-components/native";

import { SettingsScreen } from "../../features/settings/settings.screen";
import { MazeScreen } from "../../features/maze/screens/maze.screen";
import { SafeArea } from "../../components/utility/safe-area.component";
import { MainMenu } from "../../features/main-menu/screens/main-menu.screen";
import { Text } from "../../components/typography/text.component";
import { Spacer } from "../../components/spacer/spacer.component";

const TitleContainer = styled.View`
  flex-direction: row;
  align-items: center;
`;

const createScreenOptions = ({ route }) => {
  const headerShown = route.name === "Maze" ? true : false;
  const iconName = TAB_ICON[route.name];
  let profile = {};

  return {
    ...profile,
    tabBarIcon: ({ size, color }) => (
      <MaterialCommunityIcons name={iconName} size={size} color={color} />
    ),
    headerShown: headerShown,
    tabBarActiveTintColor: "tomato",
    tabBarInactiveTintColor: "gray",
  };
};

const TAB_ICON = {
  "Main Menu": "menu",
  Maze: "camera",
  Settings: "cog",
};

const Tab = createBottomTabNavigator();

export const AppNavigator = () => (
  <Tab.Navigator screenOptions={createScreenOptions}>
    <Tab.Screen name="Main Menu" component={MainMenu} />
    <Tab.Screen name="Maze" component={MazeScreen} />
    <Tab.Screen name="Settings" component={SettingsScreen} />
  </Tab.Navigator>
);
