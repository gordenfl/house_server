#!/usr/bin/env python3
"""
Simple Zillow Irvine CA House Data Scraper
使用SQLite数据库的简化版本，抓取Irvine, CA附近的房屋数据
"""

import requests
import json
import time
import random
import os
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from urllib.parse import urljoin
import urllib.request
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleIrvineScraper:
    def __init__(self, db_path="irvine_houses.db"):
        self.base_url = "https://www.zillow.com"
        self.irvine_url = "https://www.zillow.com/irvine-ca/"
        self.ua = UserAgent()
        self.houses_data = []
        self.db_path = db_path
        self.setup_driver()
        self.setup_database()
        
    def setup_driver(self):
        """设置Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        
        # 禁用图片加载以加快速度
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("WebDriver setup completed")
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {e}")
            raise
    
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
    
    def get_house_listings(self, max_pages=3):
        """获取房屋列表"""
        logger.info(f"Starting to scrape house listings from Irvine, CA (max {max_pages} pages)")
        
        for page in range(1, max_pages + 1):
            try:
                # 构建搜索URL
                search_url = f"{self.irvine_url}?p={page}"
                logger.info(f"Scraping page {page}: {search_url}")
                
                self.driver.get(search_url)
                time.sleep(random.uniform(3, 5))
                
                # 等待页面加载
                try:
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='property-card']")))
                except:
                    logger.warning(f"Timeout waiting for page {page} to load")
                    continue
                
                # 获取房屋卡片
                house_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-test='property-card']")
                logger.info(f"Found {len(house_cards)} house cards on page {page}")
                
                for i, card in enumerate(house_cards):
                    try:
                        house_data = self.extract_house_info(card, page, i)
                        if house_data:
                            self.houses_data.append(house_data)
                            logger.info(f"Extracted house {len(self.houses_data)}: {house_data.get('address', 'Unknown')}")
                    except Exception as e:
                        logger.error(f"Error extracting house info from card {i}: {e}")
                        continue
                
                # 随机延迟避免被封
                time.sleep(random.uniform(4, 7))
                
            except Exception as e:
                logger.error(f"Error scraping page {page}: {e}")
                continue
        
        logger.info(f"Completed scraping. Total houses found: {len(self.houses_data)}")
        return self.houses_data
    
    def extract_house_info(self, card, page_num, card_index):
        """从房屋卡片中提取信息"""
        try:
            house_data = {}
            
            # 获取房屋链接
            try:
                link_element = card.find_element(By.CSS_SELECTOR, "a[data-test='property-card-link']")
                house_url = urljoin(self.base_url, link_element.get_attribute('href'))
                house_data['zillow_url'] = house_url
                
                # 提取ZPID
                zpid_match = house_url.split('/')[-1].split('_')[0]
                if zpid_match.isdigit():
                    house_data['zpid'] = zpid_match
            except:
                house_data['zpid'] = f"page{page_num}_card{card_index}"
            
            # 获取地址
            try:
                address_element = card.find_element(By.CSS_SELECTOR, "[data-test='property-card-addr']")
                house_data['address'] = address_element.text.strip()
            except:
                house_data['address'] = f"Irvine Address {len(self.houses_data) + 1}"
            
            # 获取价格
            try:
                price_element = card.find_element(By.CSS_SELECTOR, "[data-test='property-card-price']")
                price_text = price_element.text.strip()
                house_data['price'] = self.parse_price(price_text)
            except:
                house_data['price'] = None
            
            # 获取房屋基本信息
            try:
                details_element = card.find_element(By.CSS_SELECTOR, "[data-test='property-card-details']")
                details_text = details_element.text.strip()
                house_data.update(self.parse_house_details(details_text))
            except:
                pass
            
            # 获取房屋类型
            try:
                type_element = card.find_element(By.CSS_SELECTOR, "[data-test='property-card-type']")
                house_data['house_type'] = type_element.text.strip()
            except:
                house_data['house_type'] = "House"
            
            # 获取图片
            try:
                img_element = card.find_element(By.CSS_SELECTOR, "img[data-test='property-card-img']")
                img_url = img_element.get_attribute('src')
                house_data['image_url'] = img_url
            except:
                house_data['image_url'] = None
            
            # 设置默认位置信息（Irvine, CA）
            house_data['city'] = "Irvine"
            house_data['state'] = "CA"
            house_data['zip_code'] = "92618"
            
            # 添加抓取时间戳
            house_data['scraped_at'] = datetime.now()
            
            return house_data
            
        except Exception as e:
            logger.error(f"Error extracting house info: {e}")
            return None
    
    def parse_price(self, price_text):
        """解析价格"""
        try:
            # 移除货币符号和逗号
            price_clean = price_text.replace('$', '').replace(',', '').replace('+', '')
            
            # 处理价格范围 (如 $500K - $600K)
            if ' - ' in price_clean:
                prices = price_clean.split(' - ')
                low_price = int(prices[0].replace('K', '000').replace('M', '000000'))
                high_price = int(prices[1].replace('K', '000').replace('M', '000000'))
                return (low_price + high_price) // 2  # 返回平均价格
            
            # 处理单个价格
            if 'K' in price_clean:
                return int(price_clean.replace('K', '000'))
            elif 'M' in price_clean:
                return int(price_clean.replace('M', '000000'))
            else:
                return int(price_clean)
        except:
            return None
    
    def parse_house_details(self, details_text):
        """解析房屋详细信息"""
        details = {}
        parts = details_text.split(' · ')
        
        for part in parts:
            part = part.strip()
            if 'bed' in part.lower():
                details['bedrooms'] = self.extract_number(part)
            elif 'bath' in part.lower():
                details['bathrooms'] = self.extract_number(part)
            elif 'sqft' in part.lower() or 'sq ft' in part.lower():
                details['area_sqft'] = self.extract_number(part)
            elif 'acre' in part.lower():
                details['lot_area_sqft'] = int(self.extract_number(part) * 43560)  # 转换为平方英尺
        
        return details
    
    def extract_number(self, text):
        """从文本中提取数字"""
        import re
        numbers = re.findall(r'\d+\.?\d*', text)
        return float(numbers[0]) if numbers else None
    
    def download_house_image(self, house_data, save_dir="images"):
        """下载房屋图片"""
        try:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            if not house_data.get('image_url'):
                return None
            
            # 生成文件名
            zpid = house_data.get('zpid', f"house_{len(self.houses_data)}")
            filename = f"{zpid}_main.jpg"
            filepath = os.path.join(save_dir, filename)
            
            # 下载图片
            urllib.request.urlretrieve(house_data['image_url'], filepath)
            logger.info(f"Downloaded image: {filename}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
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
                house_data.get('zillow_url'),
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
    
    def run_scraping(self, max_pages=3):
        """运行完整的抓取流程"""
        logger.info("Starting Zillow Irvine CA scraping process...")
        
        try:
            # 获取房屋列表
            houses = self.get_house_listings(max_pages)
            
            # 下载图片并保存到数据库
            logger.info("Downloading house images and saving to database...")
            saved_count = 0
            
            for i, house in enumerate(houses):
                logger.info(f"Processing house {i+1}/{len(houses)}: {house.get('address')}")
                
                # 下载图片
                image_path = self.download_house_image(house)
                if image_path:
                    house['image_path'] = image_path
                
                # 保存到数据库
                house_id = self.save_to_database(house)
                if house_id:
                    saved_count += 1
                
                # 随机延迟
                time.sleep(random.uniform(1, 3))
            
            logger.info(f"Scraping completed! Saved {saved_count} houses to SQLite database.")
            
            # 保存原始数据到JSON文件
            with open('irvine_houses_data.json', 'w', encoding='utf-8') as f:
                json.dump(houses, f, indent=2, ensure_ascii=False, default=str)
            
            # 生成数据统计
            self.generate_stats()
            
            return houses
            
        except Exception as e:
            logger.error(f"Error in scraping process: {e}")
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
            
            stats = {
                "total_houses": total_houses,
                "total_images": total_images,
                "average_price": round(avg_price, 2) if avg_price else 0,
                "house_types": dict(house_types),
                "scraped_at": datetime.now().isoformat()
            }
            
            with open('irvine_stats.json', 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            
            logger.info("Statistics generated:")
            logger.info(f"  Total houses: {total_houses}")
            logger.info(f"  Total images: {total_images}")
            logger.info(f"  Average price: ${avg_price:,.2f}" if avg_price else "  Average price: N/A")
            
        except Exception as e:
            logger.error(f"Error generating stats: {e}")
    
    def cleanup(self):
        """清理资源"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
            if hasattr(self, 'conn'):
                self.conn.close()
            logger.info("Cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

def main():
    """主函数"""
    print("🏠 Zillow Irvine CA House Data Scraper")
    print("=" * 50)
    
    scraper = SimpleIrvineScraper()
    try:
        # 运行抓取，最多抓取3页数据
        houses = scraper.run_scraping(max_pages=3)
        
        print(f"\n✅ 抓取完成！")
        print(f"📊 共获取 {len(houses)} 个房屋信息")
        print("\n📁 数据已保存到:")
        print("   - SQLite数据库: irvine_houses.db")
        print("   - JSON文件: irvine_houses_data.json")
        print("   - 统计信息: irvine_stats.json")
        print("   - 图片文件夹: images/")
        
        print("\n🔍 查看数据:")
        print("   - 使用SQLite浏览器打开 irvine_houses.db")
        print("   - 或运行: sqlite3 irvine_houses.db 'SELECT * FROM houses LIMIT 5;'")
        
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
    finally:
        scraper.cleanup()

if __name__ == "__main__":
    main()
