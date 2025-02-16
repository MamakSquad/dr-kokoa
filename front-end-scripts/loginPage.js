import React, {useState} from 'react';
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
  Alert,
} from 'react-native';

const {width: windowWidth} = Dimensions.get('window');
const scale = PixelRatio.get();

const App = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');

  const handleRegister = async () => {
    if (!username || !password || !phone) {
      Alert.alert('Error', 'All fields are required');
      return;
    }

    const payload = {username, password, phone};

    try {
      const response = await fetch('https://dr-kokoa.onrender.com/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        Alert.alert('Success', 'Registration successful');
      } else {
        Alert.alert('Error', data.message || 'Registration failed');
      }
    } catch (error) {
      Alert.alert('Error', 'Something went wrong. Please try again.');
    }
  };

  return (
    <View style={styles.container}>
      <StatusBar hidden={true} />
      <View style={styles.header}>
        <Text style={styles.headerText}>DR KOKOA</Text>
      </View>
      <View style={styles.content}>
        <TextInput
          style={styles.inputBG}
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
        />
        <TextInput
          style={styles.inputBG}
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        <TextInput
          style={styles.inputBG}
          placeholder="Phone Number"
          value={phone}
          onChangeText={setPhone}
          keyboardType="phone-pad"
        />
        <TouchableOpacity style={styles.button} onPress={handleRegister}>
          <Text style={styles.buttonText}>Register</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default App;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'rgb(200,200,200)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  header: {
    width: '100%',
    height: '10%',
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
  },
  headerText: {
    color: 'black',
    fontSize: scale * 18,
  },
  content: {
    width: '80%',
    alignItems: 'center',
  },
  inputBG: {
    width: '100%',
    padding: 12,
    marginVertical: 10,
    backgroundColor: 'white',
    borderRadius: 10,
    elevation: 2,
  },
  button: {
    marginTop: 15,
    backgroundColor: 'black',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 10,
    alignItems: 'center',
    width: '100%',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
  },
});
