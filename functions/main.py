# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import db_fn

# The Firebase Admin SDK to access the Firebase Realtime Database and Cloud Messaging.
from firebase_admin import initialize_app, db, messaging

app = initialize_app()

# 채팅방에 새로운 채팅 추가됐을 때
@db_fn.on_value_created(
    reference = r"/chattings/messages/{roomID}/{messageID}",
    region = "asia-southeast1"
)
def onMessageCreated(event: db_fn.Event[db_fn.Change]):

    # 채팅방ID, 메시지ID, 작성자UID
    roomID = event.params['roomID']
    messageID = event.params['messageID']
    writer_uid = event.data['uid']
    print(f"채팅 정보: {roomID}, {messageID}")

    # 채팅방 이름 가져오기
    group_title_ref = db.reference(f'/chattings/rooms/{roomID}/title')
    group_title = group_title_ref.get()

    # 채팅 작성자 이름 가져오기
    writer_info_ref = db.reference(f'/users/{writer_uid}/name')
    writer_name = writer_info_ref.get()

    # 채팅방 참가자 목록 가져오기
    participants_ref = db.reference(f'/chattings/rooms/{roomID}/members')
    participants = participants_ref.get().keys()
    print(f"채팅방 참가자 목록: {participants}")

    # 채팅방 참가자 토큰 목록 가져오기
    tokens = []
    for uid in participants: 
        user_info_ref = db.reference(f'/users/{uid}/fcm-token')
        user_token = user_info_ref.get()
        if user_token == None:
            continue
        tokens.append(user_token)
    print(f"채팅방 참가자 토큰 목록: {tokens}")

    # 메시지 양식
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title = f"{group_title}",
            body = f"{writer_name}:\n{event.data['content']}",
        ),
        tokens=tokens,
    )

    # Send message
    response = messaging.send_multicast(message)
    # Response
    print(f'{response.success_count} messages were sent successfully')

    
# 모임 참가상태 바뀌었을 때
@db_fn.on_value_written(
    reference = r"/posts/{postID}/participants/{userID}",
    region = "asia-southeast1"
)
def onParticipantsChange(event: db_fn.Event[db_fn.Change]):

    # 채팅방ID, 메시지ID, 작성자UID
    postID = event.params['postID']
    userID = event.params['userID']
    print(f"참가 변경됨: {postID}, {userID}")

    print(f"이전 데이터: {event.data.before}")
    print(f"이후 데이터: {event.data.after}")