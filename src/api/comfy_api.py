"""ComfyUI API interaction module."""
import json
import urllib.request
from src.config.config import Config



def queue_prompt(prompt):
    """
    Queue a generation prompt to the server.

    Args:
        prompt (dict): JSON data for the prompt.

    Returns:
        dict: Response data containing prompt_id.
    """
    try:
        payload = {"prompt": prompt, "client_id": Config.comfy_client_id()}
        print("param is {}".format(payload))
        url = f"{Config.get_comfy_api_url()}/prompt"

        # Print curl command for debugging
        curl_cmd = (
            f"curl -X POST '{url}' "
            f"-H 'Content-Type: application/json' "
            f"-d '{json.dumps(payload, ensure_ascii=False)}'"
        )
        print("CURL 命令：\n" + curl_cmd)

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data)

        # Set HTTP proxy from configuration
        proxy_handler = urllib.request.ProxyHandler({"http": Config.get_proxy(), "https": Config.get_proxy()})
        opener = urllib.request.build_opener(proxy_handler)
        response = opener.open(req)

        return json.loads(response.read())
    except Exception as e:
        print(f"Error in queue_prompt: {e}")
        return None


def get_prompt_info(prompt_id):
    """
    Get prompt information for a specific prompt_id.

    Args:
        prompt_id (str): Unique identifier for the prompt.

    Returns:
        dict: JSON data containing prompt information.
    """
    try:
        url = f"{Config.get_comfy_api_url()}/prompt/{prompt_id}"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except Exception as e:
        print(f"Error in get_prompt_info: {e}")
        return None


def get_history(prompt_id):
    """
    Get generation history for a specific prompt ID.

    Args:
        prompt_id (str): Unique ID for the prompt.

    Returns:
        dict: JSON data containing history.
    """
    try:
        url = f"{Config.get_comfy_api_url()}/history/{prompt_id}"
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Error in get_history: {e}")
        return None


def get_image(image_id, history, prompt_id):
    """
    Get image data for a specific image ID.

    Args:
        image_id (str): Unique identifier for the image.
        history (dict): History data containing image information.
        prompt_id (str): ID of the prompt that generated the image.

    Returns:
        PIL.Image: Image object.
    """
    for node_id, node_output in history[prompt_id]['outputs'].items():
        if 'images' in node_output:
            for image in node_output['images']:
                # This step gets the image download URL
                # image['filename'] is the filename, supports multiple generations
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                if image_data:
                    return image_data