#!/usr/bin/env python3

from rediscluster import RedisCluster
import argparse
import configparser
import os

def get_redis_config():
    """
    Read Redis configuration from config.properties file
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'properties', 'config.properties')
    config.read(config_path)
    
    return {
        'host': config.get('Redis', 'host'),
        'port': int(config.get('Redis', 'port')),
        'password': config.get('Redis', 'password')
    }

def delete_keys_with_prefix(host, port, password, prefix):
    """
    Delete all keys with the specified prefix from Redis cluster
    """
    # Initialize Redis cluster connection
    startup_nodes = [{"host": host, "port": port}]
    rc = RedisCluster(
        startup_nodes=startup_nodes,
        password=password,
        decode_responses=True
    )
    
    try:
        # Use scan_iter to find keys matching the prefix
        keys_to_delete = []
        
        # Get all keys matching the prefix
        for key in rc.scan_iter(match=f"{prefix}*", count=100):
            keys_to_delete.append(key)
        
        if not keys_to_delete:
            print(f"No keys found with prefix '{prefix}'")
            return
        
        print(f"Found {len(keys_to_delete)} keys with prefix '{prefix}':")
        
        # Print and delete keys in a single loop
        for key in keys_to_delete:
            print(f"- {key}")
            rc.delete(key)
        
        print(f"\nSuccessfully deleted {len(keys_to_delete)} keys with prefix '{prefix}'")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        rc.close()

def main():
    parser = argparse.ArgumentParser(description='Delete Redis keys with specified prefix')
    parser.add_argument('--prefix', default='test', help='Key prefix to delete')
    
    args = parser.parse_args()
    
    # Get Redis configuration from config file
    redis_config = get_redis_config()
    
    delete_keys_with_prefix(redis_config['host'], redis_config['port'], redis_config['password'], args.prefix)

if __name__ == "__main__":
    main() 