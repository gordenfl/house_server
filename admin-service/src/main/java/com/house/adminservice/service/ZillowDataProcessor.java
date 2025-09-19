package com.house.adminservice.service;

import com.house.common.dto.HouseDTO;
import com.house.common.entity.*;
import com.house.adminservice.repository.*;
import com.house.datacollectionservice.model.ZillowProperty;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ZillowDataProcessor {
    
    @Autowired
    private HouseRepository houseRepository;
    
    @Autowired
    private HouseTypeRepository houseTypeRepository;
    
    @Autowired
    private HouseStatusRepository houseStatusRepository;
    
    @RabbitListener(queues = "zillow.property.data")
    @Transactional
    public void processZillowProperty(ZillowProperty zillowProperty) {
        try {
            System.out.println("Processing Zillow property: " + zillowProperty.getZpid());
            
            // 检查是否已存在
            if (houseRepository.findByZillowId(zillowProperty.getZpid()).isPresent()) {
                System.out.println("Property already exists: " + zillowProperty.getZpid());
                return;
            }
            
            // 创建或更新房屋记录
            House house = new House();
            house.setAddress(zillowProperty.getStreetAddress());
            house.setCity(zillowProperty.getCity());
            house.setState(zillowProperty.getState());
            house.setZipCode(zillowProperty.getZipcode());
            house.setLatitude(zillowProperty.getLatitude());
            house.setLongitude(zillowProperty.getLongitude());
            house.setAreaSqft(zillowProperty.getLivingArea());
            house.setLotAreaSqft(zillowProperty.getLotAreaValue());
            house.setBuildYear(zillowProperty.getYearBuilt());
            house.setBathrooms(zillowProperty.getBathrooms() != null ? zillowProperty.getBathrooms().intValue() : 0);
            house.setBedrooms(zillowProperty.getBedrooms());
            house.setDescription(zillowProperty.getDescription());
            house.setZillowId(zillowProperty.getZpid());
            
            // 设置房屋类型
            HouseType houseType = mapZillowHomeTypeToHouseType(zillowProperty.getHomeType());
            house.setHouseType(houseType);
            
            // 设置房屋状态
            HouseStatus houseStatus = mapZillowStatusToHouseStatus(zillowProperty.getHomeStatus());
            house.setHouseStatus(houseStatus);
            
            // 保存房屋
            houseRepository.save(house);
            
            System.out.println("Successfully processed property: " + zillowProperty.getZpid());
            
        } catch (Exception e) {
            System.err.println("Error processing Zillow property " + zillowProperty.getZpid() + ": " + e.getMessage());
        }
    }
    
    private HouseType mapZillowHomeTypeToHouseType(String zillowHomeType) {
        if (zillowHomeType == null) {
            return houseTypeRepository.findByName("HOUSE").orElse(null);
        }
        
        switch (zillowHomeType.toLowerCase()) {
            case "single family":
            case "house":
                return houseTypeRepository.findByName("HOUSE").orElse(null);
            case "condo":
            case "condominium":
                return houseTypeRepository.findByName("CONDO").orElse(null);
            case "apartment":
                return houseTypeRepository.findByName("APARTMENT").orElse(null);
            default:
                return houseTypeRepository.findByName("HOUSE").orElse(null);
        }
    }
    
    private HouseStatus mapZillowStatusToHouseStatus(String zillowStatus) {
        if (zillowStatus == null) {
            return houseStatusRepository.findByName("FOR_SALE").orElse(null);
        }
        
        switch (zillowStatus.toLowerCase()) {
            case "for sale":
            case "for sale by owner":
                return houseStatusRepository.findByName("FOR_SALE").orElse(null);
            case "sold":
                return houseStatusRepository.findByName("SOLD").orElse(null);
            case "foreclosed":
                return houseStatusRepository.findByName("FORECLOSED").orElse(null);
            default:
                return houseStatusRepository.findByName("FOR_SALE").orElse(null);
        }
    }
}
