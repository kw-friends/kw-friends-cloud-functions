# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import db_fn

# The Firebase Admin SDK to access the Firebase Realtime Database and Cloud Messaging.
from firebase_admin import initialize_app, db, messaging

app = initialize_app()

#registration_token = 'token'

@db_fn.on_value_created(
    reference = r"/chattings/messages/{roomID}/{messageID}",
    region = "asia-southeast1"
)
def onMessageCreated(event: db_fn.Event[db_fn.Change]):

    message = messaging.Message(
        notification=messaging.Notification(
            title = event.data['uid'],
            body = event.data['content'],
        ),
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

    
