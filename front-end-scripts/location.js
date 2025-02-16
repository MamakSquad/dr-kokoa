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
  FlatList,
} from 'react-native';

const {width: windowWidth, height: windowHeight} = Dimensions.get('window');
const scale = PixelRatio.get();

const backButton = require('./src/bg/homeIcon.png');
const header = require('./src/bg/mapHeader.png');
const bg = require('./src/bg/bg1.png');

const schedule = () => {
  const navigation = useNavigation();

  return (
    <View style={styles.container}>
      {/* header view */}
      <TouchableOpacity style={styles.header} activeOpacity={1}>
        <Image source={header} style={styles.headerImage} />
      </TouchableOpacity>

      <View style={styles.margin} />

      <View style={styles.content}>
        <Image source={bg} style={styles.bg} />
        {/* content view */}
        <TouchableOpacity
          style={styles.mapContainer}
          activeOpacity={1}></TouchableOpacity>
        <TouchableOpacity style={styles.Button} activeOpacity={1}>
          <Text>Open Maps</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default schedule;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
  },
  header: {
    position: 'absolute',
  },
  headerImage: {
    width: 500,
    height: 700,
  },
  margin: {
    margin: 115,
  },
  bg: {
    width: windowWidth,
    height: windowHeight,
    position: 'absolute',
  },
  content: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  mapContainer: {
    width: windowWidth * 0.75,
    height: windowHeight * 0.5,
    backgroundColor: 'gray',
    marginBottom: 125,
    borderRadius: 35,
  },
  Button: {
    width: windowWidth * 0.65,
    height: windowHeight * 0.075,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'white',
    borderRadius: 20,
  },
});
