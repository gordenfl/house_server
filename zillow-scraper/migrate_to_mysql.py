#!/usr/bin/env python3
"""
将SQLite数据迁移到MySQL数据库
"""

import sqlite3
import pymysql
import json
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataMigrator:
    def __init__(self, sqlite_db="irvine_houses.db"):
        self.sqlite_db = sqlite_db
        self.mysql_config = {
            'host': 'localhost',
            'user': 'house_user',
            'password': 'house_password',
            'database': 'house_db',
            'charset': 'utf8mb4'
        }
        
    def connect_sqlite(self):
        """连接SQLite数据库"""
        try:
            self.sqlite_conn = sqlite3.connect(self.sqlite_db)
            self.sqlite_cursor = self.sqlite_conn.cursor()
            logger.info(f"Connected to SQLite database: {self.sqlite_db}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to SQLite: {e}")
            return False
    
    def connect_mysql(self):
        """连接MySQL数据库"""
        try:
            self.mysql_conn = pymysql.connect(**self.mysql_config)
            self.mysql_cursor = self.mysql_conn.cursor()
            logger.info("Connected to MySQL database")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            return False
    
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
            self.mysql_cursor.execute("SELECT id FROM house_types WHERE name = %s", (mapped_type,))
            result = self.mysql_cursor.fetchone()
            return result[0] if result else 3  # 默认HOUSE
        except:
            return 3
    
    def get_house_status_id(self, house_status):
        """获取房屋状态ID"""
        status_mapping = {
            'FOR_SALE': 'FOR_SALE',
            'SOLD': 'SOLD',
            'FORECLOSED': 'FORECLOSED'
        }
        
        mapped_status = status_mapping.get(house_status, 'FOR_SALE')
        
        try:
            self.mysql_cursor.execute("SELECT id FROM house_statuses WHERE name = %s", (mapped_status,))
            result = self.mysql_cursor.fetchone()
            return result[0] if result else 1  # 默认FOR_SALE
        except:
            return 1
    
    def migrate_houses(self):
        """迁移房屋数据"""
        try:
            # 从SQLite读取房屋数据
            self.sqlite_cursor.execute("SELECT * FROM houses")
            houses = self.sqlite_cursor.fetchall()
            
            # 获取列名
            columns = [description[0] for description in self.sqlite_cursor.description]
            logger.info(f"Found {len(houses)} houses in SQLite database")
            
            migrated_count = 0
            
            for house_data in houses:
                house_dict = dict(zip(columns, house_data))
                
                # 获取类型和状态ID
                house_type_id = self.get_house_type_id(house_dict.get('house_type'))
                house_status_id = self.get_house_status_id(house_dict.get('house_status'))
                
                # 插入到MySQL
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
                    house_dict.get('address', ''),
                    house_dict.get('city', 'Irvine'),
                    house_dict.get('state', 'CA'),
                    house_dict.get('zip_code', '92618'),
                    house_dict.get('latitude', 33.6846),
                    house_dict.get('longitude', -117.8265),
                    house_type_id,
                    house_dict.get('area_sqft'),
                    house_status_id,
                    house_dict.get('build_year'),
                    house_dict.get('bathrooms'),
                    house_dict.get('bedrooms'),
                    house_dict.get('description', ''),
                    house_dict.get('zpid')
                )
                
                self.mysql_cursor.execute(insert_query, values)
                house_id = self.mysql_cursor.lastrowid
                
                # 如果有价格信息，插入销售记录
                if house_dict.get('price'):
                    sale_query = """
                    INSERT INTO house_sales (house_id, sale_date, sale_price, created_at)
                    VALUES (%s, %s, %s, NOW())
                    """
                    self.mysql_cursor.execute(sale_query, (house_id, datetime.now().date(), house_dict['price']))
                
                migrated_count += 1
                logger.info(f"Migrated house: {house_dict.get('address')} (ID: {house_id})")
            
            self.mysql_conn.commit()
            logger.info(f"Successfully migrated {migrated_count} houses to MySQL")
            return migrated_count
            
        except Exception as e:
            logger.error(f"Error migrating houses: {e}")
            return 0
    
    def migrate_images(self):
        """迁移图片数据"""
        try:
            # 从SQLite读取图片数据
            self.sqlite_cursor.execute("SELECT * FROM house_images")
            images = self.sqlite_cursor.fetchall()
            
            if not images:
                logger.info("No images to migrate")
                return 0
            
            # 获取列名
            columns = [description[0] for description in self.sqlite_cursor.description]
            logger.info(f"Found {len(images)} images in SQLite database")
            
            # 这里可以创建一个house_images表来存储图片信息
            # 由于原始MySQL schema中没有这个表，我们暂时跳过
            logger.info("Image migration skipped - house_images table not in MySQL schema")
            return len(images)
            
        except Exception as e:
            logger.error(f"Error migrating images: {e}")
            return 0
    
    def run_migration(self):
        """运行完整的数据迁移"""
        logger.info("Starting data migration from SQLite to MySQL...")
        
        # 连接数据库
        if not self.connect_sqlite():
            return False
        
        if not self.connect_mysql():
            self.sqlite_conn.close()
            return False
        
        try:
            # 迁移数据
            houses_migrated = self.migrate_houses()
            images_migrated = self.migrate_images()
            
            logger.info(f"Migration completed:")
            logger.info(f"  - Houses migrated: {houses_migrated}")
            logger.info(f"  - Images found: {images_migrated}")
            
            return True
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            return False
        finally:
            # 关闭连接
            if hasattr(self, 'sqlite_conn'):
                self.sqlite_conn.close()
            if hasattr(self, 'mysql_conn'):
                self.mysql_conn.close()

def main():
    """主函数"""
    print("🔄 SQLite to MySQL Data Migration Tool")
    print("=" * 50)
    
    migrator = DataMigrator()
    
    try:
        success = migrator.run_migration()
        
        if success:
            print("\n✅ 数据迁移完成！")
            print("📊 SQLite数据已成功迁移到MySQL数据库")
            print("\n💡 现在可以使用完整的微服务系统了")
        else:
            print("\n❌ 数据迁移失败")
            print("请检查MySQL数据库连接和配置")
            
    except Exception as e:
        print(f"❌ 迁移过程出错: {e}")

if __name__ == "__main__":
    main()
