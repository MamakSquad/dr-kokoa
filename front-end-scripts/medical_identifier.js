import {useNavigation} from '@react-navigation/native';
import React, {useState} from 'react';
import {launchImageLibrary} from 'react-native-image-picker';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
  PixelRatio,
  Image,
  Alert,
} from 'react-native';

const {width: windowWidth, height: windowHeight} = Dimensions.get('window');
const scale = PixelRatio.get();

const backButton = require('./src/bg/homeIcon.png');
const header = require('./src/bg/medIerHeader.png');
const bg = require('./src/bg/bg1.png');

const Location = () => {
  const [imageDisplay, setImageDisplay] = useState(null);
  const [detectedText, setDetectedText] = useState(null);
  const navigation = useNavigation();

  const openImagePicker = () => {
    const options = {
      mediaType: 'photo',
      includeBase64: false,
      maxHeight: 2000,
      maxWidth: 2000,
    };

    launchImageLibrary(options, response => {
      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('Image picker error: ', response.error);
      } else {
        let imageUri = response.assets?.[0]?.uri;
        if (imageUri) {
          setImageDisplay({uri: imageUri});
        }
      }
    });
  };

  const sendImageToBackend = async () => {
    if (!imageDisplay?.uri) {
      Alert.alert('No Image Selected', 'Please select an image first.');
      return;
    }

    const formData = new FormData();
    formData.append('image', {
      uri: imageDisplay.uri,
      type: 'image/jpeg', // Ensure this matches your image type
      name: 'image.jpg',
    });

    try {
      const response = await fetch('https://dr-kokoa.onrender.com/detect', {
        method: 'POST',
        body: formData, // No headers needed for multipart/form-data
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      console.log('Response from backend:', data);
    } catch (error) {
      console.error('Error sending image:', error);
      Alert.alert('Error', 'Failed to send image. Please try again.');
    }
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
        <TouchableOpacity style={styles.iconBox} activeOpacity={1}>
          {imageDisplay ? (
            <Image source={imageDisplay} style={styles.iconStyles} />
          ) : (
            <Text style={styles.iconBoxText}>
              Please Insert Image from Gallery
            </Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.galleryButton}
          onPress={openImagePicker}>
          <Text style={{color: 'white'}}>Open Gallery</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.galleryButton}
          onPress={sendImageToBackend}>
          <Text style={{color: 'white'}}>Generate Reminder</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default Location;

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
    margin: 25,
  },
  bg: {
    position: 'absolute',
  },
  content: {
    width: windowWidth * 0.75,
    alignItems: 'center',
    marginTop: 50,
    elevation: 3,
  },
  galleryButton: {
    width: windowWidth * 0.35,
    height: windowHeight * 0.05,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgb(22, 4, 124)',
    borderRadius: 20,
    marginVertical: 15,
  },
  backButton_style: {
    width: windowWidth * 0.3,
    height: windowWidth * 0.3,
    tintColor: 'white',
  },
  iconStyles: {
    width: windowWidth * 0.65,
    height: windowWidth * 0.45,
    borderRadius: 25,
  },
  iconBox: {
    width: windowWidth * 0.75,
    height: windowWidth * 0.55,
    backgroundColor: 'gray',
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 50,
  },
  iconBoxText: {
    color: 'white',
  },
});
