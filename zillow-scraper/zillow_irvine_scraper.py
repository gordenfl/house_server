#!/usr/bin/env python3
"""
Zillow Irvine CA House Data Scraper
抓取Irvine, CA附近的房屋数据，包括房屋信息、图片和详细信息
"""

import requests
import json
import time
import random
import os
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from urllib.parse import urljoin, urlparse
import urllib.request
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ZillowIrvineScraper:
    def __init__(self):
        self.base_url = "https://www.zillow.com"
        self.irvine_url = "https://www.zillow.com/irvine-ca/"
        self.ua = UserAgent()
        self.session = requests.Session()
        self.houses_data = []
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
        """设置数据库连接"""
        try:
            self.db_connection = pymysql.connect(
                host='localhost',
                user='house_user',
                password='house_password',
                database='house_db',
                charset='utf8mb4',
                autocommit=True
            )
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def get_house_listings(self, max_pages=5):
        """获取房屋列表"""
        logger.info(f"Starting to scrape house listings from Irvine, CA (max {max_pages} pages)")
        
        for page in range(1, max_pages + 1):
            try:
                # 构建搜索URL
                search_url = f"{self.irvine_url}?p={page}"
                logger.info(f"Scraping page {page}: {search_url}")
                
                self.driver.get(search_url)
                time.sleep(random.uniform(2, 4))
                
                # 等待页面加载
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='property-card']")))
                
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
                time.sleep(random.uniform(3, 6))
                
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
            link_element = card.find_element(By.CSS_SELECTOR, "a[data-test='property-card-link']")
            house_url = urljoin(self.base_url, link_element.get_attribute('href'))
            house_data['zillow_url'] = house_url
            
            # 提取ZPID
            zpid_match = house_url.split('/')[-1].split('_')[0]
            if zpid_match.isdigit():
                house_data['zpid'] = zpid_match
            
            # 获取地址
            try:
                address_element = card.find_element(By.CSS_SELECTOR, "[data-test='property-card-addr']")
                house_data['address'] = address_element.text.strip()
            except:
                house_data['address'] = "Address not available"
            
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
                house_data['house_type'] = "Unknown"
            
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
            house_data['zip_code'] = "92618"  # Irvine的默认邮编
            
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
                details['lot_area_acres'] = self.extract_number(part)
        
        return details
    
    def extract_number(self, text):
        """从文本中提取数字"""
        import re
        numbers = re.findall(r'\d+\.?\d*', text)
        return float(numbers[0]) if numbers else None
    
    def get_detailed_house_info(self, house_data):
        """获取房屋详细信息"""
        try:
            if not house_data.get('zillow_url'):
                return house_data
            
            logger.info(f"Getting detailed info for: {house_data['address']}")
            
            self.driver.get(house_data['zillow_url'])
            time.sleep(random.uniform(2, 4))
            
            # 等待页面加载
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ds-bed-bath-beyond")))
            except:
                pass
            
            # 获取更多详细信息
            try:
                # 获取完整地址
                address_element = self.driver.find_element(By.CSS_SELECTOR, "h1[data-test='property-details-header']")
                full_address = address_element.text.strip()
                house_data['full_address'] = full_address
            except:
                pass
            
            # 获取坐标
            try:
                # 从页面中提取坐标信息
                script_tags = self.driver.find_elements(By.TAG_NAME, "script")
                for script in script_tags:
                    script_content = script.get_attribute('innerHTML')
                    if 'latitude' in script_content and 'longitude' in script_content:
                        # 简单的正则表达式提取坐标
                        import re
                        lat_match = re.search(r'"latitude":\s*([+-]?\d+\.?\d*)', script_content)
                        lng_match = re.search(r'"longitude":\s*([+-]?\d+\.?\d*)', script_content)
                        if lat_match and lng_match:
                            house_data['latitude'] = float(lat_match.group(1))
                            house_data['longitude'] = float(lng_match.group(1))
                            break
            except:
                # 如果无法获取精确坐标，使用Irvine的大致坐标
                house_data['latitude'] = 33.6846
                house_data['longitude'] = -117.8265
            
            # 获取年份
            try:
                year_element = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='year-built']")
                house_data['build_year'] = int(year_element.text.strip())
            except:
                pass
            
            # 获取房屋状态
            try:
                status_element = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='property-status']")
                house_data['house_status'] = status_element.text.strip()
            except:
                house_data['house_status'] = "For Sale"
            
            # 获取更多图片
            try:
                img_elements = self.driver.find_elements(By.CSS_SELECTOR, ".media-stream img")
                image_urls = [img.get_attribute('src') for img in img_elements[:5]]  # 最多5张图片
                house_data['additional_images'] = image_urls
            except:
                house_data['additional_images'] = []
            
            # 获取描述
            try:
                desc_element = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='property-description']")
                house_data['description'] = desc_element.text.strip()
            except:
                pass
            
            time.sleep(random.uniform(1, 3))
            return house_data
            
        except Exception as e:
            logger.error(f"Error getting detailed info: {e}")
            return house_data
    
    def download_house_image(self, house_data, save_dir="images"):
        """下载房屋图片"""
        try:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            if not house_data.get('image_url'):
                return None
            
            # 生成文件名
            zpid = house_data.get('zpid', 'unknown')
            filename = f"{zpid}_main.jpg"
            filepath = os.path.join(save_dir, filename)
            
            # 下载图片
            urllib.request.urlretrieve(house_data['image_url'], filepath)
            logger.info(f"Downloaded image: {filename}")
            
            # 下载额外图片
            if house_data.get('additional_images'):
                for i, img_url in enumerate(house_data['additional_images'][:3]):  # 最多下载3张额外图片
                    try:
                        extra_filename = f"{zpid}_extra_{i+1}.jpg"
                        extra_filepath = os.path.join(save_dir, extra_filename)
                        urllib.request.urlretrieve(img_url, extra_filepath)
                        logger.info(f"Downloaded extra image: {extra_filename}")
                    except:
                        continue
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            return None
    
    def save_to_database(self, house_data):
        """保存房屋数据到数据库"""
        try:
            cursor = self.db_connection.cursor()
            
            # 检查房屋类型
            house_type = self.get_house_type_id(house_data.get('house_type', 'Unknown'))
            house_status = self.get_house_status_id(house_data.get('house_status', 'For Sale'))
            
            # 插入房屋数据
            insert_query = """
            INSERT INTO houses (
                address, city, state, zip_code, latitude, longitude,
                house_type_id, area_sqft, house_status_id, build_year,
                bathrooms, bedrooms, description, zillow_id, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW()
            )
            """
            
            values = (
                house_data.get('address', ''),
                house_data.get('city', 'Irvine'),
                house_data.get('state', 'CA'),
                house_data.get('zip_code', '92618'),
                house_data.get('latitude', 33.6846),
                house_data.get('longitude', -117.8265),
                house_type,
                house_data.get('area_sqft'),
                house_status,
                house_data.get('build_year'),
                house_data.get('bathrooms'),
                house_data.get('bedrooms'),
                house_data.get('description', ''),
                house_data.get('zpid')
            )
            
            cursor.execute(insert_query, values)
            house_id = cursor.lastrowid
            
            # 如果有价格信息，插入销售记录
            if house_data.get('price'):
                sale_query = """
                INSERT INTO house_sales (house_id, sale_date, sale_price, created_at)
                VALUES (%s, %s, %s, NOW())
                """
                cursor.execute(sale_query, (house_id, datetime.now().date(), house_data['price']))
            
            logger.info(f"Saved house to database: {house_data.get('address')} (ID: {house_id})")
            return house_id
            
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            return None
    
    def get_house_type_id(self, house_type):
        """获取房屋类型ID"""
        type_mapping = {
            'House': 'HOUSE',
            'Condo': 'CONDO',
            'Apartment': 'APARTMENT',
            'Townhouse': 'HOUSE'
        }
        
        mapped_type = type_mapping.get(house_type, 'HOUSE')
        
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id FROM house_types WHERE name = %s", (mapped_type,))
            result = cursor.fetchone()
            return result[0] if result else 3  # 默认HOUSE
        except:
            return 3
    
    def get_house_status_id(self, house_status):
        """获取房屋状态ID"""
        status_mapping = {
            'For Sale': 'FOR_SALE',
            'Sold': 'SOLD',
            'Foreclosed': 'FORECLOSED'
        }
        
        mapped_status = status_mapping.get(house_status, 'FOR_SALE')
        
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id FROM house_statuses WHERE name = %s", (mapped_status,))
            result = cursor.fetchone()
            return result[0] if result else 1  # 默认FOR_SALE
        except:
            return 1
    
    def run_scraping(self, max_pages=3, get_details=True):
        """运行完整的抓取流程"""
        logger.info("Starting Zillow Irvine CA scraping process...")
        
        try:
            # 获取房屋列表
            houses = self.get_house_listings(max_pages)
            
            # 获取详细信息
            if get_details:
                for i, house in enumerate(houses):
                    logger.info(f"Processing house {i+1}/{len(houses)}")
                    houses[i] = self.get_detailed_house_info(house)
                    time.sleep(random.uniform(2, 4))  # 避免被封
            
            # 下载图片
            logger.info("Downloading house images...")
            for house in houses:
                self.download_house_image(house)
                time.sleep(random.uniform(1, 2))
            
            # 保存到数据库
            logger.info("Saving data to database...")
            saved_count = 0
            for house in houses:
                house_id = self.save_to_database(house)
                if house_id:
                    saved_count += 1
            
            logger.info(f"Scraping completed! Saved {saved_count} houses to database.")
            
            # 保存原始数据到JSON文件
            with open('irvine_houses_data.json', 'w', encoding='utf-8') as f:
                json.dump(houses, f, indent=2, ensure_ascii=False, default=str)
            
            return houses
            
        except Exception as e:
            logger.error(f"Error in scraping process: {e}")
            raise
        finally:
            self.cleanup()
    
    def cleanup(self):
        """清理资源"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
            if hasattr(self, 'db_connection'):
                self.db_connection.close()
            logger.info("Cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

def main():
    """主函数"""
    scraper = ZillowIrvineScraper()
    try:
        # 运行抓取，最多抓取3页数据
        houses = scraper.run_scraping(max_pages=3, get_details=True)
        print(f"\n✅ 抓取完成！共获取 {len(houses)} 个房屋信息")
        print("📁 数据已保存到:")
        print("   - 数据库: house_db.houses 表")
        print("   - JSON文件: irvine_houses_data.json")
        print("   - 图片文件夹: images/")
        
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
    finally:
        scraper.cleanup()

if __name__ == "__main__":
    main()
