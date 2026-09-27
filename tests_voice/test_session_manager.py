from src.voice.session_manager import SessionManager

manager = SessionManager()

session_id = manager.create_session()


print("\nSession ID:")
print(session_id)


session = manager.get_session(
    session_id
)


print("\nSession:")
print(session)


manager.end_session(
    session_id
)


print("\nAfter ending:")
print(
    manager.get_session(session_id)
)