# SmartCache: An Optimized Content Caching System API
![Capture](https://github.com/user-attachments/assets/534783a3-f3f1-464a-be94-e07ba8b3bffc)


## Overview
SmartCache is a robust and efficient content caching system built using FastAPI. It is designed to cache responses from a simulated slow API and serve cached content with features like cache invalidation, stampede prevention, and statistics tracking. The system ensures optimal performance, thread safety, and efficient memory usage through a Least Recently Used (LRU) eviction policy.

## Features
- **GET Endpoint**: Retrieves content using the cache when available.
- **Simulated Slow API**: Mimics real-world scenarios with a 2-second delay.
- **In-Memory Cache**: Includes a default Time-to-Live (TTL) of 5 minutes.
- **Cache Invalidation**: Supports forced cache refresh for specific content.
- **Stampede Prevention**: Uses locks to handle concurrent requests efficiently.
- **Cache Statistics**: Tracks hit rate, miss rate, and current cache size.
- **Settings Update Endpoint**: Allows TTL and cache size adjustments at runtime.
- **Basic Eviction Policy**: Implements LRU eviction to manage cache size.
- **Thread-Safe**: Ensures safe concurrent access to the cache.

## Installation

### Prerequisites
- Python 3.8+

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/skidrow8852/smartcache.git
   cd smartcache
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   fastapi dev
   ```

## Usage

### Endpoints

#### 1. Retrieve Cached Content
**GET** `/content`
- Retrieves content from the cache or fetches it from the simulated slow API.

#### 2. Invalidate Cache
**POST** `/invalidate`
- **Body Parameter**:
  ```json
  {
    "key": "content"
  }
  ```
- Invalidates a specific cache entry by key.

#### 3. View Cache Statistics
**GET** `/stats`
- Returns statistics such as cache hits, misses, current size, and TTL.

#### 4. Update Cache Settings
**POST** `/settings`
- **Body Parameter**:
  ```json
  {
    "ttl": 300,
    "max_size": 100
  }
  ```
- Updates cache TTL and maximum size dynamically.

### Simulated Slow API
The application simulates a slow API that introduces a 2-second delay before returning data. This ensures a realistic caching scenario.

## Configuration
The cache has default settings:
- **TTL**: 5 minutes (300 seconds)
- **Max Size**: 100 entries

You can update these settings dynamically via the `/settings` endpoint.

## How It Works
1. **Cache Retrieval**: The system first checks the cache for the requested key.
2. **Stampede Prevention**: If the cache is empty, a lock prevents concurrent requests from overloading the slow API.
3. **Cache Update**: Responses are stored in the cache with a timestamp.
4. **LRU Eviction**: When the cache reaches its maximum size, the least recently used entry is removed.


