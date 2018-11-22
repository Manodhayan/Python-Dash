from firebase import firebase
firebase = firebase.FirebaseApplication('https://hospital-ambience.firebaseio.com', None)
result = firebase.get('/Manodhayan Kathamuthu', None)
print (result)
