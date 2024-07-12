// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from 'firebase/firestore';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD0IDgZk-QxdybIyKfhWs5xmoJtjBig0FE",
  authDomain: "droneapp-e3051.firebaseapp.com",
  databaseURL: "https://droneapp-e3051-default-rtdb.firebaseio.com",
  projectId: "droneapp-e3051",
  storageBucket: "droneapp-e3051.appspot.com",
  messagingSenderId: "898618416322",
  appId: "1:898618416322:web:9a48f7968236a7d0512f5b",
  measurementId: "G-WKJFT0RCM6"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db };