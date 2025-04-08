# server.py
from mcp.server.fastmcp import FastMCP
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import logging
import sys
from fastapi import FastAPI
import uvicorn

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# Verify required environment variables
required_vars = ['BASE_URL_ECOM_V2', 'AUTHORIZATION', 'UUID']
for var in required_vars:
    if not os.getenv(var):
        logger.warning(f"Missing environment variable: {var}")
    else:
        logger.info(f"Found environment variable: {var}")

# Create FastAPI app
app = FastAPI()

# Create an MCP server
mcp = FastMCP("RestaurantMenuAPI", app=app)
logger.info("MCP Server initialized with name: Restaurant Menu API")

@mcp.tool()
async def get_restaurant_menu(restaurant_id: int, branch_id: int, brand_id: str) -> List[str]:
    """
    Fetch restaurant menu categories from the API.
    
    Args:
        restaurant_id: The ID of the restaurant
        branch_id: The ID of the branch
        brand_id: The ID of the brand
        
    Returns:
        List of category display texts
    """
    try:
        logger.info(f"Fetching menu categories for restaurant_id={restaurant_id}, branch_id={branch_id}, brand_id={brand_id}")
        
        # Get environment variables
        base_url = os.getenv('BASE_URL_ECOM_V2')
        authorization = os.getenv('AUTHORIZATION')
        uuid = os.getenv('UUID')
        
        if not all([base_url, authorization, uuid]):
            logger.error("Missing required environment variables")
            raise Exception('Missing required environment variables')
            
        # Prepare request payload
        payload = {
            "restaurant_id": restaurant_id,
            "branch_id": branch_id,
            "brand_id": brand_id,
            "is_pos": 2,
            "session_id": "uak84xaaez3zujkyn11io",
            "version": "0.1",
            "lang": "en",
            "source": "kiosk",
            "ui_request_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        logger.debug(f"Making API request to {base_url}/ecom/v1/restaurant-menu")
        
        # Make API request
        response = requests.post(
            f"{base_url}/ecom/v1/restaurant-menu",
            json=payload,
            headers={
                'Authorization': authorization,
                'UUID': uuid,
                'Content-Type': 'application/json'
            },
            verify=True
        )
        
        # Check response status
        response.raise_for_status()
        data = response.json()
        logger.debug("API request successful")
            
        if not data or not data.get('data'):
            logger.error("Invalid response structure received from API")
            raise Exception('Invalid response structure')
            
        menu_data = data['data']
        categories = []
        
        # Extract category display texts
        if menu_data.get('menu_type'):
            for menu in menu_data['menu_type']:
                if menu.get('menu_category'):
                    for category in menu['menu_category']:
                        display_text = category.get('category_display_text', '')
                        if category.get('category_display_text_v1'):
                            for lang_text in category['category_display_text_v1']:
                                if lang_text.get('language') == 'en':
                                    display_text = lang_text.get('display_text', display_text)
                                    break
                        if display_text:  # Only add non-empty categories
                            categories.append(display_text)
        
        logger.info(f"Found {len(categories)} categories")
        return categories
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching restaurant menu: {str(e)}")
        raise Exception(f"Error making API request: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching restaurant menu: {str(e)}")
        raise Exception(f"Error fetching restaurant menu: {str(e)}")

@mcp.tool()
async def get_category_items(restaurant_id: int, branch_id: int, brand_id: str, category_name: str) -> List[Dict[str, Any]]:
    """
    Fetch menu items for a specific category from the API.
    
    Args:
        restaurant_id: The ID of the restaurant
        branch_id: The ID of the branch
        brand_id: The ID of the brand
        category_name: The name of the category to get items for
        
    Returns:
        List of items with their details (display text, description, and price)
    """
    try:
        logger.info(f"Fetching items for category '{category_name}' (restaurant_id={restaurant_id}, branch_id={branch_id}, brand_id={brand_id})")
        
        # Get environment variables
        base_url = os.getenv('BASE_URL_ECOM_V2')
        authorization = os.getenv('AUTHORIZATION')
        uuid = os.getenv('UUID')
        
        if not all([base_url, authorization, uuid]):
            logger.error("Missing required environment variables")
            raise Exception('Missing required environment variables')
            
        # Prepare request payload
        payload = {
            "restaurant_id": restaurant_id,
            "branch_id": branch_id,
            "brand_id": brand_id,
            "is_pos": 2,
            "session_id": "uak84xaaez3zujkyn11io",
            "version": "0.1",
            "lang": "en",
            "source": "kiosk",
            "ui_request_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        logger.debug(f"Making API request to {base_url}/ecom/v1/restaurant-menu")
        
        # Make API request
        response = requests.post(
            f"{base_url}/ecom/v1/restaurant-menu",
            json=payload,
            headers={
                'Authorization': authorization,
                'UUID': uuid,
                'Content-Type': 'application/json'
            },
            verify=True
        )
        
        # Check response status
        response.raise_for_status()
        data = response.json()
        logger.debug("API request successful")
            
        if not data or not data.get('data'):
            logger.error("Invalid response structure received from API")
            raise Exception('Invalid response structure')
            
        menu_data = data['data']
        items = []
        found_categories = []  # For debugging
        
        # Find the category and its items
        if menu_data.get('menu_type'):
            for menu in menu_data['menu_type']:
                if menu.get('menu_category'):
                    for category in menu['menu_category']:
                        # Get category display text
                        display_text = category.get('category_display_text', '').strip()
                        if category.get('category_display_text_v1'):
                            for lang_text in category['category_display_text_v1']:
                                if lang_text.get('language') == 'en':
                                    display_text = lang_text.get('display_text', display_text).strip()
                                    break
                        
                        found_categories.append(display_text)  # Add to found categories for debugging
                        
                        # Check if this is the category we're looking for (case-insensitive and trimmed)
                        if display_text.lower() == category_name.strip().lower():
                            logger.info(f"Found matching category: {display_text}")
                            # Found the category, now get its items
                            if category.get('cat_items'):
                                for item in category['cat_items']:
                                    item_details = {
                                        'display_text': item.get('item_display_text', ''),
                                        'description': item.get('item_description', ''),
                                        'price': item.get('price', 0),
                                        'image': item.get('item_image', '')
                                    }
                                    items.append(item_details)
                            break
                
        if not items:
            logger.warning(f"No items found for category: {category_name}")
            logger.info(f"Available categories: {', '.join(found_categories)}")
            raise Exception(f'No items found for category: "{category_name}". Available categories: {", ".join(found_categories)}')
            
        logger.info(f"Found {len(items)} items in category '{category_name}'")
        return items
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching category items: {str(e)}")
        raise Exception(f"Error making API request: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching category items: {str(e)}")
        raise Exception(f"Error fetching category items: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Restaurant Menu MCP Server')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to listen on')
    args = parser.parse_args()
    
    logger.info("Starting Restaurant Menu API MCP Server...")
    logger.info("Server configuration:")
    logger.info(f"- Host: {args.host}")
    logger.info(f"- Port: {args.port}")
    logger.info(f"- Base URL: {os.getenv('BASE_URL_ECOM_V2', 'Not set')}")
    logger.info("- Available tools:")
    logger.info("  1. get_restaurant_menu: Fetch menu categories")
    logger.info("  2. get_category_items: Fetch items for a specific category")
    logger.info("\nServer is ready to accept requests...")
    
    # Run the server using uvicorn
    uvicorn.run(app, host=args.host, port=args.port)