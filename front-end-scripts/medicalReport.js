import {useNavigation} from '@react-navigation/native';
import React, {useState} from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
  PixelRatio,
  Image,
  Modal,
} from 'react-native';
import {matrixTransform} from 'react-native-svg/lib/typescript/elements/Shape';

const {width: windowWidth, height: windowHeight} = Dimensions.get('window');
const scale = PixelRatio.get();

const backIcon = require('./src/angle-left.png');
const header = require('./src/bg/assistantHeader.png');
const navigatorIcon_1 = require('./src/bg/eatsymbol.png');
const navigatorIcon_2 = require('./src/bg/healthsymbol.png');
const navigatorIcon_3 = require('./src/bg/bathsymbol.png');
const navigatorIcon_4 = require('./src/bg/bedsymbol.png');
const bg = require('./src/bg/bg1.png');

const MedicalReport = () => {
  const navigation = useNavigation();
  const [modalVisible, setModalVisible] = useState(false);

  return (
    <View style={styles.container}>
      {/* header view */}
      <TouchableOpacity style={styles.header} activeOpacity={1}>
        <Image source={header} style={styles.headerImage} />
      </TouchableOpacity>
      <View style={styles.margin} />
      {/* Content */}
      <View style={styles.content}>
        <Image source={bg} style={styles.bg} />
        <TouchableOpacity
          style={styles.navigator_style}
          onPress={() => setModalVisible(true)}
          activeOpacity={0.75}>
          <Image source={navigatorIcon_1} style={styles.navigatorIcon_style} />
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.navigator_style}
          onPress={() => setModalVisible(true)}
          activeOpacity={0.75}>
          <Image source={navigatorIcon_2} style={styles.navigatorIcon_style} />
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.navigator_style}
          onPress={() => setModalVisible(true)}
          activeOpacity={0.75}>
          <Image source={navigatorIcon_3} style={styles.navigatorIcon_style} />
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.navigator_style}
          onPress={() => setModalVisible(true)}
          activeOpacity={0.75}>
          <Image source={navigatorIcon_4} style={styles.navigatorIcon_style} />
        </TouchableOpacity>
      </View>

      {/* Modal */}
      <Modal visible={modalVisible} animationType="fade" transparent={true}>
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text style={styles.modalText}>Text1</Text>
            <Text style={styles.modalText}>Text2</Text>
            <Text style={styles.modalText}>Text3</Text>
            <TouchableOpacity
              onPress={() => setModalVisible(false)}
              style={styles.closeButton}>
              <Text style={styles.closeButtonText}>Close</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
};

export default MedicalReport;

const styles = StyleSheet.create({
  container: {flex: 1, alignItems: 'flex-start', justifyContent: 'flex-start'},
  header: {
    position: 'absolute',
  },
  headerImage: {
    width: 500,
    height: 700,
  },
  margin: {
    margin: 124,
  },
  content: {
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingBottom: 80,
  },
  bg: {
    width: windowWidth,
    height: windowHeight,
    position: 'absolute',
  },
  navigator_style: {
    width: windowWidth * 0.4,
    height: windowHeight * 0.25,
    backgroundColor: 'rgb(12, 188, 211)',
    borderRadius: (windowWidth * 0.35) / 5,
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
    margin: 20,
    elevation: 5,
  },
  navigatorIcon_style: {
    width: windowWidth * 0.55,
    height: windowWidth * 0.5,
  },
  backButton_style: {
    width: windowWidth * 0.1,
    height: windowWidth * 0.1,
    color: 'white',
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalContent: {
    width: windowWidth * 0.8,
    padding: 20,
    backgroundColor: 'white',
    borderRadius: 10,
    alignItems: 'center',
  },
  modalText: {
    fontSize: scale * 12,
    marginVertical: 5,
  },
  closeButton: {
    marginTop: 20,
    paddingVertical: 10,
    paddingHorizontal: 20,
    backgroundColor: 'rgb(83, 81, 245)',
    borderRadius: 5,
  },
  closeButtonText: {
    color: 'white',
    fontSize: scale * 12,
    fontWeight: 'bold',
  },
});
