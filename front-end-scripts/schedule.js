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
const header = require('./src/bg/appointmentHeader.png');
const bg = require('./src/bg/bg1.png');

const schedule = () => {
  const navigation = useNavigation();

  const reminders = [
    {
      title: 'test1',
    },
    {
      title: 'test2',
    },
  ];

  const Reminder = ({item}) => {
    <TouchableOpacity style={styles.reminder}>
      <Text>{item}</Text>
    </TouchableOpacity>;
  };

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
        <FlatList
          data={reminders}
          renderItem={({item}) => <Reminder item={item.title} />}
        />
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
    margin: 45,
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
  backButton_style: {
    width: windowWidth * 0.1,
    height: windowWidth * 0.1,
    color: 'white',
  },
  reminder: {
    width: 'auto',
    height: '20%',
    backgroundColor: 'rgb(0, 77, 107)',
  },
});
