# import os
# import json

# class JSONMemory:
#     def __init__(self, file_path='memory/memory.json'):
#         self.file_path = os.path.abspath(file_path)
#         if not os.path.exists(self.file_path):
#             os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
#             with open(self.file_path, 'w') as f:
#                 json.dump({}, f)

#     def save(self, session_id, message):
#         print(f"[DEBUG] Saving message for {session_id}: {message}")
#         with open(self.file_path, 'r') as f:
#             data = json.load(f)
            
#         if session_id not in data:
#             data[session_id] = []
#         data[session_id].append(message)

#         with open(self.file_path, 'w') as f:
#             json.dump(data, f, indent=2)

#     def load(self, session_id):
#         with open(self.file_path, 'r') as f:
#             data = json.load(f)
#         history = data.get(session_id, [])
#         print(f"[DEBUG] Loaded memory for {session_id}: {history}")
#         return history

import os
import json

class JSONMemory:
    def __init__(self, file_path='memory/memory.json'):
        self.file_path = os.path.abspath(file_path)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            print("[DEBUG] Creating new memory.json")
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def save(self, session_id, message):
        print(f"[DEBUG] Saving message for {session_id}: {message}")
        with open(self.file_path, 'r') as f:
            data = json.load(f)

        if session_id not in data:
            data[session_id] = []
        data[session_id].append(message)

        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self, session_id):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        history = data.get(session_id, [])
        print(f"[DEBUG] Loaded memory for {session_id}: {history}")
        return history