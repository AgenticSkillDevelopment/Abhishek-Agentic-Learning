# video_mcp_tool/server/video_server.py

# import os
# import sys
# import subprocess
# from mcp.server.fastmcp import FastMCP
# from core import main as core_main
# from core.main import main

# # Optional: Install core package dynamically (skip if already installed)
# CORE_PACKAGE = "core-0.0.0.tar.gz"
# if not os.path.exists("core"):
#     subprocess.check_call([
#         sys.executable, "-m", "pip", "install", os.path.abspath(CORE_PACKAGE)
#     ])

# # Start MCP server
# mcp = FastMCP(name="video_detection_server")

# @mcp.tool()
# async def run_detection(source: str = " /home/abhishek/Downloads/video(248)_normal_part000.mp4", targets: str = "Eating") -> str:
#     """
#     Run ONNX-based action detection.
#     :param source: Path to video file, webcam, or RTSP URL
#     :param targets: Comma-separated target classes (e.g., "Eating,Fighting")
#     :return: Status string
#     """
#     target_list = [cls.strip() for cls in targets.split(",")]
#     core_main.main(source, target_list)
#     return f"✅ Detection complete. Snapshots saved in 'snapshots/'"

# if __name__ == "__main__":
#     print("🎥 MCP server for video detection running...")
#     mcp.run(transport="streamable-http")

# import os
# import sys
# import subprocess
# from typing import List
# from mcp.server.fastmcp import FastMCP
# from core import main as core_main
# from core.main import main
# # Set default MCP server port
# os.environ["PORT"] = "8000"

# # Create MCP server instance
# mcp = FastMCP(name="video_action_detector")

# @mcp.tool()
# async def run_video_detection(video_source: str = "/home/abhishek/Downloads/video(248)_normal_part000.mp4", target_classes: List[str] = ["Eating"]) -> str:
#     try:
#         CORE_PACKAGE = "core-0.0.0.tar.gz"
#         subprocess.check_call([sys.executable, "-m", "pip", "install", os.path.abspath(CORE_PACKAGE)])
#         install_msg = f"[✔] Installed core package from: {CORE_PACKAGE}"

#         subprocess.run([
#             sys.executable,
#             "-c",
#             (
#                 "from core import main as core_main; "
#                 f"core_main.main('{video_source}', {target_classes})"
#             )
#         ], capture_output=True, text=True, check=True)

#         snapshot_dir = os.path.abspath("snapshots")
#         if not os.path.exists(snapshot_dir):
#             return f"{install_msg}\n[⚠️] Detection completed, but no 'snapshots/' directory was created."

#         snapshot_files = os.listdir(snapshot_dir)
#         if not snapshot_files:
#             return f"{install_msg}\n[📂] Snapshots folder exists but is empty: {snapshot_dir}"

#         return (
#             f"{install_msg}\n"
#             f"[🎬] Detection completed on: {video_source}\n"
#             f"[📸] Snapshots saved to: {snapshot_dir}\n"
#             f"[🎯] Classes detected: {', '.join(target_classes)}"
#         )

#     except subprocess.CalledProcessError as e:
#         return f"[❌] Error during detection pipeline: {e}"

#     except Exception as e:
#         return f"[❌] Unexpected error: {e}"


# # Run the MCP server
# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")

# import os
# import sys
# import subprocess
# from mcp.server.fastmcp import FastMCP
# from core import main as core_main
# from core.main import main

# # Optional: Install core package dynamically (skip if already installed)
# CORE_PACKAGE = "core-0.0.0.tar.gz"
# if not os.path.exists("core"):
#     subprocess.check_call([
#         sys.executable, "-m", "pip", "install", os.path.abspath(CORE_PACKAGE)
#     ])

# # Ensure results directory exists (e.g., for CSV or logs)
# RESULTS_DIR = "results"
# os.makedirs(RESULTS_DIR, exist_ok=True)

# # Start MCP server
# mcp = FastMCP(name="video_detection_server")

# @mcp.tool()
# async def run_detection(source: str = "/home/abhishek/Downloads/video(248)_normal_part000.mp4", targets: str = "Eating") -> str:
#     """
#     Run ONNX-based action detection.
#     :param source: Path to video file, webcam, or RTSP URL
#     :param targets: Comma-separated target classes (e.g., "Eating,Fighting")
#     :return: Status string
#     """
#     try:
#         # Clean and parse class list
#         target_list = [cls.strip() for cls in targets.split(",")]

#         # Run the detection
#         core_main.main(source, target_list)

#         return (
#             f"✅ Detection complete.\n"
#             f"📂 Snapshots saved in 'snapshots/'.\n"
#             f"📁 Results directory ensured at './{RESULTS_DIR}/'."
#         )
#     except Exception as e:
#         return f"❌ Detection failed: {str(e)}"

# if __name__ == "__main__":
#     print("🎥 MCP server for video detection running...")
#     mcp.run(transport="streamable-http")

# import os
# import sys
# import subprocess
# from mcp.server.fastmcp import FastMCP
# from core import main as core_main

# # Install core package
# CORE_PACKAGE = "core-0.0.0.tar.gz"
# if not os.path.exists("core"):
#     subprocess.check_call([
#         sys.executable, "-m", "pip", "install", os.path.abspath(CORE_PACKAGE)
#     ])

# mcp = FastMCP(name="video_detection_server")

# @mcp.tool()
# async def run_detection(source: str = "/home/abhishek/Downloads/video(248)_normal_part000.mp4", targets: str = "Eating") -> str:
#     """
#     Run ONNX-based action detection.
#     """
#     # Create snapshots directory if not exists
#     os.makedirs("snapshots", exist_ok=True)

#     target_list = [cls.strip() for cls in targets.split(",")]
#     core_main.main(source, target_list)

#     if not os.listdir("snapshots"):
#         return f"🟡 No matching activity found for: {targets}."

#     return f"✅ Detection complete for {targets}. Snapshots saved in 'snapshots/'"

# if __name__ == "__main__":
#     print("🎥 MCP server for video detection running...")
#     mcp.run(transport="streamable-http")

import os
import sys
import subprocess
from typing import List
from mcp.server.fastmcp import FastMCP
from core import main as core_main

# === Constants ===
SNAPSHOT_DIR = "snapshots"
CORE_PACKAGE = "core-0.0.0.tar.gz"

# === Ensure snapshot directory exists ===
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# === Install core package if not already installed ===
if not os.path.exists("core"):
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", os.path.abspath(CORE_PACKAGE)
    ])

# === Create MCP server ===
mcp = FastMCP(name="video_action_mcp")

@mcp.tool()
async def run_detection(source: str = "/home/abhishek/Downloads/video(248)_normal_part000.mp4 ", targets: str = "Fighting,Eating,Talking") -> str:
    """
    Run ONNX-based human action detection from video.
    :param source: Path to the video file or "webcam"
    :param targets: Comma-separated class names (e.g. "Eating,Fighting")
    :return: Status message with snapshot info
    """
    try:
        # === Prepare parameters ===
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        target_list = [cls.strip() for cls in targets.split(",")]

        # === Call main detection pipeline ===
        core_main.main(source, target_list)

        # === Snapshot Reporting ===
        snapshot_files = os.listdir(SNAPSHOT_DIR)
        if not snapshot_files:
            return f"🟡 Detection completed but no snapshots were generated for: {targets}."

        snapshot_lines = "\n".join(f"📸 {snap}" for snap in snapshot_files)
        return (
            f"✅ Detection complete on video: {source}\n"
            f"🎯 Target Classes: {', '.join(target_list)}\n"
            f"📁 Snapshots folder: {SNAPSHOT_DIR}\n"
            f"{snapshot_lines}"
        )

    except subprocess.CalledProcessError as e:
        return f"❌ Error during model core package setup: {e}"
    except Exception as e:
        return f"❌ Detection failed due to unexpected error: {e}"

# === Start MCP Server ===
if __name__ == "__main__":
    print("🎥 MCP server for ONNX-based video action detection running...")
    mcp.run(transport="streamable-http")


# import os
# import sys
# import subprocess
# from mcp.server.fastmcp import FastMCP
# from core import main as core_main

# # Ensure snapshot folder exists
# SNAPSHOT_DIR = "snapshots"
# os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# # Install core package if needed
# CORE_PACKAGE = "core-0.0.0.tar.gz"
# if not os.path.exists("core"):
#     subprocess.check_call([
#         sys.executable, "-m", "pip", "install", os.path.abspath(CORE_PACKAGE)
#     ])

# mcp = FastMCP(name="video_detection_server")

# @mcp.tool()
# async def run_detection(source: str, targets: str) -> str:
#     target_list = [cls.strip() for cls in targets.split(",")]
#     core_main.main(source, target_list)  # assumes core/main.py handles saving to snapshots/
    
#     snapshot_files = os.listdir(SNAPSHOT_DIR)
#     if not snapshot_files:
#         return "✅ Detection done, but no snapshots were saved."

#     snapshots_info = "\n".join(f"📸 {snap}" for snap in snapshot_files)
#     return f"✅ Detection complete. Snapshots:\n{snapshots_info}"

# if __name__ == "__main__":
#     print("🎥 MCP server for video detection running...")
#     mcp.run(transport="streamable-http")
