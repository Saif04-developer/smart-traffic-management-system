"""
Test script for recording workflow.
Simulates browser by fetching canvas data and sending frame captures.
"""

import requests
import json
import base64
import time
from PIL import Image, ImageDraw
import io

BASE_URL = 'http://127.0.0.1:5000'

def generate_test_frame(time_step):
    """Generate a simple test canvas frame (PNG)."""
    # Create a simple 600x500 image
    img = Image.new('RGB', (600, 500), color=(249, 249, 249))
    draw = ImageDraw.Draw(img)
    
    # Draw title
    draw.text((20, 20), f"Test Frame - Step {time_step}", fill=(0, 0, 0))
    
    # Draw simple network (4x4 grid)
    padding = 50
    step_size = 137.5
    
    for i in range(4):
        for j in range(4):
            x = padding + i * step_size
            y = padding + j * step_size
            # Draw intersection circle
            draw.ellipse([x-8, y-8, x+8, y+8], fill=(100, 200, 100), outline=(0, 0, 0))
            # Draw position label
            pos_id = i + j * 4
            draw.text((x+12, y), str(pos_id), fill=(0, 0, 0))
    
    # Draw roads
    for i in range(4):
        for j in range(4):
            x = padding + i * step_size
            y = padding + j * step_size
            if i < 3:
                next_x = padding + (i + 1) * step_size
                draw.line([(x, y), (next_x, y)], fill=(224, 224, 224), width=3)
            if j < 3:
                next_y = padding + (j + 1) * step_size
                draw.line([(x, y), (x, next_y)], fill=(224, 224, 224), width=3)
    
    # Convert to PNG bytes
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    png_bytes = buf.getvalue()
    
    # Convert to data URL
    b64 = base64.b64encode(png_bytes).decode('utf-8')
    return f'data:image/png;base64,{b64}'

def test_recording_workflow():
    """Test full recording workflow."""
    print("\n=== RECORDING WORKFLOW TEST ===\n")
    
    # Step 1: Start simulation
    print("1. Starting simulation...")
    start_resp = requests.post(f'{BASE_URL}/api/simulation/start', json={
        'name': 'Recording Test',
        'controller': 'fixed_time',
        'grid_size': 4,
        'arrival_rate': 0.15
    })
    print(f"   Status: {start_resp.json()['status']}")
    
    # Step 2: Start recording
    print("2. Starting recording...")
    rec_start = requests.post(f'{BASE_URL}/api/recording/start')
    print(f"   {rec_start.json()}")
    
    # Step 3: Simulate frame captures (user would do this via polling)
    print("3. Capturing test frames...")
    for frame_idx in range(10):
        # Generate test frame
        frame_data = generate_test_frame(frame_idx)
        
        # Send to server
        resp = requests.post(f'{BASE_URL}/api/recording/add-frame', json={
            'frame_data': frame_data
        })
        
        if resp.status_code == 200:
            print(f"   Frame {frame_idx}: OK")
        else:
            print(f"   Frame {frame_idx}: ERROR - {resp.text}")
        
        time.sleep(0.1)  # Simulate frame capture timing
    
    # Step 4: Check recording status
    print("4. Checking recording status...")
    status_resp = requests.get(f'{BASE_URL}/api/recording/status')
    status = status_resp.json()
    print(f"   Recording: {status['recording']}, Frames: {status['frames_captured']}")
    
    # Step 5: Stop recording (encode video)
    print("5. Stopping recording and encoding video...")
    stop_resp = requests.post(f'{BASE_URL}/api/recording/stop')
    if stop_resp.status_code == 200:
        stop_data = stop_resp.json()
        print(f"   Status: {stop_data['status']}")
        print(f"   Video path: {stop_data.get('video_path', 'N/A')}")
    else:
        print(f"   ERROR: {stop_resp.text}")
        return False
    
    # Step 6: Verify video file
    print("6. Verifying video file...")
    import os
    video_path = stop_data.get('video_path')
    if video_path and os.path.exists(video_path):
        file_size = os.path.getsize(video_path)
        print(f"   ✓ Video file exists: {os.path.basename(video_path)}")
        print(f"   ✓ File size: {file_size:,} bytes")
        return True
    else:
        print(f"   ✗ Video file not found")
        return False

if __name__ == '__main__':
    try:
        success = test_recording_workflow()
        print(f"\n=== TEST {'PASSED' if success else 'FAILED'} ===\n")
    except Exception as e:
        print(f"\n✗ Test error: {e}\n")
