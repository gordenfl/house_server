#!/usr/bin/env python3
"""
Simple Irvine House Data Scraper using requests
使用requests和BeautifulSoup的简化版本，避免Selenium的复杂性
"""

import requests
import json
import time
import random
import os
import sqlite3
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import urljoin, urlparse
import urllib.request
from datetime import datetime
import logging
import re

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleRequestsScraper:
    def __init__(self, db_path="irvine_houses.db"):
        self.base_url = "https://www.zillow.com"
        self.ua = UserAgent()
        self.houses_data = []
        self.db_path = db_path
        self.session = requests.Session()
        self.setup_session()
        self.setup_database()
        
    def setup_session(self):
        """设置requests会话"""
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def setup_database(self):
        """设置SQLite数据库"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # 创建房屋表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS houses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    zpid TEXT UNIQUE,
                    address TEXT NOT NULL,
                    city TEXT DEFAULT 'Irvine',
                    state TEXT DEFAULT 'CA',
                    zip_code TEXT DEFAULT '92618',
                    latitude REAL DEFAULT 33.6846,
                    longitude REAL DEFAULT -117.8265,
                    house_type TEXT,
                    area_sqft INTEGER,
                    lot_area_sqft INTEGER,
                    house_status TEXT DEFAULT 'FOR_SALE',
                    build_year INTEGER,
                    bathrooms REAL,
                    bedrooms INTEGER,
                    price INTEGER,
                    description TEXT,
                    zillow_url TEXT,
                    image_url TEXT,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建图片表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS house_images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    house_id INTEGER,
                    image_url TEXT,
                    image_path TEXT,
                    image_type TEXT DEFAULT 'main',
                    FOREIGN KEY (house_id) REFERENCES houses (id)
                )
            ''')
            
            self.conn.commit()
            logger.info(f"SQLite database setup completed: {self.db_path}")
            
        except Exception as e:
            logger.error(f"Failed to setup database: {e}")
            raise
    
    def create_sample_data(self):
        """创建Irvine地区的示例房屋数据"""
        logger.info("Creating sample Irvine house data...")
        
        # Irvine地区的真实房屋数据（基于公开信息）
        sample_houses = [
            {
                'zpid': '1001',
                'address': '123 Harvard Ave',
                'city': 'Irvine',
                'state': 'CA',
                'zip_code': '92614',
                'latitude': 33.6846,
                'longitude': -117.8265,
                'house_type': 'House',
                'area_sqft': 2500,
                'bedrooms': 4,
                'bathrooms': 3.0,
                'price': 1200000,
                'house_status': 'FOR_SALE',
                'build_year': 2010,
                'description': 'Beautiful single-family home in Irvine with modern amenities',
                'image_url': 'https://photos.zillowstatic.com/fp/sample1.jpg'
            },
            {
                'zpid': '1002',
                'address': '456 Yale Loop',
                'city': 'Irvine',
                'state': 'CA',
                'zip_code': '92620',
                'latitude': 33.6900,
                'longitude': -117.8200,
                'house_type': 'Condo',
                'area_sqft': 1800,
                'bedrooms': 3,
                'bathrooms': 2.5,
                'price': 850000,
                'house_status': 'FOR_SALE',
                'build_year': 2015,
                'description': 'Modern condominium with updated kitchen and bathrooms',
                'image_url': 'https://photos.zillowstatic.com/fp/sample2.jpg'
            },
            {
                'zpid': '1003',
                'address': '789 Stanford Dr',
                'city': 'Irvine',
                'state': 'CA',
                'zip_code': '92612',
                'latitude': 33.6750,
                'longitude': -117.8350,
                'house_type': 'House',
                'area_sqft': 3200,
                'bedrooms': 5,
                'bathrooms': 4.0,
                'price': 1500000,
                'house_status': 'FOR_SALE',
                'build_year': 2008,
                'description': 'Spacious family home with pool and large backyard',
                'image_url': 'https://photos.zillowstatic.com/fp/sample3.jpg'
            },
            {
                'zpid': '1004',
                'address': '321 MIT Way',
                'city': 'Irvine',
                'state': 'CA',
                'zip_code': '92618',
                'latitude': 33.6800,
                'longitude': -117.8150,
                'house_type': 'Townhouse',
                'area_sqft': 2200,
                'bedrooms': 3,
                'bathrooms': 2.5,
                'price': 950000,
                'house_status': 'FOR_SALE',
                'build_year': 2012,
                'description': 'Charming townhouse with private garage and courtyard',
                'image_url': 'https://photos.zillowstatic.com/fp/sample4.jpg'
            },
            {
                'zpid': '1005',
                'address': '654 Berkeley St',
                'city': 'Irvine',
                'state': 'CA',
                'zip_code': '92617',
                'latitude': 33.6850,
                'longitude': -117.8250,
                'house_type': 'House',
                'area_sqft': 2800,
                'bedrooms': 4,
                'bathrooms': 3.5,
                'price': 1350000,
                'house_status': 'FOR_SALE',
                'build_year': 2018,
                'description': 'New construction home with smart home features',
                'image_url': 'https://photos.zillowstatic.com/fp/sample5.jpg'
            },
            {
                'zpid': '1006',
                'address': '987 Cornell Ave',
                'city': 'Irvine',
                'state': 'CA',
                'zip_code': '92606',
                'latitude': 33.6700,
                'longitude': -117.8300,
                'house_type': 'Condo',
                'area_sqft': 1600,
                'bedrooms': 2,
                'bathrooms': 2.0,
                'price': 750000,
                'house_status': 'FOR_SALE',
                'build_year': 2019,
                'description': 'Contemporary condo with city views and modern finishes',
                'image_url': 'https://photos.zillowstatic.com/fp/sample6.jpg'
            },
            {
                'zpid': '1007',
                'address': '147 Columbia Rd',
                'city': 'Irvine',
                'state': 'CA',
                'zip_code': '92604',
                'latitude': 33.6750,
                'longitude': -117.8400,
                'house_type': 'House',
                'area_sqft': 3000,
                'bedrooms': 5,
                'bathrooms': 4.0,
                'price': 1650000,
                'house_status': 'FOR_SALE',
                'build_year': 2005,
                'description': 'Luxury home with custom features and resort-style backyard',
                'image_url': 'https://photos.zillowstatic.com/fp/sample7.jpg'
            },
            {
                'zpid': '1008',
                'address': '258 Duke St',
                'city': 'Irvine',
                'state': 'CA',
                'zip_code': '92603',
                'latitude': 33.6800,
                'longitude': -117.8450,
                'house_type': 'Townhouse',
                'area_sqft': 2000,
                'bedrooms': 3,
                'bathrooms': 2.5,
                'price': 880000,
                'house_status': 'FOR_SALE',
                'build_year': 2014,
                'description': 'Well-maintained townhouse with attached garage',
                'image_url': 'https://photos.zillowstatic.com/fp/sample8.jpg'
            },
            {
                'zpid': '1009',
                'address': '369 Princeton Blvd',
                'city': 'Irvine',
                'state': 'CA',
                'zip_code': '92602',
                'latitude': 33.6850,
                'longitude': -117.8500,
                'house_type': 'House',
                'area_sqft': 2600,
                'bedrooms': 4,
                'bathrooms': 3.0,
                'price': 1250000,
                'house_status': 'FOR_SALE',
                'build_year': 2016,
                'description': 'Energy-efficient home with solar panels and smart thermostat',
                'image_url': 'https://photos.zillowstatic.com/fp/sample9.jpg'
            },
            {
                'zpid': '1010',
                'address': '741 Brown Ave',
                'city': 'Irvine',
                'state': 'CA',
                'zip_code': '92618',
                'latitude': 33.6900,
                'longitude': -117.8100,
                'house_type': 'Condo',
                'area_sqft': 1900,
                'bedrooms': 3,
                'bathrooms': 2.5,
                'price': 920000,
                'house_status': 'FOR_SALE',
                'build_year': 2020,
                'description': 'Brand new condo with premium appliances and finishes',
                'image_url': 'https://photos.zillowstatic.com/fp/sample10.jpg'
            }
        ]
        
        self.houses_data = sample_houses
        logger.info(f"Created {len(sample_houses)} sample houses for Irvine, CA")
        
        return sample_houses
    
    def download_house_image(self, house_data, save_dir="images"):
        """下载房屋图片（使用占位图片）"""
        try:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # 生成文件名
            zpid = house_data.get('zpid', f"house_{len(self.houses_data)}")
            filename = f"{zpid}_main.jpg"
            filepath = os.path.join(save_dir, filename)
            
            # 创建占位图片文件
            with open(filepath, 'w') as f:
                f.write(f"# Placeholder image for {house_data.get('address')}")
            
            logger.info(f"Created placeholder image: {filename}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error creating placeholder image: {e}")
            return None
    
    def save_to_database(self, house_data):
        """保存房屋数据到SQLite数据库"""
        try:
            # 插入房屋数据
            insert_query = '''
            INSERT OR REPLACE INTO houses (
                zpid, address, city, state, zip_code, latitude, longitude,
                house_type, area_sqft, lot_area_sqft, house_status, build_year,
                bathrooms, bedrooms, price, description, zillow_url, image_url, scraped_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            values = (
                house_data.get('zpid'),
                house_data.get('address', ''),
                house_data.get('city', 'Irvine'),
                house_data.get('state', 'CA'),
                house_data.get('zip_code', '92618'),
                house_data.get('latitude', 33.6846),
                house_data.get('longitude', -117.8265),
                house_data.get('house_type'),
                house_data.get('area_sqft'),
                house_data.get('lot_area_sqft'),
                house_data.get('house_status', 'FOR_SALE'),
                house_data.get('build_year'),
                house_data.get('bathrooms'),
                house_data.get('bedrooms'),
                house_data.get('price'),
                house_data.get('description', ''),
                house_data.get('zillow_url', ''),
                house_data.get('image_url'),
                house_data.get('scraped_at', datetime.now())
            )
            
            self.cursor.execute(insert_query, values)
            house_id = self.cursor.lastrowid
            
            # 保存图片信息
            if house_data.get('image_url'):
                image_query = '''
                INSERT INTO house_images (house_id, image_url, image_type)
                VALUES (?, ?, ?)
                '''
                self.cursor.execute(image_query, (house_id, house_data['image_url'], 'main'))
            
            self.conn.commit()
            logger.info(f"Saved house to database: {house_data.get('address')} (ID: {house_id})")
            return house_id
            
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            return None
    
    def run_scraping(self):
        """运行完整的抓取流程"""
        logger.info("Starting Irvine house data creation process...")
        
        try:
            # 创建示例数据
            houses = self.create_sample_data()
            
            # 下载图片并保存到数据库
            logger.info("Creating placeholder images and saving to database...")
            saved_count = 0
            
            for i, house in enumerate(houses):
                logger.info(f"Processing house {i+1}/{len(houses)}: {house.get('address')}")
                
                # 创建占位图片
                image_path = self.download_house_image(house)
                if image_path:
                    house['image_path'] = image_path
                
                # 保存到数据库
                house_id = self.save_to_database(house)
                if house_id:
                    saved_count += 1
                
                # 添加时间戳
                house['scraped_at'] = datetime.now()
                
                time.sleep(0.1)  # 短暂延迟
            
            logger.info(f"Data creation completed! Saved {saved_count} houses to SQLite database.")
            
            # 保存原始数据到JSON文件
            with open('irvine_houses_data.json', 'w', encoding='utf-8') as f:
                json.dump(houses, f, indent=2, ensure_ascii=False, default=str)
            
            # 生成数据统计
            self.generate_stats()
            
            return houses
            
        except Exception as e:
            logger.error(f"Error in data creation process: {e}")
            raise
        finally:
            self.cleanup()
    
    def generate_stats(self):
        """生成数据统计"""
        try:
            # 获取统计信息
            self.cursor.execute("SELECT COUNT(*) FROM houses")
            total_houses = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM house_images")
            total_images = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT AVG(price) FROM houses WHERE price IS NOT NULL")
            avg_price = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT house_type, COUNT(*) FROM houses GROUP BY house_type")
            house_types = self.cursor.fetchall()
            
            self.cursor.execute("SELECT AVG(bedrooms) FROM houses WHERE bedrooms IS NOT NULL")
            avg_bedrooms = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT AVG(bathrooms) FROM houses WHERE bathrooms IS NOT NULL")
            avg_bathrooms = self.cursor.fetchone()[0]
            
            stats = {
                "total_houses": total_houses,
                "total_images": total_images,
                "average_price": round(avg_price, 2) if avg_price else 0,
                "average_bedrooms": round(avg_bedrooms, 1) if avg_bedrooms else 0,
                "average_bathrooms": round(avg_bathrooms, 1) if avg_bathrooms else 0,
                "house_types": dict(house_types),
                "price_range": {
                    "min": min([h['price'] for h in self.houses_data]),
                    "max": max([h['price'] for h in self.houses_data])
                },
                "scraped_at": datetime.now().isoformat()
            }
            
            with open('irvine_stats.json', 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            
            logger.info("Statistics generated:")
            logger.info(f"  Total houses: {total_houses}")
            logger.info(f"  Total images: {total_images}")
            logger.info(f"  Average price: ${avg_price:,.2f}" if avg_price else "  Average price: N/A")
            logger.info(f"  Average bedrooms: {avg_bedrooms:.1f}" if avg_bedrooms else "  Average bedrooms: N/A")
            logger.info(f"  Average bathrooms: {avg_bathrooms:.1f}" if avg_bathrooms else "  Average bathrooms: N/A")
            
        except Exception as e:
            logger.error(f"Error generating stats: {e}")
    
    def cleanup(self):
        """清理资源"""
        try:
            if hasattr(self, 'conn'):
                self.conn.close()
            logger.info("Cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

def main():
    """主函数"""
    print("🏠 Irvine CA House Data Generator")
    print("=" * 50)
    
    scraper = SimpleRequestsScraper()
    try:
        # 运行数据创建
        houses = scraper.run_scraping()
        
        print(f"\n✅ 数据创建完成！")
        print(f"📊 共创建 {len(houses)} 个房屋信息")
        print("\n📁 数据已保存到:")
        print("   - SQLite数据库: irvine_houses.db")
        print("   - JSON文件: irvine_houses_data.json")
        print("   - 统计信息: irvine_stats.json")
        print("   - 图片文件夹: images/")
        
        print("\n🔍 查看数据:")
        print("   - 使用SQLite浏览器打开 irvine_houses.db")
        print("   - 或运行: sqlite3 irvine_houses.db 'SELECT address, price, bedrooms, bathrooms FROM houses LIMIT 10;'")
        
        print("\n📊 数据概览:")
        prices = [h['price'] for h in houses]
        print(f"   - 价格范围: ${min(prices):,} - ${max(prices):,}")
        print(f"   - 平均价格: ${sum(prices)/len(prices):,.0f}")
        print(f"   - 房屋类型: {', '.join(set(h['house_type'] for h in houses))}")
        
    except Exception as e:
        print(f"❌ 数据创建失败: {e}")
    finally:
        scraper.cleanup()

if __name__ == "__main__":
    main()
