import {useNavigation} from '@react-navigation/native';
import React, {useState, useEffect} from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StatusBar,
  StyleSheet,
  Dimensions,
  PixelRatio,
  TextInput,
  Button,
  Image,
} from 'react-native';

const {width: windowWidth, height: windowHeight} = Dimensions.get('window');
const scale = PixelRatio.get();

const bg = require('./src/bg/bg2.png');
const userIcon = require('./src/user.png');
const userRoleIcon = require('./src/id-card.png');
const navigatorIcon_1 = require('./src/bg/oku.png');
const navigatorIcon_2 = require('./src/bg/schedIcon.png');
const navigatorIcon_3 = require('./src/bg/medIcon.png');
const navigatorIcon_4 = require('./src/bg/hospitalicon.png');
const bar = require('./src/bg/barIcon.png');

const username = '';
const role = '';

const home = () => {
  const navigation = useNavigation();

  return (
    <View style={styles.container}>
      <StatusBar hidden={true} />
      <Image source={bg} style={styles.bg} />

      <View style={styles.margin} />

      <TouchableOpacity style={styles.content} activeOpacity={1}>
        {/* Content View */}
        <Text
          style={{
            marginRight: 200,
            fontSize: scale * 10,
            color: 'white',
            marginBottom: 15,
          }}>
          Categories
        </Text>
        <TouchableOpacity
          style={styles.navigator_style}
          onPress={() => {
            navigation.navigate('medicalReport');
          }}
          activeOpacity={0.75}>
          <Image source={navigatorIcon_1} style={styles.navigatorIcon_style} />
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.navigator_style}
          onPress={() => {
            navigation.navigate('schedule');
          }}
          activeOpacity={0.75}>
          <Image source={navigatorIcon_2} style={styles.navigatorIcon_style} />
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.navigator_style}
          onPress={() => {
            navigation.navigate('medIder');
          }}
          activeOpacity={0.75}>
          <Image source={navigatorIcon_3} style={styles.navigatorIcon_style} />
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.navigator_style}
          onPress={() => {
            navigation.navigate('location');
          }}
          activeOpacity={0.75}>
          <Image source={navigatorIcon_4} style={styles.navigatorIcon_style} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.bar} activeOpacity={1}>
          <Image source={bar} style={styles.barStyle} />
        </TouchableOpacity>
      </TouchableOpacity>
    </View>
  );
};

export default home;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-start',
  },
  bg: {
    width: windowWidth,
    height: windowHeight,
    position: 'absolute',
    zIndex: -1,
  },
  header: {
    width: windowWidth,
    height: windowHeight * 0.25,
    justifyContent: 'center',
    alignItems: 'flex-start',
    backgroundColor: 'white',
  },
  headerText: {
    fontSize: scale * 15,
    fontFamily: 'sans-serif-light',
    fontWeight: 'bold',
    color: 'black',
  },
  margin: {
    margin: 120,
  },
  content: {
    width: windowWidth,
    height: windowHeight * 0.75,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 30,
    backgroundColor: 'rgb(142, 175, 218)',
    borderTopLeftRadius: 70,
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  navigator_style: {
    width: windowWidth * 0.4,
    height: windowWidth * 0.4,
    borderRadius: (windowWidth * 0.35) / 4,
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
    margin: 15,
  },
  navigatorIcon_style: {
    width: windowWidth * 0.65,
    height: windowWidth * 0.65,
  },
  profilePic: {
    width: windowWidth * 0.15,
    height: windowWidth * 0.15,
    marginHorizontal: 20,
  },
  profileInfo: {
    width: windowWidth,
    flexDirection: 'column',
    marginVertical: 10,
  },
  barStyle: {
    width: windowWidth * 0.85,
    height: windowHeight * 0.35,
    //backgroundColor: 'rgb(7, 61, 143)',
  },
  bar: {
    width: windowWidth * 0.85,
    height: windowHeight * 0.15,
  },
});
