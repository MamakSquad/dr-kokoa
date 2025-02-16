// In App.js in a new project

import * as React from 'react';
import {View, Text, TouchableOpacity} from 'react-native';
import {NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';

import loginPage from './loginPage';
import home from './home';
import medicalReport from './medicalReport';
import schedule from './schedule';
import medicine_Identifier from './medical_identifier';
import location from './location';
import accountDetails from './acccountDetails';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="home"
        screenOptions={{headerShown: false}}>
        <Stack.Screen name="loginPage" component={loginPage} />
        <Stack.Screen name="home" component={home} />
        <Stack.Screen name="medicalReport" component={medicalReport} />
        <Stack.Screen name="schedule" component={schedule} />
        <Stack.Screen name="medIder" component={medicine_Identifier} />
        <Stack.Screen name="location" component={location} />
        <Stack.Screen name="accountDetails" component={accountDetails} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
