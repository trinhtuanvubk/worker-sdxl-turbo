import requests
import aiohttp
import asyncio
import base64
from PIL import Image
import io

API_key = ""

def get_runpod_job_id(prompt):
    """
    Synchronously get a job ID from RunPod API
    
    :param prompt: Text prompt for image generation
    :return: Job ID
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {API_key}"'
    }
    
    data = {
        'input': {"prompt": prompt}
    }
    
    response = requests.post('https://api.runpod.ai/v2/8bonj58vp5p1r3/run', 
                              headers=headers, 
                              json=data)
    
    return response.json().get('id')

async def stream_job_results(job_id):
    """
    Asynchronously stream job results for a given job ID
    
    :param job_id: Job ID to stream
    :return: Job results or None
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {API_key}"'
    }
    
    url = f'https://api.runpod.ai/v2/8bonj58vp5p1r3/status/{job_id}'
    
    async with aiohttp.ClientSession() as session:
        max_attempts = 30
        for attempt in range(max_attempts):
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                
                if data.get('status') == 'COMPLETED':
                    return data.get('output')
                elif data.get('status') == 'FAILED':
                    print("Job failed")
                    return None
                
                # Wait a bit before next attempt
                await asyncio.sleep(2)
        
        print("Max attempts reached")
        return None

async def main():

    # Get job ID synchronously
    job_id = get_runpod_job_id("a beautiful girl")

    # Stream results asynchronously
    if job_id:
        print(f"Job ID: {job_id}")
        output_base64 = await stream_job_results(job_id)
        
        if output_base64:
            print("Job completed successfully:")
            # print(output_base64)
        else:
            print("Failed to retrieve job results")

    # Replace 'base64_string' with your actual base64 string
    base64_string = output_base64
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    image.save("trash_image.jpg")


# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
