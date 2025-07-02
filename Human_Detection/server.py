# # video_mcp_tool/server/video_server.py

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

import os
import sys
import subprocess
from typing import List
from mcp.server.fastmcp import FastMCP
from core import main as core_main
from core.main import main
# Set default MCP server port
os.environ["PORT"] = "8000"

# Create MCP server instance
mcp = FastMCP(name="video_action_detector")

@mcp.tool()
async def run_video_detection(video_source: str = "/home/abhishek/Downloads/video(248)_normal_part000.mp4", target_classes: List[str] = ["Eating"]) -> str:
    try:
        CORE_PACKAGE = "core-0.0.0.tar.gz"
        subprocess.check_call([sys.executable, "-m", "pip", "install", os.path.abspath(CORE_PACKAGE)])
        install_msg = f"[✔] Installed core package from: {CORE_PACKAGE}"

        subprocess.run([
            sys.executable,
            "-c",
            (
                "from core import main as core_main; "
                f"core_main.main('{video_source}', {target_classes})"
            )
        ], check=True)

        snapshot_dir = os.path.abspath("snapshots")
        if not os.path.exists(snapshot_dir):
            return f"{install_msg}\n[⚠️] Detection completed, but no 'snapshots/' directory was created."

        snapshot_files = os.listdir(snapshot_dir)
        if not snapshot_files:
            return f"{install_msg}\n[📂] Snapshots folder exists but is empty: {snapshot_dir}"

        return (
            f"{install_msg}\n"
            f"[🎬] Detection completed on: {video_source}\n"
            f"[📸] Snapshots saved to: {snapshot_dir}\n"
            f"[🎯] Classes detected: {', '.join(target_classes)}"
        )

    except subprocess.CalledProcessError as e:
        return f"[❌] Error during detection pipeline: {e}"

    except Exception as e:
        return f"[❌] Unexpected error: {e}"


# Run the MCP server
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
